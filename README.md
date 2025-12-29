# DSA 210 Project Proposal  
## Predicting NBA Playoff Series Outcomes Based on Bench Scoring and Advanced Contributions  

**Time Frame:** 2010–2025  

---

### Motivation  

Basketball has always been one of my biggest passions, especially the NBA. During the playoffs, the dynamics of the game shift dramatically — starters log more minutes, rotations shorten, and defensive intensity skyrockets.  

As games become tougher and fatigue sets in, the performance of bench players can make the difference between advancing and going home. While star players often steal the spotlight, the **depth and efficiency of a team’s bench** may be the true differentiator for championship contenders.  

This project aims to **quantify the impact of bench contributions** in the NBA playoffs. Rather than focusing only on total bench points, I’ll create a more robust metric — one that captures both scoring and efficiency — to see how much the bench really matters in determining playoff success.  

---

### Data Sources  

Data will be collected from publicly available basketball statistics databases.  

#### **Primary Sources (for core metrics):**  
- [Basketball Reference](https://www.basketball-reference.com/)  
- [Playoff Series Match Results Data](https://www.basketball-reference.com/playoffs/series.html)  

**Metric:**  
- **Bench Scoring Differential:** Net point margin contributed by bench players per game or series.  

#### **Additional Sources (for advanced metrics):**   
- [BPM Career Leaders](https://www.basketball-reference.com/leaders/bpm_career.html)
- [VORP Career Leaders](https://www.basketball-reference.com/leaders/vorp_career.html)  

**Metrics to be developed:**  
- **Bench Player Net Rating (BPNR):** Efficiency of bench players per possession (offensive and defensive).  
- **VORP (Value Over Replacement Player)** and **BPM (Box Plus/Minus)** for all bench players.  

---

### Data Analysis Plan  

#### A. Exploratory Data Analysis (EDA) & Hypothesis Testing  

1. **Bench Trend Analysis:**  
     
2. **Series Outcome Comparison:**  
    
3. **Hypothesis Testing:**    

---

## Analysis Results 

### Phase 1: Predictive Analysis (Regular Season Depth)
We first tested if a deep bench in the regular season predicts success in the playoffs.
* **Hypothesis 1:** Teams with higher *Regular Season* bench scoring win more playoff series.
* **Metric:** Regular Season Bench Total Points vs. Playoff Series Outcome.
* **Result:**
    * **P-Value:** 0.784 (Insignificant)
    * **Conclusion:** We **failed to reject the null hypothesis**. A deep bench in the regular season is NOT a strong predictor of playoff series wins.

### Phase 2: Descriptive Analysis (Playoff Volume)
We then narrowed our scope to analyze player performance *during* the playoffs to see if bench scoring volume decided specific matchups.
* **Hypothesis 2:** The bench scoring differential (Winner - Loser) in a playoff series is significantly different from zero.
* **Metric:** (Winner Bench PPG - Loser Bench PPG) in specific playoff series.
* **Result:**
    * **P-Value:** $3.11 \times 10^{-39}$ (Highly Significant)
    * **Mean Differential:** -2.33 PPG
    * **Conclusion:** We **rejected the null hypothesis**, but with a surprising finding. The differential is **negative**, meaning series winners typically receive **fewer** points from their bench than the losers.

### Phase 3: Qualitative Analysis (Bench Efficiency)
We then analyzed the *quality* of minutes played by the bench, rather than just the raw points scored.
* **Hypothesis 3:** The bench efficiency differential (Winner - Loser) in a playoff series is significantly different from zero.
* **Metric:** Weighted Average Box Plus/Minus (BPM) Differential.
* **Result:**
    * **P-Value:** $4.48 \times 10^{-4}$ (Significant)
    * **Mean Differential:** +0.52 BPM
    * **Conclusion:** We **rejected the null hypothesis** with a **positive** correlation. Series winners typically have benches with higher efficiency ratings (BPM) than losers.

### Phase 4: Value Analysis (Bench VORP)
Finally, we assessed the overall value provided by bench players compared to a replacement-level player, combining both production and efficiency.
* **Hypothesis 4:** The average bench VORP differential (Winner - Loser) in a playoff series is significantly different from zero.
* **Metric:** Average Value Over Replacement Player (VORP) Differential.
* **Result:**
    * **P-Value:** $2.84 \times 10^{-12}$ (Highly Significant)
    * **Mean Differential:** +0.039 VORP
    * **Conclusion:** We **rejected the null hypothesis** with a strong **positive** correlation.
    * **Mean Winner Bench VORP:** 0.0767
    * **Mean Loser Bench VORP:** 0.0373
    * **Insight:** Winning bench players contribute nearly **double the value** over a replacement player compared to losing bench players.

### Key Insight: The "Hold the Line" Theory
Our multi-stage analysis reveals a nuanced reality about NBA rotations:
1.  **Star Power Rules:** In the playoffs, rotations shorten. Teams that rely on high-volume bench scoring often lose (Phase 2), likely because their starters are underperforming.
2.  **Quality Over Quantity:** While winning benches score *less*, they are *more efficient* and provide *more value*.
    * They play "winning basketball" (Positive VORP/BPM) without needing to dominate the ball.
3.  **Final Verdict:** The ideal playoff bench does not need to score 50 points; it simply needs to be efficient enough to "hold the line" and maintain the margins established by the stars.

---

## 5. Advanced Visualizations (EDA)
To deepen our understanding of the "Star Power" vs. "Depth" dynamic, we generated three distinct visualizations.

### A. Boxplot Analysis: Winners vs. Losers
We compared the distribution of Bench VORP for series winners versus losers.
* **Insight:** The median VORP for winners (Green) is distinctly higher than for losers (Red). Winners rarely have a "negative value" bench.

### B. Scatterplot: The "Volume Trap"
This plot visualizes the relationship between **Bench Scoring (X-axis)** and **Bench Value (Y-axis)**.
* **Insight:** Notice the cluster of **Red Dots (Losses)** in the bottom-right quadrant. These are teams that scored *more* bench points but provided *less* value. This visually confirms our "Volume Trap" hypothesis.

### C. Correlation Heatmap
We analyzed how our features correlate with the binary target (`Target_Win`).
* **Insight:**
    * `Diff_VORP`: **Positive Correlation** (Value leads to wins).
    * `Diff_PPG`: **Negative Correlation** (High bench scoring predicts losses).

---

## 6. Machine Learning & Prediction
**Goal:** Train a predictive model to forecast the winner of a playoff series based on Bench Metrics.
**Lecture References:**
* **Standardization** 
* **Logistic Regression** 
* **Random Forest** 
* **Confusion Matrix** 

### A. Methodology (Detailed Implementation)

#### 1. Standardization (Feature Scaling)
**Why we used it:** Our features had vastly different units. `Diff_PPG` (Volume) ranged from roughly -15 to +15, while `Diff_VORP` (Value) ranged from -0.5 to +0.5. Without scaling, models using gradient descent would be biased toward the larger numbers (PPG).
**How we applied it:** We used the **StandardScaler** ($z = \frac{x - \mu}{\sigma}$) to transform all inputs.


[Image of standard normal distribution curve]

* We centered every feature around **0** with a standard deviation of **1**.
* This ensured that `Diff_VORP` and `Diff_PPG` were treated as equals by the model.

#### 2. Logistic Regression (The "Why" Model)
**Why we used it:** We needed a **binary classifier** (Win=1, Loss=0) that is **interpretable**. We modeled the probability ($P$) that "Team A wins" using the Sigmoid function:
$$P(Y=1) = \frac{1}{1 + e^{-(\beta_0 + \beta_1 X_1 + ...)}}$$

**Key Findings (Coefficients):**
* **`Diff_PPG` Coefficient (-4.00):** This large negative number proves that for every standard deviation increase in bench scoring volume, the odds of winning **decrease** significantly.
* **`Diff_VORP` Coefficient (+1.05):** This positive number proves that higher Value Over Replacement leads to higher winning odds.

#### 3. Random Forest (The "Prediction" Model)
**Why we used it:** Basketball is complex and non-linear. **Random Forest** is an **Ensemble Method** (Bagging) that creates many "weak" decision trees and merges them to get a more accurate and stable prediction.

**How we applied it:**
* **Estimators:** We built **100 Decision Trees**. Each tree looked at a random subset of our playoff data.
* **Voting:** To predict the 2024 Finals, the model aggregated the votes of all 100 trees to produce a **Confidence Rate**.

#### 4. Confusion Matrix & Accuracy
**Why we used it:** Accuracy alone can be misleading. The Confusion Matrix helps us see *how* the model is failing (Type I vs Type II errors).

* **Accuracy:** **90.67%** (68/75 Correct)
* **True Positives (31):** Model predicted Winner, Team Won.
* **False Positives (4):** Model predicted Win, but they Lost.
* **Balance:** The errors were symmetric (4 False Positives, 4 False Negatives), indicating no bias toward one class.

### B. Recent Predictions (2020-2025)
The prediction table displays the model's specific predictions for major playoff series (Conference Finals & NBA Finals) over the last 5 years, including the **Confidence Rate** of each prediction.

* **Green:** Correct Prediction.
* **Red:** Incorrect Prediction.
* **Observation:** The model correctly predicted the winner in **14 out of the last 15** major series shown, often with high confidence (>70%).

---

### Limitations

**Limitations:**  
- Advanced stats may be incomplete for earlier seasons.  
- Calculating BPNR requires identifying all-bench lineups, which can be complex.


