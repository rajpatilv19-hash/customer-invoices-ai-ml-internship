# Week 1 Summary – Customer Invoices Data Cleaning

**Internship:** 8-Week AI/ML Internship  
**Organization:** Orvians Technologies  
**Project:** Customer Invoices  
**Week:** 1

## 1. Objective

Prepare the Customer Invoices dataset for future analysis and machine-learning work by exploring its structure, checking data quality, standardizing fields, creating invoice-payment features, and saving a reusable cleaning pipeline.

## 2. Dataset overview

- **Source file:** `train_invoices.csv`
- **Original shape:** 2,500,000 rows × 31 columns
- **Cleaned shape:** 2,500,000 rows × 36 columns
- **New columns created:** `original_payment_date`, `days_to_pay`, `delay`, `paid_late`, and `open_paid_flag`
- **Cleaned output:** `cleaned_customer_invoices.csv`

The notebook reports no initial missing values, duplicate invoice IDs, duplicate invoice numbers, invalid invoice dates, due dates earlier than invoice dates, or invalid negative/zero invoice amounts under the checks performed.

## 3. Work completed

1. Loaded the source CSV with Pandas and inspected its shape, columns, and data types.
2. Standardized column names to lowercase with underscores and removed leading/trailing spaces from text values.
3. Standardized payment status, currency, payment method, customer country, product category, and order channel values. Corrected `Upi` to `UPI`.
4. Converted `invoice_date`, `due_date`, and `payment_date` to datetime values.
5. Preserved the source payment date in `original_payment_date`. For non-Paid invoices, `payment_date` was blanked; the notebook's final validation reports zero non-Paid invoices with a payment date and zero Paid invoices without a payment date.
6. Created the following derived columns:
   - `days_to_pay`: payment date minus invoice date.
   - `delay`: payment date minus due date.
   - `paid_late`: whether a Paid invoice's delay is greater than zero; non-Paid records remain unknown.
   - `open_paid_flag`: maps Paid to Paid, Pending/Overdue to Open, and Cancelled to Cancelled.
7. Saved the cleaned dataset and a cleaning log.
8. Created `clean_invoices.py`, checked its Python syntax, executed it, and validated the generated output by reading the cleaned CSV in chunks.

## 4. Data-quality and validation results

| Check | Result recorded in notebook |
|---|---:|
| Original records | 2,500,000 |
| Original columns | 31 |
| Cleaned columns | 36 |
| Initial missing values | 0 |
| Duplicate invoice IDs | 0 |
| Duplicate invoice numbers | 0 |
| Invalid invoice dates | 0 |
| Due dates before invoice dates | 0 |
| Negative or zero invoice amounts | 0 |
| Non-Paid records with source payment dates | 799,965 |
| Non-Paid records with payment dates after cleaning | 0 |
| Paid records without payment dates after cleaning | 0 |

### Invoice-state distribution

| Invoice state | Records |
|---|---:|
| Paid | 1,700,035 |
| Open | 675,304 |
| Cancelled | 124,661 |

The notebook's validation also reports zero negative `days_to_pay` values and zero positive `delay` values for the cleaned Paid records.

## 5. Cleaning decisions

- No rows were dropped for missing values or duplicate invoices because the checks reported none.
- Text and category values were standardized to make labels consistent.
- Date fields were parsed with `errors="coerce"` so unparseable values would become missing and could be checked.
- Original payment dates were retained in `original_payment_date`; `payment_date` was kept only for invoices marked Paid. This avoids treating dates on non-Paid records as confirmed payment dates.
- No capping or imputation was reported in the notebook because the stated checks did not identify values requiring those actions.

## 6. Tools and concepts used

- Python
- Pandas
- CSV input/output
- Data types and datetime conversion
- Missing-value and duplicate checks
- Text/category standardization
- Data validation
- Feature engineering
- Reusable Python scripts

## 7. What I learned

- How to load and inspect a large CSV dataset using Pandas.
- How to check common data-quality issues before analysis.
- How to standardize text, categories, and date columns.
- How to create payment-related features from invoice and payment dates.
- How to document cleaning decisions and validate saved output files.

## 8. Challenges and handling

- The dataset contains 2.5 million records, so the cleaned output is large. The notebook validated the final row count by reading the output in chunks rather than loading it all again at once.
- The source contained payment dates for 799,965 non-Paid records. The workflow preserved those source values separately and blanked the analytical `payment_date` for non-Paid records.
- The reusable script initially used machine-specific Windows file paths. These paths should be checked or made configurable before another person runs the script on a different computer.

## 9. Deliverables

- `Internship Project 1(1).ipynb` – notebook containing exploration, cleaning, feature engineering, and validation.
- `clean_invoices.py` – reusable cleaning script.
- `cleaned_customer_invoices.csv` – cleaned invoice dataset.
- `customer_invoices_cleaning_log.csv` – cleaning issues, actions, and results.
- `week1_data_dictionary.csv` – column names, data types, and meanings.
- `week1_column_mapping.csv` – mapping to the required project fields.

## 10. Before final submission

- Confirm that the mentor has approved the rule that `payment_date` is blank for non-Paid invoices while the original value is preserved in `original_payment_date`.
- Check that the paths in `clean_invoices.py` point to the correct input and output files on the machine where it will be run.
- Review the data dictionary descriptions against the source dataset's documentation.
- Do not upload real customer information to a public repository. Keep the repository private or use an approved anonymized sample if required.

---

**Week 1 outcome:** The notebook records a cleaned dataset with 2,500,000 rows and 36 columns, a cleaning log, derived payment features, and a reusable script that passed a syntax check and was executed for validation.
