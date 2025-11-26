import pandas as pd
import numpy as np
import os

def process_playoff_hypothesis():
    print("⚙️  Processing Playoff Bench Data...")
    
    try:
        # Load the files
        players = pd.read_csv("data/raw/nba_playoff_player_stats.csv")
        outcomes = pd.read_csv("data/raw/playoff_outcomes.csv")
    except FileNotFoundError:
        print("❌ Error: Missing CSV files. Make sure you have both player stats and outcomes.")
        return

    # --- 1. CLEAN PLAYER DATA ---
    # Convert columns to numeric
    cols = ['G', 'GS', 'PTS', 'MP']
    for col in cols:
        players[col] = pd.to_numeric(players[col], errors='coerce').fillna(0)

    # Filter out 'TOT' (Total) rows
    players = players[players['Tm'] != 'TOT']

    # Define Playoff Bench: Started less than half the playoff games they played
    players['is_bench'] = players['GS'] < (players['G'] * 0.5)

    # --- 2. CALCULATE TEAM BENCH PPG ---
    # Correct Formula: (Total Bench Points Scored) / (Total Games Team Played)
    
    # Find max games played by the team in that playoff run
    team_games = players.groupby(['Tm', 'Year'])['G'].max().reset_index()
    team_games.rename(columns={'G': 'Team_Games_Played'}, inplace=True)
    
    # Sum Total Bench Points
    bench_totals = players[players['is_bench'] == True].groupby(['Tm', 'Year'])['PTS'].sum().reset_index()
    bench_totals.rename(columns={'PTS': 'Total_Bench_PTS'}, inplace=True)
    
    # Merge
    team_stats = pd.merge(bench_totals, team_games, on=['Tm', 'Year'])
    
    # Calculate PPG
    team_stats['Bench_PPG'] = team_stats['Total_Bench_PTS'] / team_stats['Team_Games_Played']
    
    print(f"   Calculated Bench stats for {len(team_stats)} playoff teams.")

    # --- 3. MAP NAMES ---
    # Standard Dictionary to map "Boston Celtics" -> "BOS"
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

    # Clean Names just in case
    outcomes['Winner'] = outcomes['Winner'].str.replace(r' \(\d+\)', '', regex=True)
    outcomes['Loser'] = outcomes['Loser'].str.replace(r' \(\d+\)', '', regex=True)

    outcomes['Winner_Code'] = outcomes['Winner'].map(team_map)
    outcomes['Loser_Code'] = outcomes['Loser'].map(team_map)

    # --- 4. MERGE & DIFF ---
    # Join Winner Stats
    df = pd.merge(outcomes, team_stats, left_on=['Winner_Code', 'Year'], right_on=['Tm', 'Year'], how='inner')
    df.rename(columns={'Bench_PPG': 'Winner_Bench_PPG'}, inplace=True)
    
    # Join Loser Stats
    df = pd.merge(df, team_stats, left_on=['Loser_Code', 'Year'], right_on=['Tm', 'Year'], how='inner', suffixes=('_Win', '_Lose'))
    df.rename(columns={'Bench_PPG': 'Loser_Bench_PPG'}, inplace=True)

    # Calculate Differential
    df['Bench_Differential'] = df['Winner_Bench_PPG'] - df['Loser_Bench_PPG']
    
    # Save
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv("data/processed/hypothesis_2_data.csv", index=False)
    print(f"✅ Success! Created 'data/processed/hypothesis_2_data.csv' with {len(df)} series.")

if __name__ == "__main__":
    process_playoff_hypothesis()
