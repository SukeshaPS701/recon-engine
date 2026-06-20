from utils.logger import get_logger

logger = get_logger("normalizer")

def normalize_transactions(transactions):
    logger.info("Normalizing transactions")
    normalized = []

    for txn in transactions:
        normalized_txn = {
            "txn_id": str(txn.get("txn_id", "")).strip(),
            "date": str(txn.get("date", "")).strip()[:10],
            "amount": round(float(txn.get("amount", 0.0)), 2),
            "currency": str(txn.get("currency", "INR")).upper().strip(),
            "sender": str(txn.get("sender", "")).strip().upper(),
            "receiver": str(txn.get("receiver", "")).strip().upper(),
            "reference": str(txn.get("reference", "")).strip().upper(),
            "bank": str(txn.get("bank", "UNKNOWN")).strip().upper(),
            "channel": str(txn.get("channel", "UNKNOWN")).strip().upper(),
            "source_format": str(txn.get("source_format", "UNKNOWN")).strip().upper()
        }
        normalized.append(normalized_txn)

    logger.info(f"Normalized {len(normalized)} transactions")
    return normalized