import pandas as pd
import numpy as np
import os

def process_hypothesis_4():
    print("⚙️  Processing Bench VORP Data...")
    
    try:
        basic = pd.read_csv("data/raw/nba_playoff_player_stats.csv")
        adv = pd.read_csv("data/raw/nba_playoff_advanced_stats.csv")
        outcomes = pd.read_csv("data/raw/playoff_outcomes.csv")
    except FileNotFoundError:
        print("❌ Error: Missing files.")
        return

    # 1. Identify Bench Players (from Basic Stats)
    basic = basic[basic['Tm'] != 'TOT']
    for col in ['G', 'GS']: basic[col] = pd.to_numeric(basic[col], errors='coerce').fillna(0)
    basic['is_bench'] = basic['GS'] < (basic['G'] * 0.5)

    # 2. Get VORP (from Advanced Stats)
    adv = adv[adv['Tm'] != 'TOT']
    adv['VORP'] = pd.to_numeric(adv['VORP'], errors='coerce').fillna(0)

    # 3. Merge
    merged = pd.merge(basic[['Player', 'Tm', 'Year', 'is_bench']], 
                      adv[['Player', 'Tm', 'Year', 'VORP']], 
                      on=['Player', 'Tm', 'Year'], how='inner')

    # 4. Calculate Average Bench VORP per Team
    bench_data = merged[merged['is_bench'] == True]
    
    # We use MEAN VORP per bench player (Efficiency/Contribution per player slot)
    # VORP is cumulative, so summing it would bias towards teams that played more games in the series.
    # Averages are safer for comparing "Unit Strength".
    team_stats = bench_data.groupby(['Tm', 'Year'])['VORP'].mean().reset_index()
    team_stats.rename(columns={'VORP': 'Bench_Avg_VORP'}, inplace=True)

    # 5. Map & Merge with Outcomes
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

    # Merge
    df = pd.merge(outcomes, team_stats, left_on=['Winner_Code', 'Year'], right_on=['Tm', 'Year'], how='inner')
    df.rename(columns={'Bench_Avg_VORP': 'Winner_Bench_VORP'}, inplace=True)
    
    df = pd.merge(df, team_stats, left_on=['Loser_Code', 'Year'], right_on=['Tm', 'Year'], how='inner', suffixes=('_Win', '_Lose'))
    df.rename(columns={'Bench_Avg_VORP': 'Loser_Bench_VORP'}, inplace=True)

    # Differential
    df['VORP_Diff'] = df['Winner_Bench_VORP'] - df['Loser_Bench_VORP']
    
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv("data/processed/hypothesis_4_data.csv", index=False)
    print(f"✅ Success! Created 'data/processed/hypothesis_4_data.csv' with {len(df)} series.")

if __name__ == "__main__":
    process_hypothesis_4()
