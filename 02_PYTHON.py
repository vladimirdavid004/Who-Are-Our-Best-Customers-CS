mport pandas as pd                                    # load pandas, nicknamed "pd" so we type less

# ---------- 1. LOAD THE DATA ----------
df = pd.read_excel("online_retail_II.xlsx", sheet_name=None)  # read EVERY sheet; sheet_name=None gives back a dictionary {sheet name: table}
df = pd.concat(df.values(), ignore_index=True)        # stack the two year sheets into one table; ignore_index renumbers rows 0, 1, 2...

# ---------- 2. CLEAN ----------
df = df.dropna(subset=["Customer ID"])                 # drop rows with no Customer ID (can't score a customer we can't identify)
df = df[~df["Invoice"].astype(str).str.startswith("C")]  # drop cancellations: invoices starting with "C"; ~ means NOT
df = df[(df["Quantity"] > 0) & (df["Price"] > 0)]     # keep rows where quantity AND price are above zero (& means AND)
df["Revenue"] = df["Quantity"] * df["Price"]          # new column: money from each line = units x unit price

# ---------- 3. BUILD THE RFM TABLE (one row per customer) ----------
snapshot = df["InvoiceDate"].max() + pd.Timedelta(days=1)  # "today" for the analysis = day after the last sale in the data
rfm = df.groupby("Customer ID").agg(                   # group all rows by customer, then calculate 3 numbers for each one:
    recency=("InvoiceDate", lambda d: (snapshot - d.max()).days),  # Recency: days from their LAST purchase to snapshot (smaller = better)
    frequency=("Invoice", "nunique"),                  # Frequency: count of DIFFERENT invoices = number of orders placed
    monetary=("Revenue", "sum"),                       # Monetary: total amount they spent
)

# ---------- 4. SCORE EACH CUSTOMER 1-5 (5 = best) ----------
rfm["R"] = pd.qcut(rfm["recency"], 5, labels=[5, 4, 3, 2, 1]).astype(int)  # split into 5 equal-size groups; labels reversed because FEWER days is better
rfm["F"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)  # rank first so ties (lots of 1-order customers) don't break qcut
rfm["M"] = pd.qcut(rfm["monetary"], 5, labels=[1, 2, 3, 4, 5]).astype(int)  # top 20% of spenders get 5, bottom 20% get 1
