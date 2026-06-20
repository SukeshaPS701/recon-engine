# Automated Reconciliation Engine – Multi Bank Settlement

## Project Overview
This project implements an **Automated Reconciliation Engine** for **multi-bank settlement systems** using simulated financial transaction data. The engine is designed to ingest transaction statements from multiple banking formats, normalize them into a unified internal schema, perform transaction matching using deterministic and fuzzy rules, and generate reconciliation and exception reports.

The project simulates reconciliation workflows across multiple banking/payment channels such as:

- **UPI**
- **NEFT**
- **RTGS**
- **Card / network settlement**

Supported input statement formats include:

- **Bank-specific CSV files**
- **MT940 bank statement format**
- **ISO 20022 CAMT.053 XML statement format**

The objective is to automate the reconciliation of high-volume transaction data across heterogeneous bank sources and identify matched, partially matched, and unmatched settlement records.

---

## Problem Statement
Financial institutions and payment systems receive transaction data from multiple banks and settlement partners in different formats. Reconciling these transactions manually is slow, error-prone, and operationally expensive. A scalable reconciliation engine must be able to:

- ingest data from different banking formats,
- normalize transaction fields into a common structure,
- compare transactions across multiple banks,
- identify exact and near matches,
- detect missing / unmatched / partially matched records,
- generate exception reports for investigation.

This project builds a prototype reconciliation engine to address these challenges.

---

## Objectives
The key objectives of this project are:

1. Build a modular reconciliation engine capable of handling multiple input formats.
2. Parse and ingest **CSV**, **MT940**, and **CAMT.053 XML** transaction files.
3. Normalize transactions into a common schema for downstream processing.
4. Implement transaction matching logic using:
   - exact matching
   - fuzzy reference matching
   - tolerance-based amount matching
5. Perform reconciliation across multiple bank sources.
6. Generate:
   - matched transaction reports
   - exception reports
   - reconciliation summaries
   - multi-source presence reports

---

## Key Features
- **Multi-format ingestion**
  - CSV parser
  - MT940 parser
  - CAMT.053 XML parser

- **Transaction normalization**
  - standard field mapping
  - uppercase reference / sender / receiver normalization
  - standardized date and amount formatting

- **Reconciliation logic**
  - exact match based on amount + date + reference
  - fuzzy reference match
  - amount tolerance-based match

- **Pairwise reconciliation**
  - CSV vs MT940
  - CSV vs CAMT.053
  - MT940 vs CAMT.053

- **Multi-source reconciliation**
  - unified reconciliation table across all sources
  - source presence matrix
  - full / partial / unmatched classification

- **Exception reporting**
  - missing in left source
  - missing in right source
  - partial match
  - unmatched records

- **Report generation**
  - CSV outputs for matched records
  - exception report CSV
  - reconciliation summary CSV
  - multi-source reconciliation report

---

## Technology Stack
- **Python**
- **pandas** – tabular data processing
- **xml.etree.ElementTree** – XML parsing
- **tabulate** – console report formatting
- **logging** – execution logging / audit trail

---

## Project Architecture

### 1. Ingestion Layer
The ingestion layer reads transaction files from multiple sources and formats.

**Supported parsers:**
- `csv_parser.py`
- `mt940_parser.py`
- `camt053_parser.py`

Each parser converts source-specific records into Python dictionaries.

---

### 2. Normalization Layer
The normalization layer transforms parsed transactions into a **common internal schema** so that matching rules can be applied consistently across all sources.

**Normalized transaction schema:**
- `txn_id`
- `date`
- `amount`
- `currency`
- `sender`
- `receiver`
- `reference`
- `bank`
- `channel`
- `source_format`

---

### 3. Matching Engine
The matching engine compares transactions across sources using deterministic and fuzzy rules.

**Matching hierarchy:**
1. **EXACT**
   - same amount
   - same date
   - same reference

2. **FUZZY_REFERENCE**
   - same amount
   - same date
   - similar reference string

3. **AMOUNT_TOLERANCE**
   - same date
   - same reference
   - amount difference within configured tolerance

---

### 4. Reconciliation Layer
The reconciliation layer produces:

- matched transactions
- unmatched left-side transactions
- unmatched right-side transactions
- classified exceptions

It supports:
- **pairwise reconciliation**
- **multi-source reconciliation**

---

### 5. Reporting Layer
The reporting layer exports reconciliation results into structured CSV files for downstream review and audit.

Generated outputs include:
- matched transactions report
- exception report
- reconciliation summary
- multi-source reconciliation report
- bank presence matrix

---

## Folder Structure

```text
recon-engine/
│
├── core/
│   ├── matcher.py
│   ├── multi_reconciler.py
│   ├── normalizer.py
│   └── reconciler.py
│
├── data/
│   ├── input/
│   │   ├── bank_a.csv
│   │   ├── bank_b.mt940
│   │   └── bank_c.xml
│   │
│   └── processed/
│       ├── matched_transactions.csv
│       ├── exceptions_report.csv
│       ├── reconciliation_summary.csv
│       ├── multi_reconciliation_report.csv
│       ├── reconciliation_dashboard_summary.csv
│       └── bank_presence_matrix.csv
│
├── logs/
│   └── recon_engine.log
│
├── parsers/
│   ├── camt053_parser.py
│   ├── csv_parser.py
│   └── mt940_parser.py
│
├── reports/
│   ├── multi_report_generator.py
│   └── report_generator.py
│
├── utils/
│   └── logger.py
│
├── main.py
├── requirements.txt
└── README.md