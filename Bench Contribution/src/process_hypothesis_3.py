import pandas as pd
import numpy as np
import os

def process_hypothesis_3():
    print("⚙️  Processing Bench Efficiency (BPM) Data...")
    
    try:
        # Load all necessary files
        basic = pd.read_csv("data/raw/nba_playoff_player_stats.csv")
        adv = pd.read_csv("data/raw/nba_playoff_advanced_stats.csv")
        outcomes = pd.read_csv("data/raw/playoff_outcomes.csv")
    except FileNotFoundError:
        print("❌ Error: Missing CSV files. Ensure you have Basic, Advanced, and Outcome data.")
        return

    # --- 1. PREPARE BASIC STATS (Identify Bench) ---
    basic = basic[basic['Tm'] != 'TOT']
    # Convert to numeric
    for col in ['G', 'GS', 'MP']:
        basic[col] = pd.to_numeric(basic[col], errors='coerce').fillna(0)
        
    # Define Bench: Started < 50% of games
    basic['is_bench'] = basic['GS'] < (basic['G'] * 0.5)
    
    # Keep only what we need to link
    # Note: 'MP' in basic is 'Minutes Per Game', we need Total Minutes for weighting.
    # Advanced stats usually has 'MP' as Total Minutes. Let's check Advanced.
    
    # --- 2. PREPARE ADVANCED STATS (Get BPM) ---
    adv = adv[adv['Tm'] != 'TOT']
    # Ensure numeric
    for col in ['BPM', 'MP']:
        adv[col] = pd.to_numeric(adv[col], errors='coerce').fillna(0)
    
    # --- 3. MERGE BASIC & ADVANCED ---
    # We merge on Player, Team, and Year
    merged = pd.merge(basic[['Player', 'Tm', 'Year', 'is_bench']], 
                      adv[['Player', 'Tm', 'Year', 'BPM', 'MP']], 
                      on=['Player', 'Tm', 'Year'], 
                      how='inner')

    # Filter for BENCH players only
    bench_players = merged[merged['is_bench'] == True].copy()
    
    # --- 4. CALCULATE WEIGHTED AVERAGE BPM ---
    # Formula: Sum(Player_BPM * Player_Minutes) / Sum(Team_Bench_Minutes)
    
    # Calculate 'Contribution' = BPM * Minutes
    bench_players['BPM_Contribution'] = bench_players['BPM'] * bench_players['MP']
    
    # Aggregate by Team and Year
    team_stats = bench_players.groupby(['Tm', 'Year']).agg({
        'BPM_Contribution': 'sum',
        'MP': 'sum'  # Total Bench Minutes
    }).reset_index()
    
    # Calculate Weighted Average
    team_stats['Bench_Avg_BPM'] = team_stats['BPM_Contribution'] / team_stats['MP']
    
    print(f"   Calculated Efficiency stats for {len(team_stats)} playoff teams.")

    # --- 5. MAP OUTCOMES ---
    # (Standard Mapping)
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

    outcomes['Winner'] = outcomes['Winner'].str.replace(r' \(\d+\)', '', regex=True)
    outcomes['Loser'] = outcomes['Loser'].str.replace(r' \(\d+\)', '', regex=True)
    outcomes['Winner_Code'] = outcomes['Winner'].map(team_map)
    outcomes['Loser_Code'] = outcomes['Loser'].map(team_map)

    # --- 6. MERGE & CALCULATE DIFFERENTIAL ---
    # Join Winner
    df = pd.merge(outcomes, team_stats, left_on=['Winner_Code', 'Year'], right_on=['Tm', 'Year'], how='inner')
    df.rename(columns={'Bench_Avg_BPM': 'Winner_Bench_BPM'}, inplace=True)
    
    # Join Loser
    df = pd.merge(df, team_stats, left_on=['Loser_Code', 'Year'], right_on=['Tm', 'Year'], how='inner', suffixes=('_Win', '_Lose'))
    df.rename(columns={'Bench_Avg_BPM': 'Loser_Bench_BPM'}, inplace=True)

    # Calculate Differential
    df['Efficiency_Diff'] = df['Winner_Bench_BPM'] - df['Loser_Bench_BPM']
    
    # Save
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv("data/processed/hypothesis_3_data.csv", index=False)
    print(f"✅ Success! Created 'data/processed/hypothesis_3_data.csv' with {len(df)} series.")

if __name__ == "__main__":
    process_hypothesis_3()
