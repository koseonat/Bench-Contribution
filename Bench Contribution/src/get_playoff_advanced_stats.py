import pandas as pd
import requests
from io import StringIO
import os
import time
import random

def get_playoff_advanced():
    print("🧠 Re-Scraping Playoff ADVANCED Stats (Adding VORP)...")
    
    all_years = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    }
    
    for year in range(2010, 2025):
        url = f"https://www.basketball-reference.com/playoffs/NBA_{year}_advanced.html"
        print(f"   Fetching {year}...", end=" ")
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 404: continue
            response.raise_for_status()
            
            dfs = pd.read_html(StringIO(response.text))
            df = dfs[0]
            df = df[df['Player'] != 'Player']
            df['Year'] = year
            
            # --- UPDATE: Added 'VORP' to the list ---
            cols_to_keep = ['Player', 'Tm', 'Year', 'G', 'MP', 'PER', 'BPM', 'VORP']
            
            valid_cols = [c for c in cols_to_keep if c in df.columns]
            df = df[valid_cols]
            
            all_years.append(df)
            print("✅ Done.")
            time.sleep(random.uniform(2, 4))
            
        except Exception as e:
            print(f"❌ Error: {e}")

    if all_years:
        final_df = pd.concat(all_years, ignore_index=True)
        os.makedirs("data/raw", exist_ok=True)
        final_df.to_csv("data/raw/nba_playoff_advanced_stats.csv", index=False)
        print(f"\n🎉 Success! Saved {len(final_df)} rows (with VORP) to 'data/raw/nba_playoff_advanced_stats.csv'")

if __name__ == "__main__":
    get_playoff_advanced()
