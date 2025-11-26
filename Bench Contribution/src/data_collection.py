import pandas as pd
import time
import os
import random

def get_stats(year, stat_type='per_game'):
    """
    Scrapes stats from Basketball Reference.
    stat_type can be 'per_game' (Basic) or 'advanced' (Enrichment).
    """
    url = f"https://www.basketball-reference.com/leagues/NBA_{year}_{stat_type}.html"
    print(f"Fetching {stat_type} stats for {year}...")
    
    try:
        # Read HTML tables
        dfs = pd.read_html(url)
        df = dfs[0]
        
        # Cleanup: Remove repeating headers in the middle of the table
        df = df[df['Player'] != 'Player']
        df['Year'] = year
        return df
    except Exception as e:
        print(f"Error scraping {year} {stat_type}: {e}")
        return None

def main():
    # 1. Collect Basic Stats (The Core Data)
    basic_data = []
    # 2. Collect Advanced Stats (The Enrichment Data)
    advanced_data = []
    
    # UPDATED RANGE: 2010 to 2026
    # Note: 2026 might fail if the season hasn't started/finished, but the try/except handles it.
    years = range(2010, 2026) 
    
    total_years = len(years)
    
    for i, year in enumerate(years):
        print(f"--- Processing {year} ({i+1}/{total_years}) ---")
        
        # Get Basic
        basic = get_stats(year, 'per_game')
        if basic is not None:
            basic_data.append(basic)
        
        # Be polite to the server (Sleep 3-5 seconds)
        time.sleep(random.uniform(3, 5)) 
        
        # Get Advanced (Enrichment)
        adv = get_stats(year, 'advanced')
        if adv is not None:
            advanced_data.append(adv)
            
        time.sleep(random.uniform(3, 5))

    # Save Basic Stats
    if basic_data:
        os.makedirs("data/raw", exist_ok=True)
        df_basic = pd.concat(basic_data, ignore_index=True)
        df_basic.to_csv("data/raw/nba_basic_stats.csv", index=False)
        print("Success: Saved nba_basic_stats.csv")

    # Save Advanced Stats
    if advanced_data:
        df_adv = pd.concat(advanced_data, ignore_index=True)
        df_adv.to_csv("data/raw/nba_advanced_stats.csv", index=False)
        print("Success: Saved nba_advanced_stats.csv")

if __name__ == "__main__":
    main()