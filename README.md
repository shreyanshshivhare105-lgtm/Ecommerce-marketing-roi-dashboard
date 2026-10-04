# 📊 Multi-Channel E-Commerce Marketing Analytics & Interactive ROI Dashboard

An end-to-end data engineering and marketing analytics project that builds a multi-table relational database in SQLite, executes advanced analytical SQL queries to evaluate performance across **Google Ads** and **Meta Ads**, and outputs an executive-level interactive dashboard in Microsoft Excel.

---

## 📌 Executive Summary & Key Business Insights

* **Total Marketing Budget:** ₹5,03,121.33
* **Total Revenue Generated:** ₹20,88,669.44
* **Overall Portfolio ROAS:** **4.15x** (₹4.15 returned for every ₹1.00 spent)
* **Total Customer Conversions:** 568 paying customers across 2,000 tracked leads.

### 🏆 Campaign Performance Highlights
1. **Top ROI Efficiency Winner:** `Google_Search_EthnicWear` achieved the highest return with an **8.88x ROAS** (₹6.45L revenue on ₹72.6K spend) and the lowest Customer Acquisition Cost (**CAC: ₹854.28**).
2. **Top Volume Driver:** `Meta_Reels_FestiveCollec` generated the highest lead volume (**465 leads**) and **₹5.77L revenue** at a **5.58x ROAS**.
3. **Underperforming Campaign:** `Meta_Carousel_WesternWear` recorded the lowest efficiency (**1.86x ROAS**) and highest acquisition cost (**CAC: ₹1,598.57**), signaling a need for creative optimization.

---

## 🛠️ Data Pipeline Architecture & Tech Stack
[ Raw Multi-Channel CSVs ]
│
▼
[ SQLite Database Seeding ]  ──> (schema.sql & Python Automation)
│
▼
[ Complex SQL Analytical Queries ] ──> (Multi-Table JOINs, CTEs & Aggregations)
│
▼
[ Automated Excel Dashboard Export ] ──> (OpenPyXL Formatting, Slicers & Charts)

* **Database & SQL:** SQLite3 (`Campaign`, `ad_performance`, `customer_leads` tables)
* **Programming & Automation:** Python 3.x (`pandas`, `sqlite3`, `openpyxl`)
* **Visualization & Reporting:** Microsoft Excel (PivotTables, Slicers, Gradient Data Bars, Bar/Column Charts)

---

## 🗄️ Relational Database Schema

* **`Campaign`**: Master table storing campaign names, target audiences, and ad categories.
* **`ad_performance`**: Daily tracking table logging ad spend, impressions, and click-through metrics.
* **`customer_leads`**: Granular log of 2,000 customer interactions, conversion statuses, and order values.

---

## 🔍 Key Analytical SQL Query

```sql
WITH DailySpend AS (
    SELECT Campaign_id, SUM(ad_spent_inr) AS total_spend_inr 
    FROM ad_performance 
    GROUP BY Campaign_id
),
LeadConversions AS (
    SELECT 
        Campaign_id, 
        COUNT(lead_id) AS total_leads,
        SUM(CASE WHEN is_converted = 1 THEN 1 ELSE 0 END) AS total_conversions,
        SUM(CASE WHEN is_converted = 1 AND customer_is_new = 1 THEN 1 ELSE 0 END) AS new_customers,
        SUM(order_value_inr) AS total_revenue_inr
    FROM customer_leads 
    GROUP BY Campaign_id
)
SELECT 
    c.channel_ AS Channel,
    c.Campaign_name AS Campaign_Name,
    c.ad_type AS Ad_Type,
    ROUND(s.total_spend_inr, 2) AS Ad_Spend_INR,
    ROUND(l.total_revenue_inr, 2) AS Revenue_INR,
    l.total_leads AS Total_Leads,
    l.total_conversions AS Total_Conversions,
    ROUND((CAST(l.total_conversions AS FLOAT) / l.total_leads) * 100, 2) AS Conv_Rate_Pct,
    ROUND(s.total_spend_inr / NULLIF(l.new_customers, 0), 2) AS CAC_INR,
    ROUND(l.total_revenue_inr / NULLIF(s.total_spend_inr, 0), 2) AS ROAS
FROM Campaign c
JOIN DailySpend s ON c.Campaign_id = s.Campaign_id
JOIN LeadConversions l ON c.Campaign_id = l.Campaign_id
ORDER BY ROAS DESC;
