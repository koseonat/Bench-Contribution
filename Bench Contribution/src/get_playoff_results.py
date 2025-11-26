import pandas as pd
import requests
from io import StringIO
import os

def get_playoff_series():
    print("Scraping Playoff Series history...")
    url = "https://www.basketball-reference.com/playoffs/series.html"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Read all tables
        dfs = pd.read_html(StringIO(response.text))
        
        target_df = None
        
        # Search for the table
        for df in dfs:
            # Flatten multi-level columns if they exist (e.g., ('Winner', 'Team') -> 'Winner Team')
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = [' '.join(col).strip() for col in df.columns.values]
            
            # Print columns to debug if needed
            # print("Checking table with cols:", df.columns.tolist())
            
            # Check for the specific messy column names you saw in the error
            # We look for partial matches because "Unnamed: 0_level_0 Yr" is unstable
            col_str = " ".join(df.columns)
            if 'Winner Team' in col_str and 'Loser Team' in col_str:
                target_df = df
                break
        
        if target_df is None:
            print("Error: Could not find the series table.")
            return

        # RENAME the messy columns to the clean names we need
        # We search for the column that *contains* 'Yr', 'Series', 'Winner Team', etc.
        
        rename_map = {}
        for col in target_df.columns:
            if 'Yr' in col: rename_map[col] = 'Year'
            elif 'Series' in col: rename_map[col] = 'Round'
            elif 'Winner Team' in col: rename_map[col] = 'Winner'
            elif 'Loser Team' in col: rename_map[col] = 'Loser'

        target_df = target_df.rename(columns=rename_map)
        
        # Keep only the clean columns
        try:
            target_df = target_df[['Year', 'Round', 'Winner', 'Loser']]
        except KeyError as e:
            print(f"Error: Renaming failed. Columns present: {target_df.columns.tolist()}")
            return

        # Filter Years (2010+)
        target_df['Year'] = pd.to_numeric(target_df['Year'], errors='coerce')
        target_df = target_df.dropna(subset=['Year'])
        target_df = target_df[target_df['Year'] >= 2010]
        
        # Save
        os.makedirs("data/raw", exist_ok=True)
        target_df.to_csv("data/raw/playoff_outcomes.csv", index=False)
        print(f"Success: Saved playoff_outcomes.csv ({len(target_df)} series found)")
        return target_df
        
    except Exception as e:
        print(f"Detailed Error: {e}")

if __name__ == "__main__":
    get_playoff_series()
