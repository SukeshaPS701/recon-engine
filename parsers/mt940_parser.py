from utils.logger import get_logger

logger = get_logger("mt940_parser")

def parse_mt940(file_path):
    logger.info(f"Reading MT940 file: {file_path}")

    transactions = []
    current_txn = {}

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()

        if line.startswith(":20:"):
            current_txn["txn_id"] = line.replace(":20:", "").strip()

        elif line.startswith(":25:"):
            current_txn["bank"] = line.replace(":25:", "").strip()

        elif line.startswith(":61:"):
            # Example simplified format:
            # :61:20260618D1000,00NTRFREF123
            content = line.replace(":61:", "").strip()

            date_part = content[:8]
            debit_credit = content[8]
            remaining = content[9:]

            amount_str = ""
            ref_part = ""

            for i, ch in enumerate(remaining):
                if ch.isalpha():
                    ref_part = remaining[i:]
                    break
                amount_str += ch

            amount = float(amount_str.replace(",", ".")) if amount_str else 0.0
            if debit_credit == "D":
                amount = -amount

            current_txn["date"] = f"{date_part[:4]}-{date_part[4:6]}-{date_part[6:]}"
            current_txn["amount"] = amount
            current_txn["reference"] = ref_part

        elif line.startswith(":86:"):
            narrative = line.replace(":86:", "").strip()
            parts = narrative.split("|")

            current_txn["sender"] = parts[0].strip() if len(parts) > 0 else ""
            current_txn["receiver"] = parts[1].strip() if len(parts) > 1 else ""
            current_txn["channel"] = parts[2].strip() if len(parts) > 2 else "UNKNOWN"
            current_txn["currency"] = "INR"
            current_txn["source_format"] = "MT940"

            transactions.append(current_txn)
            current_txn = {}

    logger.info(f"Parsed {len(transactions)} MT940 transactions")
    return transactions