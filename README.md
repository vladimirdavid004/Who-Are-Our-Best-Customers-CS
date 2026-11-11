# Case-Study-2-Who-Are-Our-Best-Customers

Case Study 2: Who Are Our Best Customers?

Subtitle: RFM customer segmentation for a UK online gift retailer

Business problem
An online gift-ware company sends the same marketing to every customer. It wants to know who its most valuable customers are, who is about to stop buying, and where to focus retention spend.

Questions
1. How do customers split into segments like Champions, Loyal, At Risk and Lost?
2. What share of revenue comes from the top 20% of customers?
3. Which segment is the biggest retention opportunity?
4. How do monthly revenue and active customers trend, and is there a holiday spike?

Approach
1. Clean (Python/pandas): drop rows with no Customer ID, remove cancellations and negative quantities, add a Revenue column (Quantity × Price).
2. RFM scores: for each customer, calculate Recency (days since last purchase), Frequency (number of invoices) and Monetary (total spend). Score each 1–5 by quintile.
3. Segments: map score combinations to named groups (for example R5-F5 = Champions, R1-F4 or higher = At Risk).
4. Revenue concentration: sort customers by spend and find the top 20% share.
5. Dashboard: Tableau Public with segment sizes, revenue by segment, and a monthly trend line.

Findings (fill in after you run it)
• Customers analyzed: ___
• Top 20% of customers drive ___% of revenue
• Champions: ___ customers, ___% of revenue
• At Risk: ___ customers worth £___ in past spend
• Peak month: ___

Recommendations (fill in)
1. Champions (recent, frequent, big spenders): reward and protect them. Give them a VIP tier with early access to new products, free shipping and a dedicated contact. Goal: keep them buying, not discount them. They already spend the most, so perks beat price cuts.
2. Loyal customers: grow them into Champions. Send personalized "you might also like" offers based on what they already buy, plus a volume bonus for larger orders (useful since many customers are wholesalers).
3. At Risk (used to buy often, haven't lately): win them back first. This is the biggest opportunity. Send a win-back email series with a time-limited offer, and have someone reach out personally to the highest-spending ones to ask why they stopped.
4. Lost customers: spend as little as possible. One low-cost reactivation email, then drop them from paid campaigns so the marketing budget goes to segments that respond.

Estimated impact: At Risk customers spent £___ in total. Winning back even 10% of that is worth about £___ in revenue. (Fill in after you run the RFM analysis.)

Why this one fits you
It's the same idea as protecting your best accounts and catching customers before they churn, which you dealt with daily in wireless. RFM is also a classic interview topic for analyst roles.
