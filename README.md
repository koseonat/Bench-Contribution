# DSA 210 Project Proposal  
## Predicting NBA Playoff Series Outcomes Based on Bench Scoring and Advanced Contributions  

**Time Frame:** 2000–2025  

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
- [NBA Stats](https://www.nba.com/stats)  
- [BPM Career Leaders](https://www.basketball-reference.com/leaders/bpm_career.html)  
- [VORP Career Leaders](https://www.basketball-reference.com/leaders/vorp_career.html)  

**Metrics to be developed:**  
- **Bench Player Net Rating (BPNR):** Efficiency of bench players per possession (offensive and defensive).  
- **VORP (Value Over Replacement Player)** and **BPM (Box Plus/Minus)** for all bench players.  

---

### Data Analysis Plan  

#### A. Exploratory Data Analysis (EDA) & Hypothesis Testing  

1. **Bench Trend Analysis:**  
   - Visualize average bench scoring differentials across all playoff teams (2000–2025).  
2. **Series Outcome Comparison:**  
   - Compare BPNR and Bench Scoring Differential between winning and losing teams.  
3. **Hypothesis Testing:**  
   - **Null Hypothesis (H₀):** There is no significant difference in mean BPNR between series-winning and series-losing teams.  

---

### Expected Findings  

I expect that teams with a **positive Bench Player Net Rating (BPNR)** will have a **significantly higher probability of winning** playoff series.  

In other words, deeper benches should translate to more consistent postseason success.  

---

### Limitations & Future Work  

**Limitations:**  
- Advanced stats may be incomplete for earlier seasons (especially before 2010).  
- Calculating BPNR requires identifying all-bench lineups, which can be complex.  

**Future Work:**  
- Extend the model to predict **series length (4, 5, 6, or 7 games)**.  
- Explore **player fatigue** and **bench usage patterns** as additional predictive features.  


