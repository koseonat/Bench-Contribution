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

### Limitations & Future Work  

**Limitations:**  
- Advanced stats may be incomplete for earlier seasons.  
- Calculating BPNR requires identifying all-bench lineups, which can be complex.
