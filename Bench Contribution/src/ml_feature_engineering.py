import pandas as pd
import numpy as np
import os

def prepare_ml_data():
    print("🔧 Re-Running Feature Engineering (Adding 'Round' info)...")

    try:
        df_vorp = pd.read_csv("data/processed/hypothesis_4_data.csv")
        df_bpm  = pd.read_csv("data/processed/hypothesis_3_data.csv")
        df_vol  = pd.read_csv("data/processed/hypothesis_2_data.csv")
    except FileNotFoundError:
        print("❌ Error: Processed data files missing.")
        return

    # Merge
    master_df = pd.merge(df_vorp, 
                         df_bpm[['Year', 'Winner', 'Loser', 'Efficiency_Diff', 'Winner_Bench_BPM', 'Loser_Bench_BPM']], 
                         on=['Year', 'Winner', 'Loser'], how='inner')
    
    master_df = pd.merge(master_df, 
                         df_vol[['Year', 'Winner', 'Loser', 'Bench_Differential', 'Winner_Bench_PPG', 'Loser_Bench_PPG']], 
                         on=['Year', 'Winner', 'Loser'], how='inner')

    ml_rows = []
    np.random.seed(42)

    for idx, row in master_df.iterrows():
        # Keep the Round info!
        series_round = row.get('Round', 'Unknown')
        
        if np.random.rand() > 0.5:
            # Case 1: Team A is Winner
            new_row = {
                'Year': row['Year'],
                'Round': series_round,
                'TeamA': row['Winner_Code'],
                'TeamB': row['Loser_Code'],
                'TeamA_Bench_VORP': row['Winner_Bench_VORP'],
                'TeamB_Bench_VORP': row['Loser_Bench_VORP'],
                'Diff_VORP': row['VORP_Diff'],
                'Diff_BPM': row['Efficiency_Diff'],
                'Diff_PPG': row['Bench_Differential'],
                'Target_Win': 1
            }
        else:
            # Case 2: Team A is Loser
            new_row = {
                'Year': row['Year'],
                'Round': series_round,
                'TeamA': row['Loser_Code'],
                'TeamB': row['Winner_Code'],
                'TeamA_Bench_VORP': row['Loser_Bench_VORP'],
                'TeamB_Bench_VORP': row['Winner_Bench_VORP'],
                'Diff_VORP': -1 * row['VORP_Diff'],
                'Diff_BPM': -1 * row['Efficiency_Diff'],
                'Diff_PPG': -1 * row['Bench_Differential'],
                'Target_Win': 0
            }
        ml_rows.append(new_row)

    ml_dataset = pd.DataFrame(ml_rows)
    ml_dataset.to_csv("data/ml/playoff_matchups_labeled.csv", index=False)
    print(f"✅ Success! Updated dataset with {len(ml_dataset)} rows.")

if __name__ == "__main__":
    prepare_ml_data()
