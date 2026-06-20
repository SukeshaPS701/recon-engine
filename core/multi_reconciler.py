from utils.logger import get_logger

logger = get_logger("multi_reconciler")


def normalize_ref(ref):
    return str(ref).strip().upper()


def is_reference_similar(ref1, ref2):
    ref1 = normalize_ref(ref1)
    ref2 = normalize_ref(ref2)

    if ref1 == ref2:
        return True

    if ref1 and ref2 and (ref1 in ref2 or ref2 in ref1):
        return True

    return False


def find_existing_group_key(grouped, txn):
    """
    Try to place a transaction into an existing group using:
    1. same date
    2. exact or fuzzy reference similarity
    """
    txn_date = str(txn.get("date", "")).strip()
    txn_ref = normalize_ref(txn.get("reference", ""))

    for key, row in grouped.items():
        row_date = str(row.get("date", "")).strip()
        row_ref = normalize_ref(row.get("reference", ""))

        if txn_date == row_date and is_reference_similar(txn_ref, row_ref):
            return key

    return None


def reconcile_multi_source(csv_transactions, mt940_transactions, camt053_transactions):
    logger.info("Starting multi-source reconciliation")

    grouped = {}

    def ensure_group(txn):
        existing_key = find_existing_group_key(grouped, txn)

        if existing_key:
            return grouped[existing_key]

        # create new group if no fuzzy/exact match group exists
        date = str(txn.get("date", "")).strip()
        ref = normalize_ref(txn.get("reference", ""))
        key = f"{date}|{ref}"

        grouped[key] = {
            "group_key": key,

            "csv_txn_id": "",
            "mt940_txn_id": "",
            "camt053_txn_id": "",

            "csv_amount": None,
            "mt940_amount": None,
            "camt053_amount": None,

            "csv_bank": "",
            "mt940_bank": "",
            "camt053_bank": "",

            "csv_channel": "",
            "mt940_channel": "",
            "camt053_channel": "",

            "date": txn.get("date", ""),
            "reference": txn.get("reference", ""),
        }
        return grouped[key]

    # Load CSV transactions
    for txn in csv_transactions:
        row = ensure_group(txn)
        row["csv_txn_id"] = txn["txn_id"]
        row["csv_amount"] = txn["amount"]
        row["csv_bank"] = txn["bank"]
        row["csv_channel"] = txn["channel"]

    # Load MT940 transactions
    for txn in mt940_transactions:
        row = ensure_group(txn)
        row["mt940_txn_id"] = txn["txn_id"]
        row["mt940_amount"] = txn["amount"]
        row["mt940_bank"] = txn["bank"]
        row["mt940_channel"] = txn["channel"]

    # Load CAMT053 transactions
    for txn in camt053_transactions:
        row = ensure_group(txn)
        row["camt053_txn_id"] = txn["txn_id"]
        row["camt053_amount"] = txn["amount"]
        row["camt053_bank"] = txn["bank"]
        row["camt053_channel"] = txn["channel"]

    results = []

    for _, row in grouped.items():
        presence_count = sum([
            1 if row["csv_txn_id"] else 0,
            1 if row["mt940_txn_id"] else 0,
            1 if row["camt053_txn_id"] else 0
        ])

        amounts = [
            row["csv_amount"],
            row["mt940_amount"],
            row["camt053_amount"]
        ]
        non_null_amounts = [a for a in amounts if a is not None]

        if presence_count == 3:
            if len(set(non_null_amounts)) == 1:
                row["final_status"] = "FULL_MATCH"
                row["exception_reason"] = ""
            else:
                row["final_status"] = "AMOUNT_MISMATCH"
                row["exception_reason"] = "Transaction exists in all sources but amounts differ"

        elif presence_count == 2:
            row["final_status"] = "PARTIAL_MATCH"
            missing_sources = []
            if not row["csv_txn_id"]:
                missing_sources.append("CSV")
            if not row["mt940_txn_id"]:
                missing_sources.append("MT940")
            if not row["camt053_txn_id"]:
                missing_sources.append("CAMT053")
            row["exception_reason"] = f"Missing in {', '.join(missing_sources)}"

        else:
            row["final_status"] = "UNMATCHED"
            present_sources = []
            if row["csv_txn_id"]:
                present_sources.append("CSV")
            if row["mt940_txn_id"]:
                present_sources.append("MT940")
            if row["camt053_txn_id"]:
                present_sources.append("CAMT053")
            row["exception_reason"] = f"Exists only in {', '.join(present_sources)}"

        results.append(row)

    logger.info(f"Multi-source reconciliation complete | grouped_records={len(results)}")
    return results