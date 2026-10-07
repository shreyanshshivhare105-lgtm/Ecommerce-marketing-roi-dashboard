import sqlite3
import pandas as pd

def analyze_marketing_performance():
    # 1. Connect to your database
    conn = sqlite3.connect("clothing_marketing_analytics.db")

    # 2. Write Multi-Table SQL JOIN Query
    sql_query = """
    WITH DailySpend AS (
        SELECT 
            Campaign_id,
            SUM(ad_spent_inr) AS total_spend_inr
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
        ROUND((CAST(l.total_conversions AS FLOAT) / l.total_leads) * 100, 2) || '%' AS Conv_Rate,
        ROUND(s.total_spend_inr / NULLIF(l.new_customers, 0), 2) AS CAC_INR,
        ROUND(l.total_revenue_inr / NULLIF(s.total_spend_inr, 0), 2) AS ROAS
    FROM Campaign c
    JOIN DailySpend s ON c.Campaign_id = s.Campaign_id
    JOIN LeadConversions l ON c.Campaign_id = l.Campaign_id
    ORDER BY ROAS DESC;
    """

    # 3. Execute query and fetch results as a pandas DataFrame
    df_results = pd.read_sql_query(sql_query, conn)
    conn.close()

    print("\n=================== CAMPAIGN PERFORMANCE REPORT ===================")
    print(df_results.to_string(index=False))
    print("===================================================================\n")

if __name__ == "__main__":
    analyze_marketing_performance()