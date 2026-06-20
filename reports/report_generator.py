import os
import pandas as pd
from tabulate import tabulate
from utils.logger import get_logger

logger = get_logger("report_generator")


def generate_report(result, output_dir="data/processed"):
    os.makedirs(output_dir, exist_ok=True)

    print("\n" + "=" * 80)
    print("                 AUTOMATED RECONCILIATION REPORT")
    print("=" * 80)
    print(f"Comparison      : {result['left_name']} vs {result['right_name']}")
    print(f"Matched         : {result['matched_count']}")
    print(f"Unmatched Left  : {result['unmatched_left_count']}")
    print(f"Unmatched Right : {result['unmatched_right_count']}")
    print(f"Exceptions      : {len(result['exceptions'])}")
    print("=" * 80)

    # Show matched summary
    if result["matched_transactions"]:
        matched_preview = []
        for pair in result["matched_transactions"]:
            matched_preview.append({
                "left_txn_id": pair["left"]["txn_id"],
                "right_txn_id": pair["right"]["txn_id"],
                "amount": pair["left"]["amount"],
                "date": pair["left"]["date"],
                "reference": pair["left"]["reference"],
                "match_type": pair["match_type"]
            })

        print("\nMatched Transactions:")
        print(tabulate(matched_preview, headers="keys", tablefmt="grid"))

    if result["exceptions"]:
        print("\nExceptions:")
        print(tabulate(result["exceptions"], headers="keys", tablefmt="grid"))

    matched_rows = []
    for pair in result["matched_transactions"]:
        matched_rows.append({
            "left_txn_id": pair["left"]["txn_id"],
            "right_txn_id": pair["right"]["txn_id"],
            "amount": pair["left"]["amount"],
            "date": pair["left"]["date"],
            "reference": pair["left"]["reference"],
            "left_bank": pair["left"]["bank"],
            "right_bank": pair["right"]["bank"],
            "match_type": pair["match_type"]
        })

    matched_df = pd.DataFrame(matched_rows)
    exceptions_df = pd.DataFrame(result["exceptions"])

    summary_df = pd.DataFrame([{
        "left_name": result["left_name"],
        "right_name": result["right_name"],
        "matched_count": result["matched_count"],
        "unmatched_left_count": result["unmatched_left_count"],
        "unmatched_right_count": result["unmatched_right_count"],
        "exception_count": len(result["exceptions"])
    }])

    matched_path = os.path.join(output_dir, "matched_transactions.csv")
    exceptions_path = os.path.join(output_dir, "exceptions_report.csv")
    summary_path = os.path.join(output_dir, "reconciliation_summary.csv")

    matched_df.to_csv(matched_path, index=False)
    exceptions_df.to_csv(exceptions_path, index=False)
    summary_df.to_csv(summary_path, index=False)

    logger.info(f"Saved matched report to {matched_path}")
    logger.info(f"Saved exceptions report to {exceptions_path}")
    logger.info(f"Saved summary report to {summary_path}")