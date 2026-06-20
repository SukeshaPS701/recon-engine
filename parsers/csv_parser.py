import pandas as pd
from utils.logger import get_logger

logger = get_logger("csv_parser")

def parse_csv(file_path):
    logger.info(f"Reading CSV file: {file_path}")

    df = pd.read_csv(file_path)
    transactions = []

    for _, row in df.iterrows():
        txn = {
            "txn_id": str(row.get("txn_id", "")).strip(),
            "date": str(row.get("date", "")).strip(),
            "amount": float(row.get("amount", 0)),
            "currency": str(row.get("currency", "INR")).strip(),
            "sender": str(row.get("sender", "")).strip(),
            "receiver": str(row.get("receiver", "")).strip(),
            "reference": str(row.get("reference", "")).strip(),
            "bank": str(row.get("bank", "UNKNOWN")).strip(),
            "channel": str(row.get("channel", "UNKNOWN")).strip(),
            "source_format": "CSV"
        }
        transactions.append(txn)

    logger.info(f"Parsed {len(transactions)} CSV transactions")
    return transactions