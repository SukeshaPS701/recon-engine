from parsers.csv_parser import parse_csv
from parsers.mt940_parser import parse_mt940
from parsers.camt053_parser import parse_camt053

from core.normalizer import normalize_transactions
from core.reconciler import reconcile
from core.multi_reconciler import reconcile_multi_source

from reports.report_generator import generate_report
from reports.multi_report_generator import generate_multi_report

from utils.logger import get_logger

logger = get_logger("main")


def main():
    logger.info("Starting Automated Reconciliation Engine")

    csv_file = "data/input/bank_a.csv"
    mt940_file = "data/input/bank_b.mt940"
    camt053_file = "data/input/bank_c.xml"

    csv_transactions = normalize_transactions(parse_csv(csv_file))
    mt940_transactions = normalize_transactions(parse_mt940(mt940_file))
    camt053_transactions = normalize_transactions(parse_camt053(camt053_file))

    print("\nLoaded Transactions Summary")
    print("-" * 40)
    print(f"CSV      : {len(csv_transactions)}")
    print(f"MT940    : {len(mt940_transactions)}")
    print(f"CAMT053  : {len(camt053_transactions)}")

    # -----------------------------
    # Pairwise reconciliation runs
    # -----------------------------
    print("\n\n### RECONCILIATION RUN 1: CSV vs MT940 ###")
    result_csv_mt940 = reconcile(
        csv_transactions,
        mt940_transactions,
        left_name="BANK_A_CSV",
        right_name="BANK_B_MT940"
    )
    generate_report(result_csv_mt940)

    print("\n\n### RECONCILIATION RUN 2: CSV vs CAMT053 ###")
    result_csv_camt = reconcile(
        csv_transactions,
        camt053_transactions,
        left_name="BANK_A_CSV",
        right_name="BANK_C_CAMT053"
    )
    generate_report(result_csv_camt)

    print("\n\n### RECONCILIATION RUN 3: MT940 vs CAMT053 ###")
    result_mt940_camt = reconcile(
        mt940_transactions,
        camt053_transactions,
        left_name="BANK_B_MT940",
        right_name="BANK_C_CAMT053"
    )
    generate_report(result_mt940_camt)

    # -----------------------------
    # Multi-source reconciliation
    # -----------------------------
    print("\n\n### MULTI-SOURCE RECONCILIATION: CSV + MT940 + CAMT053 ###")
    multi_rows = reconcile_multi_source(
        csv_transactions,
        mt940_transactions,
        camt053_transactions
    )
    generate_multi_report(multi_rows)


if __name__ == "__main__":
    main()