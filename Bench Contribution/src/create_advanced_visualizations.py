import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

def generate_plots():
    print("🎨 Generating Advanced Visualizations (Boxplot, Scatter, Heatmap)...")
    
    # 1. Load the ML Dataset (It has all the differentials ready)
    try:
        df = pd.read_csv("data/ml/playoff_matchups_labeled.csv")
    except FileNotFoundError:
        print("❌ Error: ML data not found. Run 'src/ml_feature_engineering.py' first.")
        return

    # Create output folder
    os.makedirs("figures", exist_ok=True)

    # Set the aesthetic style
    sns.set_style("whitegrid")

    # --- PLOT 1: BOXPLOT (Winner vs. Loser Bench VORP) ---
    # We need to restructure data slightly for a side-by-side boxplot
    # We will use the raw 'TeamA_Bench_VORP' and 'TeamB_Bench_VORP' based on who won
    
    winners_vorp = []
    losers_vorp = []
    
    for _, row in df.iterrows():
        if row['Target_Win'] == 1:
            winners_vorp.append(row['TeamA_Bench_VORP'])
            losers_vorp.append(row['TeamB_Bench_VORP'])
        else:
            winners_vorp.append(row['TeamB_Bench_VORP'])
            losers_vorp.append(row['TeamA_Bench_VORP'])
            
    plot_data = pd.DataFrame({
        'Winner Bench VORP': winners_vorp,
        'Loser Bench VORP': losers_vorp
    })
    
    # Melt for Seaborn
    df_melted = plot_data.melt(var_name='Group', value_name='Average Bench VORP')

    plt.figure(figsize=(8, 6))
    sns.boxplot(x='Group', y='Average Bench VORP', data=df_melted, palette=['#2ecc71', '#e74c3c'])
    plt.title('Distribution of Bench Value (VORP): Winners vs. Losers', fontsize=14)
    plt.ylabel('Average Bench VORP (Higher is Better)')
    plt.savefig("figures/boxplot_vorp.png")
    print("   ✅ Boxplot saved to figures/boxplot_vorp.png")
    plt.close()

    # --- PLOT 2: SCATTERPLOT (The "Volume Trap") ---
    # X-Axis: PPG Differential (Volume)
    # Y-Axis: VORP Differential (Value)
    # Color: Did Team A Win?
    
    plt.figure(figsize=(10, 6))
    
    # We map 0/1 to Loss/Win for the legend
    df['Outcome'] = df['Target_Win'].map({1: 'Win', 0: 'Loss'})
    
    sns.scatterplot(
        data=df, 
        x='Diff_PPG', 
        y='Diff_VORP', 
        hue='Outcome', 
        palette={'Win': '#2ecc71', 'Loss': '#e74c3c'},
        alpha=0.7,
        s=100 # Dot size
    )
    
    # Add quadrants lines
    plt.axvline(0, color='gray', linestyle='--')
    plt.axhline(0, color='gray', linestyle='--')
    
    plt.title('The Bench "Trap": Volume (PPG) vs. Value (VORP)', fontsize=14)
    plt.xlabel('Bench Scoring Differential (Positive = Team A Scored More)')
    plt.ylabel('Bench VORP Differential (Positive = Team A Had More Value)')
    plt.legend(title='Series Outcome (Team A)')
    plt.savefig("figures/scatterplot_volume_vs_value.png")
    print("   ✅ Scatterplot saved to figures/scatterplot_volume_vs_value.png")
    plt.close()

    # --- PLOT 3: HEATMAP (Feature Correlations) ---
    # We want to see how features correlate with the Target (Winning)
    
    cols_to_corr = ['Diff_PPG', 'Diff_BPM', 'Diff_VORP', 'Target_Win']
    corr_matrix = df[cols_to_corr].corr()
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(
        corr_matrix, 
        annot=True, 
        cmap='coolwarm', 
        fmt=".2f", 
        linewidths=0.5,
        vmin=-1, vmax=1
    )
    plt.title('Correlation Matrix: Which Stats Predict Winning?', fontsize=14)
    plt.savefig("figures/heatmap_correlation.png")
    print("   ✅ Heatmap saved to figures/heatmap_correlation.png")
    plt.close()

if __name__ == "__main__":
    generate_plots()
