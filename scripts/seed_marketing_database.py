import sqlite3
import pandas as pd

def seed_marketing_database():
    # 1. Connect / Create the SQLite Database File
    conn = sqlite3.connect("clothing_marketing_analytics.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    print("Reading schema from 'Sales Table  Attribute.sql'...")

    # 2. Read and execute table creation from your SQL file
    with open("Sales Table  Attribute.sql", "r") as sql_file:
        sql_script = sql_file.read()

    # Exclude CREATE DATABASE command (SQLite creates the .db file automatically)
    clean_script = "\n".join([line for line in sql_script.split("\n") if "CREATE DATABASE" not in line.upper()])
    cursor.executescript(clean_script)
    conn.commit()

    print("Loading CSV files...")

    # 3. Read raw CSV files from your directory
    df_campaigns = pd.read_csv("campaigns.csv")
    df_ad_perf = pd.read_csv("ad_performance.csv")
    df_leads = pd.read_csv("customer_leads_2000.csv")

    # 4. Map CSV column names to match the columns defined in 'Sales Table  Attribute.sql'
    df_campaigns = df_campaigns.rename(columns={"channel": "channel_"})
    df_ad_perf = df_ad_perf.rename(columns={
        "spend_date": "spent_date", 
        "ad_spend_inr": "ad_spent_inr",
        "impressions": "imperssions"
    })
    df_leads = df_leads.rename(columns={
        "channel": "channel_", 
        "is_new_customer": "customer_is_new"
    })

    # 5. Insert data into SQL tables
    df_campaigns.to_sql("Campaign", conn, if_exists="append", index=False)
    df_ad_perf.to_sql("ad_performance", conn, if_exists="append", index=False)
    df_leads.to_sql("customer_leads", conn, if_exists="append", index=False)

    print("\nDatabase created and seeded successfully!")

    # 6. Verify row counts inside 'clothing_marketing_analytics.db'
    for table in ["Campaign", "ad_performance", "customer_leads"]:
        count = cursor.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"Table '{table}': {count} total rows inserted.")

    conn.close()

if __name__ == "__main__":
    seed_marketing_database()