import os
import pandas as pd
from tabulate import tabulate
from utils.logger import get_logger

logger = get_logger("multi_report_generator")


def generate_multi_report(rows, output_dir="data/processed"):
    os.makedirs(output_dir, exist_ok=True)

    df = pd.DataFrame(rows)

    print("\n" + "=" * 95)
    print("                    MULTI-SOURCE RECONCILIATION REPORT")
    print("=" * 95)

    if not df.empty:
        preview_cols = [
            "group_key",
            "csv_txn_id",
            "mt940_txn_id",
            "camt053_txn_id",
            "csv_amount",
            "mt940_amount",
            "camt053_amount",
            "final_status",
            "exception_reason"
        ]
        preview_cols = [c for c in preview_cols if c in df.columns]
        print(tabulate(df[preview_cols], headers="keys", tablefmt="grid", showindex=False))

    # dashboard summary
    status_counts = (
        df["final_status"].value_counts(dropna=False).reset_index()
        .rename(columns={"index": "final_status", "final_status": "count"})
    ) if not df.empty else pd.DataFrame(columns=["final_status", "count"])

    # presence matrix
    presence_rows = []
    for _, row in df.iterrows():
        presence_rows.append({
            "group_key": row["group_key"],
            "present_in_csv": 1 if row["csv_txn_id"] else 0,
            "present_in_mt940": 1 if row["mt940_txn_id"] else 0,
            "present_in_camt053": 1 if row["camt053_txn_id"] else 0,
            "final_status": row["final_status"]
        })

    presence_df = pd.DataFrame(presence_rows)

    multi_report_path = os.path.join(output_dir, "multi_reconciliation_report.csv")
    dashboard_path = os.path.join(output_dir, "reconciliation_dashboard_summary.csv")
    presence_path = os.path.join(output_dir, "bank_presence_matrix.csv")

    df.to_csv(multi_report_path, index=False)
    status_counts.to_csv(dashboard_path, index=False)
    presence_df.to_csv(presence_path, index=False)

    logger.info(f"Saved multi reconciliation report to {multi_report_path}")
    logger.info(f"Saved dashboard summary to {dashboard_path}")
    logger.info(f"Saved bank presence matrix to {presence_path}")