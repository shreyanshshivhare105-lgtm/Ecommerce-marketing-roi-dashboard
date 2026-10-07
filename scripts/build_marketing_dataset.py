import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Set seed for reproducible synthetic data
np.random.seed(42)
random.seed(42)

def generate_marketing_data():
    start_date = datetime(2026, 8, 1)
    num_leads = 2000

    # -------------------------------------------------------------
    # 1. TABLE 1: CAMPAIGNS (Master Dimension)
    # -------------------------------------------------------------
    campaigns = [
        {
            "campaign_id": "CMP_G_01",
            "campaign_name": "Google_Search_EthnicWear",
            "channel": "Google Ads",
            "ad_type": "Search",
            "category": "Ethnic Wear",
            "target_audience": "High Intent Search"
        },
        {
            "campaign_id": "CMP_G_02",
            "campaign_name": "Google_PMax_Menswear",
            "channel": "Google Ads",
            "ad_type": "Performance Max",
            "category": "Menswear",
            "target_audience": "Broad Prospecting"
        },
        {
            "campaign_id": "CMP_G_03",
            "campaign_name": "Google_Search_BrandName",
            "channel": "Google Ads",
            "ad_type": "Search",
            "category": "Brand",
            "target_audience": "High Intent Search"
        },
        {
            "campaign_id": "CMP_M_01",
            "campaign_name": "Meta_Reels_FestiveCollec",
            "channel": "Meta Ads",
            "ad_type": "Reels Video",
            "category": "Ethnic Wear",
            "target_audience": "Broad Prospecting"
        },
        {
            "campaign_id": "CMP_M_02",
            "campaign_name": "Meta_Carousel_WesternWear",
            "channel": "Meta Ads",
            "ad_type": "Carousel",
            "category": "Western Wear",
            "target_audience": "Broad Prospecting"
        },
        {
            "campaign_id": "CMP_M_03",
            "campaign_name": "Meta_Retargeting_AbandonedCart",
            "channel": "Meta Ads",
            "ad_type": "Static Image",
            "category": "All",
            "target_audience": "Retargeting"
        }
    ]
    df_campaigns = pd.DataFrame(campaigns)

    # -------------------------------------------------------------
    # 2. TABLE 2: AD PERFORMANCE (Daily Spend, Impressions, Clicks)
    # -------------------------------------------------------------
    ad_performance = []
    perf_id = 1
    
    # Generate 45 days of campaign spending logs
    for day_offset in range(45):
        current_date = (start_date + timedelta(days=day_offset)).strftime("%Y-%m-%d")
        
        for cmp in campaigns:
            if "Google" in cmp["channel"]:
                daily_spend = round(random.uniform(800, 2200), 2)
                impressions = random.randint(8000, 25000)
                clicks = int(impressions * random.uniform(0.035, 0.055)) # 3.5% - 5.5% CTR
            else: # Meta Ads
                daily_spend = round(random.uniform(1200, 3200), 2)
                impressions = random.randint(15000, 45000)
                clicks = int(impressions * random.uniform(0.018, 0.032)) # 1.8% - 3.2% CTR
            
            ad_performance.append({
                "performance_id": perf_id,
                "spend_date": current_date,
                "campaign_id": cmp["campaign_id"],
                "impressions": impressions,
                "clicks": clicks,
                "ad_spend_inr": daily_spend
            })
            perf_id += 1
            
    df_ad_performance = pd.DataFrame(ad_performance)

    # -------------------------------------------------------------
    # 3. TABLE 3: CUSTOMER LEADS (2,000 Granular User Profiles)
    # -------------------------------------------------------------
    city_areas = ['Vijay Nagar', 'Palasia', 'Saket', 'Bhawarkua', 'Rau', 'Annapurna', 'Mahalakshmi Nagar']
    age_groups = ['18-24', '25-34', '35-44', '45+']
    genders = ['Female', 'Male']
    
    leads = []
    for i in range(1, num_leads + 1):
        # Campaign weighting (Meta ~55%, Google ~45%)
        cmp = random.choices(campaigns, weights=[0.15, 0.15, 0.15, 0.22, 0.20, 0.13])[0]
        
        lead_date = (start_date + timedelta(days=random.randint(0, 44))).strftime("%Y-%m-%d")
        
        # Realistic conversion probabilities
        if cmp["ad_type"] == "Search" or "Retargeting" in cmp["campaign_name"]:
            conv_prob = 0.38  # Higher purchase intent
        elif cmp["ad_type"] == "Performance Max":
            conv_prob = 0.28
        else:
            conv_prob = 0.19  # Cold audience social prospecting
            
        is_converted = bool(np.random.binomial(1, conv_prob))
        
        # Order pricing logic in INR
        if is_converted:
            if cmp["category"] == "Ethnic Wear":
                order_value = round(random.uniform(2800, 8500), 2)
            elif cmp["category"] == "Menswear":
                order_value = round(random.uniform(1400, 4800), 2)
            else:
                order_value = round(random.uniform(900, 3600), 2)
            is_new = random.choices([True, False], weights=[0.72, 0.28])[0]
        else:
            order_value = 0.0
            is_new = random.choices([True, False], weights=[0.85, 0.15])[0]

        leads.append({
            "lead_id": f"LEAD_{i:04d}",
            "created_at": lead_date,
            "campaign_id": cmp["campaign_id"],
            "channel": cmp["channel"],
            "city_area": random.choice(city_areas),
            "age_group": random.choices(age_groups, weights=[0.35, 0.40, 0.18, 0.07])[0],
            "gender": random.choices(genders, weights=[0.58, 0.42])[0],
            "is_converted": is_converted,
            "order_value_inr": order_value,
            "is_new_customer": is_new
        })

    df_leads = pd.DataFrame(leads)

    # -------------------------------------------------------------
    # 4. EXPORT TO CSV FILES
    # -------------------------------------------------------------
    df_campaigns.to_csv("campaigns.csv", index=False)
    df_ad_performance.to_csv("ad_performance.csv", index=False)
    df_leads.to_csv("customer_leads_2000.csv", index=False)

    print("Generation Complete!")
    print(f"- campaigns.csv saved ({len(df_campaigns)} rows)")
    print(f"- ad_performance.csv saved ({len(df_ad_performance)} rows)")
    print(f"- customer_leads_2000.csv saved ({len(df_leads)} rows)")

if __name__ == "__main__":
    generate_marketing_data()