# RFM Customer Segmentation - UK Online Retailer
# Data: Online Retail II, UCI Machine Learning Repository (CC BY 4.0)
#
# How to run:
#   Terminal:  python3 rfm_analysis.py
#   VS Code:   each "# %%" line starts a cell you can run on its own (click "Run Cell")
#
# Needs: pip3 install pandas openpyxl


# %% ---------- 0. SETUP ----------
import os                                              # tools for working with folders
import pandas as pd                                    # load pandas, nicknamed "pd" so we type less

FOLDER = "~/Downloads"                                 # CHANGE THIS to the folder holding the Excel file (~ = your home folder)
os.chdir(os.path.expanduser(FOLDER))                   # make that folder the working folder; expanduser turns ~ into /Users/yourname

pd.set_option("display.float_format", "{:,.0f}".format)  # show 12,293,140 instead of 1.229314e+07


# %% ---------- 1. LOAD THE DATA ----------
sheets = pd.read_excel("online_retail_II.xlsx", sheet_name=None)  # read EVERY sheet; gives back a dictionary {sheet name: table}
df = pd.concat(sheets.values(), ignore_index=True)    # stack the two year sheets into one table; ignore_index renumbers rows 0, 1, 2...
print("Rows loaded:", len(df))                         # sanity check: should be about 1,067,371


# %% ---------- 2. CLEAN ----------
df = df.dropna(subset=["Customer ID"])                 # drop rows with no Customer ID (can't score a customer we can't identify)
df = df[~df["Invoice"].astype(str).str.startswith("C")]  # drop cancellations: invoices starting with "C"; ~ means NOT
df = df[(df["Quantity"] > 0) & (df["Price"] > 0)]      # keep rows where quantity AND price are above zero (& means AND)
df["Revenue"] = df["Quantity"] * df["Price"]           # new column: money from each line = units x unit price
print("Rows after cleaning:", len(df))                 # how many usable sales rows are left


# %% ---------- 3. BUILD THE RFM TABLE (one row per customer) ----------
snapshot = df["InvoiceDate"].max() + pd.Timedelta(days=1)  # "today" for the analysis = day after the last sale in the data

rfm = df.groupby("Customer ID").agg(                   # group all rows by customer, then calculate 3 numbers for each one:
    recency=("InvoiceDate", lambda d: (snapshot - d.max()).days),  # Recency: days from their LAST purchase to snapshot (smaller = better)
    frequency=("Invoice", "nunique"),                  # Frequency: count of DIFFERENT invoices = number of orders placed
    monetary=("Revenue", "sum"),                       # Monetary: total amount they spent
)


# %% ---------- 4. SCORE EACH CUSTOMER 1-5 (5 = best) ----------
rfm["R"] = pd.qcut(rfm["recency"], 5, labels=[5, 4, 3, 2, 1]).astype(int)  # 5 equal-size groups; labels reversed because FEWER days is better
rfm["F"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)  # rank first so ties don't break qcut
rfm["M"] = pd.qcut(rfm["monetary"], 5, labels=[1, 2, 3, 4, 5]).astype(int)  # top 20% of spenders get 5, bottom 20% get 1

print("\nFirst 10 customers:")
print(rfm.head(10))                                    # peek at the scored table


# %% ---------- 5. NAME THE SEGMENTS ----------
def segment(row):                                      # a mini-machine: takes ONE customer row, returns a segment name
    if row["R"] >= 4 and row["F"] >= 4:                # bought recently AND buys often
        return "Champions"
    elif row["R"] >= 3 and row["F"] >= 3:              # fairly recent and fairly frequent
        return "Loyal"
    elif row["R"] <= 2 and row["F"] >= 3:              # used to buy often, but not lately
        return "At Risk"
    elif row["R"] >= 4:                                # bought recently, but only 1-2 orders so far
        return "New"
    else:                                              # hasn't bought in a while and rarely did
        return "Lost"

rfm["Segment"] = rfm.apply(segment, axis=1)            # run segment() on every customer; axis=1 means "go row by row"


# %% ---------- 6. SEGMENT SUMMARY ----------
summary = rfm.groupby("Segment").agg(                  # one row per segment:
    customers=("monetary", "count"),                   # how many customers are in it
    revenue=("monetary", "sum"),                       # how much they spent in total
)
summary["pct_revenue"] = (100 * summary["revenue"] / summary["revenue"].sum()).round(1)  # each segment's share of all revenue
summary = summary.sort_values("revenue", ascending=False)  # biggest segment first

print("\nSegment summary:")
print(summary.to_string(formatters={"pct_revenue": "{:.1f}%".format}))  # show the table; pct column with 1 decimal and a % sign


# %% ---------- 7. TOP 20% OF CUSTOMERS ----------
top = rfm["monetary"].sort_values(ascending=False)    # every customer's spend, biggest first
top_20_count = int(len(top) * 0.2)                    # how many customers make up the top 20%
top_20_share = 100 * top.head(top_20_count).sum() / top.sum()  # their spend divided by everyone's spend
print(f"\nTop 20% of customers drive {top_20_share:.1f}% of revenue")  # f-string: drops the number into the sentence


# %% ---------- 8. REVENUE BY MONTH ----------
monthly = df.groupby(df["InvoiceDate"].dt.to_period("M"))["Revenue"].sum()  # turn each date into its month, then total revenue per month
print("\nTop 3 months:")
print(monthly.sort_values(ascending=False).head(3))   # the 3 biggest months


# %% ---------- 9. SAVE RESULTS (for Excel and Tableau) ----------
rfm.to_csv("rfm_customers.csv")                       # every customer with scores and segment
summary.to_csv("segment_summary.csv")                 # the 5-row segment table
monthly.to_csv("monthly_revenue.csv")                 # revenue for each month
print("\nSaved 3 CSV files to:", os.getcwd())         # tells you exactly which folder they went to
