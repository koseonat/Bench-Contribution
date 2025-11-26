import pandas as pd
import requests
from io import StringIO
import os
import time
import random

def get_playoff_stats():
    print("🏀 Starting Scraping: NBA Playoff Player Stats (2010-2025)...")
    
    all_years = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    }
    
    # We scrape up to 2024 (2025 playoffs usually haven't happened or are just starting depending on current date)
    for year in range(2010, 2025):
        url = f"https://www.basketball-reference.com/playoffs/NBA_{year}_per_game.html"
        print(f"   Fetching {year} playoffs...", end=" ")
        
        try:
            response = requests.get(url, headers=headers)
            
            if response.status_code == 404:
                print("Skipped (Data not found)")
                continue
                
            response.raise_for_status()
            
            # Read the HTML table
            dfs = pd.read_html(StringIO(response.text))
            df = dfs[0]
            
            # Cleanup headers (remove repeating "Player" headers)
            df = df[df['Player'] != 'Player']
            df['Year'] = year
            
            all_years.append(df)
            print("✅ Done.")
            
            # Sleep to avoid getting banned
            time.sleep(random.uniform(2, 4))
            
        except Exception as e:
            print(f"❌ Error: {e}")

    # Combine and Save
    if all_years:
        final_df = pd.concat(all_years, ignore_index=True)
        os.makedirs("data/raw", exist_ok=True)
        final_df.to_csv("data/raw/nba_playoff_player_stats.csv", index=False)
        print(f"\n🎉 Success! Saved {len(final_df)} rows to 'data/raw/nba_playoff_player_stats.csv'")
    else:
        print("\n❌ Failed to scrape any data.")

if __name__ == "__main__":
    get_playoff_stats()
