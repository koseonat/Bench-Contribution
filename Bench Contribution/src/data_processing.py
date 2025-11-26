import pandas as pd
import numpy as np
import os

def process_data():
    print("Loading raw data...")
    try:
        basic = pd.read_csv("data/raw/nba_basic_stats.csv")
        outcomes = pd.read_csv("data/raw/playoff_outcomes.csv")
    except FileNotFoundError:
        print("Error: Missing CSV files. Run data_collection.py and get_playoff_results.py first.")
        return

    # --- PART 1: Prepare Bench Stats ---
    # Filter out partial season stats ('TOT')
    basic = basic[basic['Team'] != 'TOT']
    
    # Convert columns to numbers
    cols_to_numeric = ['G', 'GS', 'PTS', 'MP']
    for col in cols_to_numeric:
        basic[col] = pd.to_numeric(basic[col], errors='coerce').fillna(0)

    # Define Bench: Started < 50% of games
    basic['is_bench'] = basic['GS'] < (basic['G'] * 0.5)

    # Aggregate by Team and Year
    bench_stats = basic[basic['is_bench'] == True].groupby(['Team', 'Year']).agg({
        'PTS': 'sum',
        'G': 'count'
    }).reset_index()
    
    bench_stats.rename(columns={'PTS': 'Bench_Total_PTS'}, inplace=True)

    # --- PART 2: Clean Playoff Data ---
    # CRITICAL FIX: Remove the seed numbers (e.g., " (1)") from the names
    # We use Regex to replace " (any number)" with nothing
    outcomes['Winner'] = outcomes['Winner'].str.replace(r' \(\d+\)', '', regex=True)
    outcomes['Loser'] = outcomes['Loser'].str.replace(r' \(\d+\)', '', regex=True)

    # Map Full Names to Codes
    team_map = {
        'Atlanta Hawks': 'ATL', 'Boston Celtics': 'BOS', 'Brooklyn Nets': 'BRK', 'New Jersey Nets': 'NJN',
        'Charlotte Hornets': 'CHO', 'Charlotte Bobcats': 'CHA', 'Chicago Bulls': 'CHI', 'Cleveland Cavaliers': 'CLE',
        'Dallas Mavericks': 'DAL', 'Denver Nuggets': 'DEN', 'Detroit Pistons': 'DET', 'Golden State Warriors': 'GSW',
        'Houston Rockets': 'HOU', 'Indiana Pacers': 'IND', 'Los Angeles Clippers': 'LAC', 'Los Angeles Lakers': 'LAL',
        'Memphis Grizzlies': 'MEM', 'Miami Heat': 'MIA', 'Milwaukee Bucks': 'MIL', 'Minnesota Timberwolves': 'MIN',
        'New Orleans Pelicans': 'NOP', 'New Orleans Hornets': 'NOH', 'New York Knicks': 'NYK', 'Oklahoma City Thunder': 'OKC',
        'Orlando Magic': 'ORL', 'Philadelphia 76ers': 'PHI', 'Phoenix Suns': 'PHO', 'Portland Trail Blazers': 'POR',
        'Sacramento Kings': 'SAC', 'San Antonio Spurs': 'SAS', 'Toronto Raptors': 'TOR', 'Utah Jazz': 'UTA',
        'Washington Wizards': 'WAS'
    }

    outcomes['Winner_Code'] = outcomes['Winner'].map(team_map)
    outcomes['Loser_Code'] = outcomes['Loser'].map(team_map)
    
    # Check for unmapped teams (debugging)
    missing_winners = outcomes[outcomes['Winner_Code'].isna()]['Winner'].unique()
    if len(missing_winners) > 0:
        print(f"Warning: Could not map these winning teams: {missing_winners}")

    # --- PART 3: Create Analysis Dataset ---
    # Create two rows per series: one for Winner, one for Loser
    winners = outcomes[['Year', 'Winner_Code', 'Round']].copy()
    winners.rename(columns={'Winner_Code': 'Team'}, inplace=True)
    winners['Series_Result'] = 'Won'
    
    losers = outcomes[['Year', 'Loser_Code', 'Round']].copy()
    losers.rename(columns={'Loser_Code': 'Team'}, inplace=True)
    losers['Series_Result'] = 'Lost'
    
    series_df = pd.concat([winners, losers])
    
    # Drop rows where mapping failed (if any)
    series_df.dropna(subset=['Team'], inplace=True)

    # Merge with Bench Stats
    final_df = pd.merge(series_df, bench_stats, on=['Team', 'Year'], how='inner')
    
    # Save
    os.makedirs("data/processed", exist_ok=True)
    final_df.to_csv("data/processed/playoff_bench_analysis.csv", index=False)
    print(f"Success: Created analysis file with {len(final_df)} series participants.")

if __name__ == "__main__":
    process_data()