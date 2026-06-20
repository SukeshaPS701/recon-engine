from utils.logger import get_logger

logger = get_logger("matcher")


def is_reference_similar(ref1, ref2):
    """
    Very simple fuzzy check:
    - exact match -> True
    - one reference contains the other -> True
    """
    ref1 = str(ref1).strip().upper()
    ref2 = str(ref2).strip().upper()

    if ref1 == ref2:
        return True

    if ref1 and ref2 and (ref1 in ref2 or ref2 in ref1):
        return True

    return False


def find_best_match(left_txn, candidate_transactions, amount_tolerance=1.0):
    """
    Match priority:
    1. EXACT -> amount + date + reference exact
    2. FUZZY_REFERENCE -> amount + date + similar reference
    3. AMOUNT_TOLERANCE -> date same + reference same + amount within tolerance
    """
    # 1) Exact match
    for right_txn in candidate_transactions:
        if (
            left_txn["amount"] == right_txn["amount"]
            and left_txn["date"] == right_txn["date"]
            and left_txn["reference"] == right_txn["reference"]
        ):
            return right_txn, "EXACT"

    # 2) Fuzzy reference match
    for right_txn in candidate_transactions:
        if (
            left_txn["amount"] == right_txn["amount"]
            and left_txn["date"] == right_txn["date"]
            and is_reference_similar(left_txn["reference"], right_txn["reference"])
        ):
            return right_txn, "FUZZY_REFERENCE"

    # 3) Amount tolerance match
    for right_txn in candidate_transactions:
        if (
            left_txn["date"] == right_txn["date"]
            and left_txn["reference"] == right_txn["reference"]
            and abs(left_txn["amount"] - right_txn["amount"]) <= amount_tolerance
        ):
            return right_txn, "AMOUNT_TOLERANCE"

    return None, None


def match_transactions(left_transactions, right_transactions, amount_tolerance=1.0):
    logger.info("Starting transaction matching")

    matched = []
    unmatched_left = []
    unmatched_right = right_transactions.copy()

    for left_txn in left_transactions:
        found_match, match_type = find_best_match(
            left_txn,
            unmatched_right,
            amount_tolerance=amount_tolerance
        )

        if found_match:
            matched.append({
                "left": left_txn,
                "right": found_match,
                "match_type": match_type
            })
            unmatched_right.remove(found_match)
        else:
            unmatched_left.append(left_txn)

    logger.info(
        f"Matching complete | matched={len(matched)} | "
        f"unmatched_left={len(unmatched_left)} | unmatched_right={len(unmatched_right)}"
    )

    return matched, unmatched_left, unmatched_right