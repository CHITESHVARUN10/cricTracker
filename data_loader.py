"""
data_loader.py — IPL Dataset loader
Verified column names directly from CSVs:
  Ball_By_Ball: ID, Innings, Overs, BallNumber, Batter, Bowler, NonStriker,
                ExtraType, BatsmanRun, ExtrasRun, TotalRun, IsWicketDelivery,
                PlayerOut, Kind, FieldersInvolved, BattingTeam
  Match_Info:   match_number, team1, team2, match_date, toss_winner,
                toss_decision, result, eliminator, winner, player_of_match,
                venue, city, team1_players, team2_players

Venue names are canonicalized on load (see VENUE_CANONICAL) so stadiums
with multiple spellings/renames (Wankhede, Eden Gardens, Chinnaswamy,
Arun Jaitley/Feroz Shah Kotla, etc.) group together in the dashboard.
"""

import streamlit as st
import pandas as pd
import os

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = (
    os.path.join(BASE_DIR, "IPL-DATASET", "csv")
    if os.path.isdir(os.path.join(BASE_DIR, "IPL-DATASET", "csv"))
    else os.path.join(BASE_DIR, "IPL-DATASET")
)

# ── Venue canonicalization ─────────────────────────────────────────────────────
# Same stadium appears under multiple names/spellings across seasons
# (e.g. "Wankhede Stadium" vs "Wankhede Stadium, Mumbai"). Map every observed
# variant to one canonical display name so dropdowns and grouped stats line up.
VENUE_CANONICAL = {
    # Mumbai
    "Wankhede Stadium": "Wankhede Stadium, Mumbai",
    "Wankhede Stadium, Mumbai": "Wankhede Stadium, Mumbai",
    "Brabourne Stadium": "Brabourne Stadium, Mumbai",
    "Brabourne Stadium, Mumbai": "Brabourne Stadium, Mumbai",
    # Kolkata
    "Eden Gardens": "Eden Gardens, Kolkata",
    "Eden Gardens, Kolkata": "Eden Gardens, Kolkata",
    # Bengaluru
    "M Chinnaswamy Stadium": "M. Chinnaswamy Stadium, Bengaluru",
    "M.Chinnaswamy Stadium": "M. Chinnaswamy Stadium, Bengaluru",
    "M Chinnaswamy Stadium, Bengaluru": "M. Chinnaswamy Stadium, Bengaluru",
    "M.Chinnaswamy Stadium, Bengaluru": "M. Chinnaswamy Stadium, Bengaluru",
    "M Chinnaswamy Stadium, Bangalore": "M. Chinnaswamy Stadium, Bengaluru",
    "M.Chinnaswamy Stadium, Bangalore": "M. Chinnaswamy Stadium, Bengaluru",
    "M. Chinnaswamy Stadium, Bengaluru": "M. Chinnaswamy Stadium, Bengaluru",
    "M. Chinnaswamy Stadium, Bangalore": "M. Chinnaswamy Stadium, Bengaluru",
    # Delhi (Feroz Shah Kotla renamed Arun Jaitley Stadium)
    "Feroz Shah Kotla": "Arun Jaitley Stadium, Delhi",
    "Feroz Shah Kotla, Delhi": "Arun Jaitley Stadium, Delhi",
    "Arun Jaitley Stadium": "Arun Jaitley Stadium, Delhi",
    "Arun Jaitley Stadium, Delhi": "Arun Jaitley Stadium, Delhi",
    # Ahmedabad (Sardar Patel renamed Narendra Modi Stadium)
    "Sardar Patel Stadium, Motera": "Narendra Modi Stadium, Ahmedabad",
    "Narendra Modi Stadium": "Narendra Modi Stadium, Ahmedabad",
    "Narendra Modi Stadium, Ahmedabad": "Narendra Modi Stadium, Ahmedabad",
    # Chennai
    "MA Chidambaram Stadium": "MA Chidambaram Stadium, Chennai",
    "M.A. Chidambaram Stadium": "MA Chidambaram Stadium, Chennai",
    "MA Chidambaram Stadium, Chepauk": "MA Chidambaram Stadium, Chennai",
    "MA Chidambaram Stadium, Chennai": "MA Chidambaram Stadium, Chennai",
    "MA Chidambaram Stadium, Chepauk, Chennai": "MA Chidambaram Stadium, Chennai",
    "M. A. Chidambaram Stadium, Chepauk": "MA Chidambaram Stadium, Chennai",
    # Jaipur
    "Sawai Mansingh Stadium": "Sawai Mansingh Stadium, Jaipur",
    "Sawai Mansingh Stadium, Jaipur": "Sawai Mansingh Stadium, Jaipur",
    # Hyderabad (same ground, "Uppal" vs "Hyderabad")
    "Rajiv Gandhi International Stadium, Uppal": "Rajiv Gandhi International Stadium, Hyderabad",
    "Rajiv Gandhi International Stadium, Hyderabad": "Rajiv Gandhi International Stadium, Hyderabad",
    "Rajiv Gandhi International Stadium": "Rajiv Gandhi International Stadium, Hyderabad",
    "Rajiv Gandhi International Stadium, Uppal, Hyderabad": "Rajiv Gandhi International Stadium, Hyderabad",
    # Mohali / Chandigarh (PCA Stadium renamed IS Bindra Stadium)
    "Punjab Cricket Association Stadium, Mohali": "Punjab Cricket Association IS Bindra Stadium, Chandigarh",
    "Punjab Cricket Association IS Bindra Stadium": "Punjab Cricket Association IS Bindra Stadium, Chandigarh",
    "Punjab Cricket Association IS Bindra Stadium, Chandigarh": "Punjab Cricket Association IS Bindra Stadium, Chandigarh",
    "Punjab Cricket Association IS Bindra Stadium, Mohali": "Punjab Cricket Association IS Bindra Stadium, Chandigarh",
    "Punjab Cricket Association IS Bindra Stadium, Mohali, Chandigarh": "Punjab Cricket Association IS Bindra Stadium, Chandigarh",
    # Pune (Subrata Roy Sahara Stadium renamed MCA Stadium)
    "Subrata Roy Sahara Stadium": "Maharashtra Cricket Association Stadium, Pune",
    "Maharashtra Cricket Association Stadium": "Maharashtra Cricket Association Stadium, Pune",
    "Maharashtra Cricket Association Stadium, Pune": "Maharashtra Cricket Association Stadium, Pune",
    # Navi Mumbai (DY Patil Sports Academy)
    "Dr DY Patil Sports Academy": "Dr DY Patil Sports Academy, Mumbai",
    "Dr DY Patil Sports Academy, Mumbai": "Dr DY Patil Sports Academy, Mumbai",
    "Dr. DY Patil Sports Academy": "Dr DY Patil Sports Academy, Mumbai",
    "Dr. DY Patil Sports Academy, Mumbai": "Dr DY Patil Sports Academy, Mumbai",
    # Raipur
    "Shaheed Veer Narayan Singh International Stadium": "Shaheed Veer Narayan Singh International Stadium, Raipur",
    "Shaheed Veer Narayan Singh International Stadium, Raipur": "Shaheed Veer Narayan Singh International Stadium, Raipur",
    # Dharamsala
    "Himachal Pradesh Cricket Association Stadium": "Himachal Pradesh Cricket Association Stadium, Dharamsala",
    "Himachal Pradesh Cricket Association Stadium, Dharamsala": "Himachal Pradesh Cricket Association Stadium, Dharamsala",
    # UAE venues
    "Sheikh Zayed Stadium": "Sheikh Zayed Stadium, Abu Dhabi",
    "Sheikh Zayed Stadium, Abu Dhabi": "Sheikh Zayed Stadium, Abu Dhabi",
    "Zayed Cricket Stadium, Abu Dhabi": "Sheikh Zayed Stadium, Abu Dhabi",
    "Zayed Cricket Stadium": "Sheikh Zayed Stadium, Abu Dhabi",
    "Dubai International Cricket Stadium": "Dubai International Cricket Stadium, Dubai",
    "Dubai International Cricket Stadium, Dubai": "Dubai International Cricket Stadium, Dubai",
    "Dubai International Cricket Stadium, NA": "Dubai International Cricket Stadium, Dubai",
    "Sharjah Cricket Stadium": "Sharjah Cricket Stadium, Sharjah",
    "Sharjah Cricket Stadium, Sharjah": "Sharjah Cricket Stadium, Sharjah",
    "Sharjah Cricket Stadium, NA": "Sharjah Cricket Stadium, Sharjah",
    # Visakhapatnam
    "Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium": "Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium, Visakhapatnam",
    "Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium, Visakhapatnam": "Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium, Visakhapatnam",
    # Rajkot
    "Saurashtra Cricket Association Stadium": "Saurashtra Cricket Association Stadium, Rajkot",
    "Saurashtra Cricket Association Stadium, Rajkot": "Saurashtra Cricket Association Stadium, Rajkot",
    # Cuttack
    "Barabati Stadium": "Barabati Stadium, Cuttack",
    "Barabati Stadium, Cuttack": "Barabati Stadium, Cuttack",
    # Kochi
    "Nehru Stadium": "Nehru Stadium, Kochi",
    "Nehru Stadium, Kochi": "Nehru Stadium, Kochi",
    # Ranchi
    "JSCA International Stadium Complex": "JSCA International Stadium Complex, Ranchi",
    "JSCA International Stadium Complex, Ranchi": "JSCA International Stadium Complex, Ranchi",
    # Guwahati
    "Barsapara Cricket Stadium": "Barsapara Cricket Stadium, Guwahati",
    "Barsapara Cricket Stadium, Guwahati": "Barsapara Cricket Stadium, Guwahati",
    # Lucknow
    "Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium": "Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium, Lucknow",
    "Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium, Lucknow": "Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium, Lucknow",
    # Mullanpur / New Chandigarh (New PCA stadium)
    "Maharaja Yadavindra Singh International Cricket Stadium, Mullanpur": "Maharaja Yadavindra Singh International Cricket Stadium, Mullanpur",
    "Maharaja Yadavindra Singh International Cricket Stadium": "Maharaja Yadavindra Singh International Cricket Stadium, Mullanpur",
    "Maharaja Yadavindra Singh International Cricket Stadium, New Chandigarh": "Maharaja Yadavindra Singh International Cricket Stadium, Mullanpur",
}

def normalize_venues(df):
    """Map venue strings to canonical names so duplicate stadiums group correctly."""
    df = df.copy()
    if "venue" in df.columns:
        df["venue"] = df["venue"].astype(str).str.strip().map(
            lambda v: VENUE_CANONICAL.get(v, v)
        )
    return df

@st.cache_data(show_spinner=False)
def load_matches():
    path = os.path.join(DATA_DIR, "Match_Info.csv")
    df = pd.read_csv(path)
    df["match_date"] = pd.to_datetime(df["match_date"], errors="coerce")
    df["season"] = df["match_date"].dt.year
    df = normalize_venues(df)
    return df

@st.cache_data(show_spinner=False)
def load_balls():
    path = os.path.join(DATA_DIR, "Ball_By_Ball_Match_Data.csv")
    df = pd.read_csv(path)
    return df

@st.cache_data(show_spinner=False)
def load_players():
    path = os.path.join(DATA_DIR, "2024_players_details.csv")
    return pd.read_csv(path)

@st.cache_data(show_spinner=False)
def load_teams():
    path = os.path.join(DATA_DIR, "teams_info.csv")
    return pd.read_csv(path)
