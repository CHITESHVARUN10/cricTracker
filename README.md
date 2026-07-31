# IPL Match Insights Dashboard 🏏

A comprehensive, interactive Streamlit analytics dashboard for exploring historical Indian Premier League (IPL) cricket data. Rebuilt with pixel-perfect modern UI designs, rich data visualizations, and custom styled tables.

## 📌 Data Source & Attribution
This project relies on ball-by-ball delivery data, match outcomes, player profiles, and team information sourced from the MIT-licensed dataset:
👉 **[ritesh-ojha/IPL-DATASET](https://github.com/ritesh-ojha/IPL-DATASET)**

*Note: The dataset repository is an external data source and is licensed under the MIT License.*

---

## 🚀 Features & Dashboard Screens

The dashboard features 8 core analytical tabs, a global hero KPI bar, sidebar filters, and a bottom raw-data preview:

1. **Overview (Match Outcome Snapshot)**: Match result distribution (runs, wickets, ties), top venue win rates for batting first, and annual match counts across 2008–2024.
2. **Toss Analytics**: Coin toss decision distribution, win percentages when winning the toss, and win rate comparison between choosing to bat vs field first.
3. **Venue Impact Dashboard**: Individual venue deep dives, venue win split (batting first vs chasing), and top batters per venue.
4. **Teams Tab Panel**: Team-specific win statistics, win rates by innings context, and season-by-season win counts.
5. **Players Tab Panel**: Head-to-head player comparison (Runs, Strike Rate, Average, Wickets, Economy, 4s, 6s) and top batting & bowling leaderboards.
6. **Insights Lab (Advanced Analytics)**: Multi-metric venue matrix, team head-to-head records, and player form trackers.
7. **Phases Tab Panel**: Over-by-over phase analysis comparing Powerplay (overs 1–6), Middle Overs (overs 7–15), and Death Overs (overs 16–20).
8. **Matchups Tab Panel**: Head-to-head batter vs bowler statistics and run distribution.

### 🎨 Table Rendering Quality
All data tables across all tabs (leaderboards, venue matrices, comparison tables, raw data preview) are rendered as custom styled HTML cards featuring:
- Clean white card background
- Light grey header row
- Zebra-striped alternating rows
- Right-aligned formatted numeric columns (percentages with `%`, formatted decimals, commas for large integers)

---

## 🛠️ Setup & Running Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Launch Streamlit Dashboard**:
   ```bash
   streamlit run app.py
   ```

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
