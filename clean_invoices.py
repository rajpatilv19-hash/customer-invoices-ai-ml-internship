
import pandas as pd
import os

# File paths
input_file = r"C:\Users\rajpa\train_invoices.csv"
output_file = r"C:\Users\rajpa\Internship Project 1\cleaned_customer_invoices.csv"
log_file = r"C:\Users\rajpa\Internship Project 1\customer_invoices_cleaning_log.csv"

print("Starting invoice data cleaning...")

# Load original dataset
print("Loading original dataset...")

df = pd.read_csv(input_file)

print("Dataset loaded successfully!")
print("Original dataset shape:", df.shape)

# Standardize column names
df.columns = (
    df.columns.str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# Remove leading and trailing spaces from text columns
text_columns = df.select_dtypes(include="object").columns

for col in text_columns:
    df[col] = df[col].str.strip()

print("Column names and text values standardized.")

# Standardize categorical columns
df["payment_status"] = df["payment_status"].str.title()

df["currency"] = df["currency"].str.upper()

category_columns = [
    "payment_method",
    "customer_country",
    "product_category",
    "order_channel"
]

for col in category_columns:
    df[col] = df[col].str.title()

# Correct UPI capitalization
df["payment_method"] = df["payment_method"].replace({
    "Upi": "UPI"
})

print("Categorical values standardized.")

# Convert date columns to datetime
date_columns = [
    "invoice_date",
    "due_date",
    "payment_date"
]

for col in date_columns:
    df[col] = pd.to_datetime(df[col], errors="coerce")

print("Date columns converted to datetime.")

# Preserve original payment dates
df["original_payment_date"] = df["payment_date"].copy()

# Keep confirmed payment dates only for Paid invoices
paid_mask = df["payment_status"] == "Paid"

df["payment_date"] = df["payment_date"].where(paid_mask)

print("Original payment dates preserved.")
print("Non-paid payment dates masked.")

# Feature Engineering

# 1. Calculate days taken to pay
df["days_to_pay"] = (
    df["payment_date"] - df["invoice_date"]
).dt.days

# 2. Calculate payment delay
df["delay"] = (
    df["payment_date"] - df["due_date"]
).dt.days

# 3. Identify late payments
df["paid_late"] = pd.Series(
    pd.NA, index=df.index, dtype="boolean"
)

paid_mask = df["payment_status"] == "Paid"

df.loc[paid_mask, "paid_late"] = (
    df.loc[paid_mask, "delay"] > 0
)

# 4. Classify invoice state
df["open_paid_flag"] = df["payment_status"].map({
    "Paid": "Paid",
    "Pending": "Open",
    "Overdue": "Open",
    "Cancelled": "Cancelled"
})

print("Feature engineering completed!")

# Data Validation

print("\\nStarting validation...")

print("Total records:", len(df))

print("\\nDuplicate invoice IDs:",
      df["invoice_id"].duplicated().sum())

print("\\nMissing values in new columns:")
print(df[[
    "days_to_pay",
    "delay",
    "paid_late",
    "open_paid_flag"
]].isnull().sum())

print("\\nNegative days to pay:",
      (df["days_to_pay"] < 0).sum())

print("Positive payment delays:",
      (df["delay"] > 0).sum())

print("\\nInvoice state distribution:")
print(df["open_paid_flag"].value_counts())

print("\\nValidation completed!")

# Save cleaned dataset
print("\\nSaving cleaned dataset...")

df.to_csv(output_file, index=False)

print("Cleaned dataset saved:", output_file)

# Create cleaning log
cleaning_log = [
    {
        "Issue": "Missing values",
        "Finding": "No initial missing values",
        "Action": "No changes required"
    },
    {
        "Issue": "Duplicate invoice IDs",
        "Finding": "0 duplicates",
        "Action": "No changes required"
    },
    {
        "Issue": "Duplicate invoice numbers",
        "Finding": "0 duplicates",
        "Action": "No changes required"
    },
    {
        "Issue": "Date validation",
        "Finding": "No invalid dates or due dates before invoice dates",
        "Action": "Converted dates to datetime"
    },
    {
        "Issue": "Invalid numerical values",
        "Finding": "No invalid values found",
        "Action": "No changes required"
    },
    {
        "Issue": "Text standardization",
        "Finding": "Whitespace and capitalization standardized",
        "Action": "Cleaned text and categories"
    },
    {
        "Issue": "UPI capitalization",
        "Finding": "UPI standardized",
        "Action": "Corrected capitalization"
    },
    {
    ,
    {
        "Issue": "Feature engineering",
        "Finding": "Four analytical columns created",
        "Action": "Created days_to_pay, delay, paid_late and open_paid_flag"
    }
]

cleaning_log_df = pd.DataFrame(cleaning_log)

cleaning_log_df.to_csv(log_file, index=False)

print("Cleaning log saved:", log_file)

print("\\nAll cleaning operations completed!")
