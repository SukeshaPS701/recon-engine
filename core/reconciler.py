from core.matcher import match_transactions
from utils.logger import get_logger

logger = get_logger("reconciler")


def classify_exceptions(unmatched_left, unmatched_right):
    """
    Build exception records for reporting.
    """
    exceptions = []

    for txn in unmatched_left:
        exceptions.append({
            "side": "LEFT",
            "txn_id": txn["txn_id"],
            "date": txn["date"],
            "amount": txn["amount"],
            "reference": txn["reference"],
            "bank": txn["bank"],
            "channel": txn["channel"],
            "exception_type": "MISSING_IN_RIGHT"
        })

    for txn in unmatched_right:
        exceptions.append({
            "side": "RIGHT",
            "txn_id": txn["txn_id"],
            "date": txn["date"],
            "amount": txn["amount"],
            "reference": txn["reference"],
            "bank": txn["bank"],
            "channel": txn["channel"],
            "exception_type": "MISSING_IN_LEFT"
        })

    return exceptions


def reconcile(left_transactions, right_transactions, left_name="LEFT", right_name="RIGHT"):
    logger.info(f"Reconciling {left_name} vs {right_name}")

    matched, unmatched_left, unmatched_right = match_transactions(
        left_transactions, right_transactions
    )

    exceptions = classify_exceptions(unmatched_left, unmatched_right)

    result = {
        "left_name": left_name,
        "right_name": right_name,
        "matched_count": len(matched),
        "unmatched_left_count": len(unmatched_left),
        "unmatched_right_count": len(unmatched_right),
        "matched_transactions": matched,
        "unmatched_left": unmatched_left,
        "unmatched_right": unmatched_right,
        "exceptions": exceptions
    }

    logger.info("Reconciliation complete")
    return result