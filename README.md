DSA 210 Project Proposal: Importance of Bench
Contribution in the NBA Playoffs

Predicting NBA Playoff Series Outcomes Based on Bench Scoring and Advanced
Contributions

Time Frame : 2000-2025, to make the data collection process more feasible

I. Motivation

I love basketball and the NBA, and I have been following the league for years. In the NBA
playoffs, coaches are inclined to give more minutes to their starting players rather than their
bench players. Therefore, rotations shorten once the regular season is over. In the playoffs, the
defensive intensity of the games significantly increases and games become more competitive.
As a result of increased intensity and gravity of the games, starting players struggle more and
get tired faster. This is where the importance of bench contribution comes into play.While star
player performance is crucial, the depth and efficiency of the non-starter unit (the bench) are
often considered as the key differentiators between championship contenders. This project is
motivated by an urge to quantify this conventional wisdom. I aim to move beyond simple total
bench points to develop a robust metric that captures the true impact of non-starting players by
enriching my data with additional statistics and using it to predict the likelihood of a team
winning a playoff series.

II.Data Sources

The data for this project will be collected from publicly available online sports statistics
databases.

The data sources for collecting my primary data are stated below, and I will be calculating the
bench scoring differential which is the net point margin contributed by bench players(non-
starters) per series/game.

(https://www.basketball-reference.com/),
(https://www.basketball-reference.com/playoffs/series.html)

The data sources for collecting additional data to enrich the project are stated below. I will be
calculating the Bench Player Net Ranking (BPNR) which focusses on the efficiency of the
bench players per possesion both offensively and defensively. Also I will be calculating the
Value Over Replacement Player (VORP) and Box Plus/Minus (BPM) statistics for the bench
players of the teams.

(https://www.nba.com/stats),
(https://www.basketball-reference.com/leaders/bpm_career_p.html),
(https://www.basketball-reference.com/leaders/vorp_career.html)

III.Data Analysis

A. Exploratory Data Analysis (EDA) and Hypothesis Testing

1. Bench Trend Analysis: Visualizing average bench scoring differential for all playoff
teams over the selected seasons.
2. Series Outcome Comparison: Comparing the distributions of BPNR and Bench
Scoring Differential for teams that win a series versus teams that lose a series.
3. Hypothesis Testing: Testing the null hypothesis.
(H0): There is no significant difference in the mean Bench Player Net Rating (BPNR)
between series-winning and series-losing teams.

B. Machine Learning Implementation

The primary analytical goal is to predict the outcome (Win/Loss) of an NBA playoff
series based on bench contributions using supervised and unsupervised machine learning
methods.

IV.Findings

• Expected Findings: I expect to find that a positive Bench Player Net Rating
(BPNR) is a strong predictor of winning a series.

V.Limitations and Future Work

• Limitations: Data availability for advanced metrics may be limited in older seasons,
potentially reducing the sample size. Calculating BPNR requires careful cleaning to
correctly identify all-bench lineups, which may introduce complexity.
• Future Work: The model could be extended to predict the series length (4, 5, 6, or 7
games) using classifications and approaches.
