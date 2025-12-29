import pandas as pd
import matplotlib.pyplot as plt
import os

def save_table_image():
    print("📊 Rendering Table with Confidence Rates...")

    try:
        df = pd.read_csv("data/ml/final_predictions_2020_2025.csv")
    except FileNotFoundError:
        return

    # Filter for Last 5 Years (2020+)
    df_recent = df[df['Year'] >= 2020].copy()
    
    # Filter for Finals/Conf Finals if possible
    if 'Round' in df_recent.columns:
        df_filtered = df_recent[df_recent['Round'].str.contains('Finals', case=False, na=False)].copy()
        if not df_filtered.empty:
            df_display = df_filtered
        else:
            df_display = df_recent.head(15)
    else:
        df_display = df_recent.head(15)

    df_display = df_display.sort_values(by=['Year', 'Round'], ascending=[False, True])
    
    # Updated Columns to Show
    cols = ['Year', 'Round', 'Matchup', 'Predicted', 'Actual', 'Conf %', 'Res']
    df_display = df_display[cols]

    # Dynamic Height Adjustment
    fig, ax = plt.subplots(figsize=(15, len(df_display)*0.6 + 1)) 
    ax.axis('off')

    table = ax.table(
        cellText=df_display.values,
        colLabels=df_display.columns,
        cellLoc='center',
        loc='center',
        colColours=['#2c3e50']*len(cols)
    )

    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1.0, 1.8)

    # Style Loop
    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_text_props(color='white', weight='bold')
        else:
            if row % 2 == 0: cell.set_facecolor('#ecf0f1')
            
            # Color Code Result
            if df_display.columns[col] == 'Res':
                txt = df_display.iloc[row-1]['Res']
                if 'Correct' in txt:
                    cell.set_text_props(color='#27ae60', weight='bold')
                else:
                    cell.set_text_props(color='#c0392b', weight='bold')
            
            # Bold the Confidence for emphasis
            if df_display.columns[col] == 'Conf %':
                 cell.set_text_props(weight='bold')

    plt.title('Prediction Results with Confidence (2020-2025 Major Series)', fontsize=16, weight='bold', pad=10)
    
    os.makedirs("figures", exist_ok=True)
    plt.savefig("figures/prediction_table.png", bbox_inches='tight', dpi=300)
    print("✅ Success! Table saved to figures/prediction_table.png")

if __name__ == "__main__":
    save_table_image()
