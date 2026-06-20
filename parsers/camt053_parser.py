import xml.etree.ElementTree as ET
from utils.logger import get_logger

logger = get_logger("camt053_parser")

def parse_camt053(file_path):
    logger.info(f"Reading CAMT.053 file: {file_path}")

    tree = ET.parse(file_path)
    root = tree.getroot()

    transactions = []

    for entry in root.findall(".//transaction"):
        txn = {
            "txn_id": entry.findtext("txn_id", default="").strip(),
            "date": entry.findtext("date", default="").strip(),
            "amount": float(entry.findtext("amount", default="0")),
            "currency": entry.findtext("currency", default="INR").strip(),
            "sender": entry.findtext("sender", default="").strip(),
            "receiver": entry.findtext("receiver", default="").strip(),
            "reference": entry.findtext("reference", default="").strip(),
            "bank": entry.findtext("bank", default="UNKNOWN").strip(),
            "channel": entry.findtext("channel", default="UNKNOWN").strip(),
            "source_format": "CAMT053"
        }
        transactions.append(txn)

    logger.info(f"Parsed {len(transactions)} CAMT.053 transactions")
    return transactions