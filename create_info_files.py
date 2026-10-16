import os

content = """# IPL Match Insights Dashboard

## 📌 Project Overview
- **Title:** IPL Match Insights Dashboard
- **Slug:** `ipl-match-insights-dashboard`
- **Short Description (1 Line):** An interactive cricket data analytics dashboard delivering deep match insights, toss impact, venue statistics, team comparisons, and player matchups from historical IPL data.
- **Published:** true
- **Featured:** true
- **Live URL:** http://localhost:8501
- **GitHub Repository:** https://github.com/CHITESHVARUN10/cricTracker
- **Demo Credentials:** None required (Public analytics dashboard)

---

## 📖 Full Description
The **IPL Match Insights Dashboard** is a comprehensive, production-grade sports analytics web application built with **Python**, **Streamlit**, **Pandas**, and **Plotly**. Designed to transform raw, multi-gigabyte historical ball-by-ball cricket data into actionable tactical intelligence, the dashboard processes over **1,240+ IPL matches** and **295,000+ individual deliveries** spanning from the tournament's inception in 2008 through the 2024 season.

Engineered with a tailored, terracotta-themed visual design system inspired by Google Stitch UI tokens (`#a33d23` primary, `#e76f51` primary-container, `#006a60` secondary teal, `#f9f9ff` surface background), the application delivers 8 dedicated analytical modules, real-time slice-and-dice sidebar filtering, and custom-styled HTML data tables with zebra striping, monospace numeric formatting, and metric sorting.

---

## 🎯 Motivation
Modern T20 cricket has evolved into an intensely data-driven sport where tactical decisions—such as whether to bat first at specific venues, how to allocate bowling resources across match phases, or exploiting batter-bowler head-to-head match-ups—directly determine match outcomes. 

This project was conceived and engineered to:
1. Provide analysts, coaches, and cricket enthusiasts with instant, sub-second visual querying across 17 seasons of IPL data.
2. Uncover counter-intuitive trends (e.g., how toss decisions correlate with win percentages at distinct venues like Chepauk vs. Wankhede).
3. Deliver a professional, polished user experience that bridges the gap between raw data science scripts and interactive, executive-ready dashboard interfaces.

---

## 🏗️ Build Process & Architecture
The dashboard is structured around a high-performance modular pipeline:

1. **High-Performance Data Ingestion & Memory Caching:**
   - Sourced from the verified, MIT-licensed [ritesh-ojha/IPL-DATASET](https://github.com/ritesh-ojha/IPL-DATASET) repository.
   - Leveraged Streamlit's `@st.cache_data` decorators to load and index 295k+ ball records and 1.2k+ match summaries in memory, enabling instant filter updates without redundant disk reads.

2. **Data Pipeline & Vectorized Aggregation Engine:**
   - Implemented vectorized Pandas algorithms for custom cricket metrics: Batting Strike Rates, Bowling Economies, Phase Slicing (Powerplay: overs 1–6, Middle: overs 7–15, Death: overs 16–20), Venue Win Ratios, and Head-to-Head Batter vs. Bowler interaction matrices.

3. **Design System & Visual Styling (Stitch UI Tokens):**
   - Injected custom CSS rules via `st.markdown(unsafe_allow_html=True)` to replicate Google Stitch tokens pixel-for-pixel:
     - **Typography:** Google Fonts (`Archivo Narrow` for headlines, `Plus Jakarta Sans` for body text, `JetBrains Mono` for metric labels and data numbers).
     - **Color Tokens:** Deep Terracotta (`#a33d23`), Coral Accent (`#e76f51`), Deep Teal (`#006a60`), Light Sky Blue (`#8cf5e4`), and Warm White background gradients.
     - **Ambient Drop Shadows:** `0px 4px 20px rgba(231, 111, 81, 0.08)` for elevation and visual depth.

4. **Custom Table Component Renderer:**
   - Replaced default Streamlit tables with bespoke HTML/CSS table containers featuring custom header gradients, hover highlights (`rgba(163,61,35,0.05)`), monospace data alignment, and automatic percentage formatting.

---

## 💡 Lessons Learned
- **Large Dataset Optimization in Python:** Utilizing categorical typing and memoized aggregation functions prevents UI thread stalls when dynamically querying across hundreds of thousands of ball events.
- **Design Tokens & CSS in Streamlit:** Discovered effective patterns for overriding default Streamlit container styles to achieve a distinct brand identity without third-party frontend wrappers.
- **Cricket Analytics Domain Nuances:** Handling boundary cases in cricket statistics (e.g., super overs, no-result rain abandonments, wide/no-ball extras in economy calculation, undefeated batsman average calculations).

---

## 🛠️ Languages & Tech Stack
- **Languages:** Python (Core logic & data processing), HTML5 (Custom markup), CSS3 (Tokens, animations, gradients), JavaScript
- **Frameworks & Libraries:** 
  - `Streamlit` (Web framework & state management)
  - `Pandas` (Data manipulation & indexing)
  - `NumPy` (Vectorized calculations)
  - `Plotly Graph Objects & Express` (Interactive chart rendering)
- **Design Tokens & UI:** Google Stitch Design System, Tailwind CSS token injection, Material Symbols Outlined, Google Fonts (Archivo Narrow, Plus Jakarta Sans, JetBrains Mono)
- **Dataset:** IPL Historical Ball-by-Ball & Match Info Dataset (MIT License)

---

## 🌟 Key Features
1. **Global Hero Banner & KPI Bar:** Live summary cards for Total Matches (1,243+), Venues (60+), Active Franchises (19), Batting-First Win % (44%), and Average 1st Innings Runs (168).
2. **Overview (Match Outcome Snapshot):** Win-type distribution (Runs vs. Wickets vs. Ties), annual match volume trends (2008–2024), and venue win-rate bar charts.
3. **Toss Analytics Engine:** Deep dive into coin-toss win influence, win probability when choosing to bat vs. field first, and historical decision distributions.
4. **Venue Impact Profiler:** Ground-specific analysis featuring win split ratios (batting first vs. chasing), average scoring benchmarks, and top 10 ground run scorers.
5. **Team Performance Matrix:** Franchise performance metrics, win rates sliced by innings context (defending vs. chasing), and season-by-season victory progressions.
6. **Player Leaders & Head-to-Head Comparison:** Dual-player comparison tool (Runs, Strike Rate, Average, 4s, 6s, Wickets, Economy) alongside Top 10 Batting and Bowling leaderboards.
7. **Insights Lab (Advanced Analytics Hub):** Multi-venue deep dive matrix, team head-to-head comparison tool, and single-player multi-season form tracker with recent innings logs.
8. **Phase-by-Phase Breakdown:** Over-by-over analysis comparing Powerplay (overs 1–6), Middle Overs (overs 7–15), and Death Overs (overs 16–20) run rates, wickets fallen, and scoring acceleration curves.
9. **Batter vs. Bowler Matchup Tool:** Head-to-head tactical query engine displaying total runs scored, balls faced, boundary counts, dot balls, dismissals, and runs-off-bat distribution histograms (0, 1, 2, 3, 4, 6).
10. **Interactive Slice-and-Dice Sidebar Filters:** Dynamic season sliders (2008–2024), venue dropdowns, and franchise selectors that propagate instantly across all 8 tabs.
11. **Raw Data Preview Expander:** Paginated, formatted data table displaying raw match details and winners.

---

## 📅 Timeline & Metadata
- **Start Date:** 2024-03-01
- **End Date:** 2024-05-15
- **Is Ongoing:** false
- **Is Hackathon Project:** false
- **Hackathon Details:** N/A

---

## 📸 Screenshots Catalog
All screenshots are saved in Full HD (1920x1080) high resolution under `screenshots/`:

| Filename | Description | Category |
| :--- | :--- | :--- |
| `01_portfolio_hero_featured_card.png` | Portfolio Website Hero with Featured IPL Dashboard Card | Portfolio |
| `02_portfolio_projects_section_bento.png` | Portfolio Projects Section Bento Card for IPL Dashboard | Portfolio |
| `03_portfolio_project_detail_header.png` | Portfolio Project Detail Page Header & Actions | Portfolio |
| `04_portfolio_project_detail_fullpage.png` | Full-page View of IPL Dashboard Project Detail Page | Portfolio |
| `05_app_overview_fullpage.png` | IPL Dashboard Global Overview & Outcome Snapshot | Live App |
| `06_app_toss_tab.png` | Toss Impact Analytics & Decision Win Rates | Live App |
| `07_app_venue_tab.png` | Venue Deep Dive & Scoring Profiles | Live App |
| `08_app_teams_tab.png` | Team Performance & Season Win Trends | Live App |
| `09_app_players_tab.png` | Player Leaders & Head-to-Head Comparison | Live App |
| `10_app_insights_lab_tab.png` | Insights Lab Analytics Matrix & Player Form Tracker | Live App |
| `11_app_phases_tab.png` | Phase-by-Phase Analysis (Powerplay, Middle, Death) | Live App |
| `12_app_matchups_tab.png` | Batter vs Bowler Head-to-Head Matchup Tool | Live App |

---

## 🎬 YouTube Video Plan (2–3 Minutes)
*To be recorded for the portfolio video demo section:*

- **Duration:** 2 Minutes 30 Seconds
- **Structure & Timestamp Breakdown:**
  - **[0:00 - 0:25] Introduction & Problem Context:** Quick introduction of the project, problem statement (making 295k+ ball records interactive and tactical), and high-level tech stack (Python, Streamlit, Plotly, Stitch design tokens).
  - **[0:25 - 0:50] Overview & Global KPI Bar:** Showcasing the live KPI metrics, dynamic season filtering from the sidebar, and match outcome distribution charts.
  - **[0:50 - 1:15] Toss Analytics & Venue Deep Dive:** Demonstrating the impact of toss decisions at grounds like Chepauk vs. Wankhede, explaining the win split charts.
  - **[1:15 - 1:45] Phases & Player Matchup Tool:** Live interaction selecting Virat Kohli vs. Sunil Narine in the Matchup tool, inspecting the ball-by-ball run distribution and dismissal history.
  - **[1:45 - 2:10] Insights Lab & Player Form Tracker:** Walking through multi-season form curves and recent innings breakdowns.
  - **[2:10 - 2:30] Outro & Links:** Summary of key technical learnings, invitation to explore the live repository, and GitHub/LinkedIn contact callouts.

---

## 📬 Contact Information
- **GitHub:** [https://github.com/CHITESHVARUN10](https://github.com/CHITESHVARUN10)
- **LinkedIn:** [https://www.linkedin.com/in/chitesh-varun-9032542b9/](https://www.linkedin.com/in/chitesh-varun-9032542b9/)
- **Email:** *Available upon request / Contact via Portfolio Website*

---

## 📋 Screenshots Required Checklist
- **Screenshots Taken (12):**
  - ✅ `01_portfolio_hero_featured_card.png` (Portfolio Hero Featured Card)
  - ✅ `02_portfolio_projects_section_bento.png` (Portfolio Projects Bento Section)
  - ✅ `03_portfolio_project_detail_header.png` (Portfolio Detail Header)
  - ✅ `04_portfolio_project_detail_fullpage.png` (Portfolio Detail Full Page)
  - ✅ `05_app_overview_fullpage.png` (App Overview Tab)
  - ✅ `06_app_toss_tab.png` (App Toss Tab)
  - ✅ `07_app_venue_tab.png` (App Venue Tab)
  - ✅ `08_app_teams_tab.png` (App Teams Tab)
  - ✅ `09_app_players_tab.png` (App Players Tab)
  - ✅ `10_app_insights_lab_tab.png` (App Insights Lab Tab)
  - ✅ `11_app_phases_tab.png` (App Phases Tab)
  - ✅ `12_app_matchups_tab.png` (App Matchups Tab)
- **Waiting for Manual Upload (0):** None required — all web dashboard screens and portfolio cards were automatically captured in Full HD (1920x1080).
- **Screenshots Not Required:** Mobile native app screens (this project is an optimized desktop/tablet responsive web analytics application).
"""

destinations = [
    "/Users/chiteshvarun/D-drive/project info/IPL Match Insights Dashboard",
    "/Users/chiteshvarun/D-drive/projects/IPL Match Insights Dashboard"
]

for d in destinations:
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "README.md"), "w", encoding="utf-8") as f:
        f.write(content)
    with open(os.path.join(d, "README.txt"), "w", encoding="utf-8") as f:
        f.write(content)
    print("Successfully written to:", d)
