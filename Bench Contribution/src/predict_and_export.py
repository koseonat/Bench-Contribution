import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

def export_predictions():
    print("🔮 Generating Prediction Report (with Confidence)...")

    try:
        df = pd.read_csv("data/ml/playoff_matchups_labeled.csv")
    except FileNotFoundError:
        print("❌ Error: ML data not found.")
        return

    train_mask = df['Year'] <= 2019
    test_mask  = df['Year'] >= 2020
    
    features = ['Diff_VORP', 'Diff_BPM', 'Diff_PPG']
    
    X_train = df.loc[train_mask, features]
    y_train = df.loc[train_mask, 'Target_Win']
    X_test = df.loc[test_mask, features]
    y_test = df.loc[test_mask, 'Target_Win']
    
    meta_test = df.loc[test_mask, ['Year', 'Round', 'TeamA', 'TeamB']]

    rf = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=5)
    rf.fit(X_train, y_train)

    predictions = rf.predict(X_test)
    probs = rf.predict_proba(X_test)[:, 1]

    results = []
    for (idx, row), pred, prob, actual in zip(meta_test.iterrows(), predictions, probs, y_test):
        real_winner = row['TeamA'] if actual == 1 else row['TeamB']
        pred_winner = row['TeamA'] if pred == 1 else row['TeamB']
        
        # Calculate Confidence (Probability of the predicted class)
        confidence = prob if pred == 1 else (1 - prob)
        
        status = "✅ Correct" if real_winner == pred_winner else "❌ Incorrect"
        
        results.append({
            'Year': row['Year'],
            'Round': row['Round'],
            'Matchup': f"{row['TeamA']} vs {row['TeamB']}",
            'Predicted': pred_winner,
            'Actual': real_winner,
            'Conf %': f"{confidence:.1%}",  # Added Confidence Column
            'Res': status
        })

    final_df = pd.DataFrame(results)
    final_df.to_csv("data/ml/final_predictions_2020_2025.csv", index=False)
    print(f"✅ Success! Saved predictions with Confidence rates.")

if __name__ == "__main__":
    export_predictions()
