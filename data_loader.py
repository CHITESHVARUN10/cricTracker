"""
data_loader.py — IPL Dataset loader
Verified column names directly from CSVs:
  Ball_By_Ball: ID, Innings, Overs, BallNumber, Batter, Bowler, NonStriker,
                ExtraType, BatsmanRun, ExtrasRun, TotalRun, IsWicketDelivery,
                PlayerOut, Kind, FieldersInvolved, BattingTeam
  Match_Info:   match_number, team1, team2, match_date, toss_winner,
                toss_decision, result, eliminator, winner, player_of_match,
                venue, city, team1_players, team2_players
"""

import streamlit as st
import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "IPL-DATASET", "csv")

@st.cache_data(show_spinner=False)
def load_matches():
    path = os.path.join(DATA_DIR, "Match_Info.csv")
    df = pd.read_csv(path)
    df["match_date"] = pd.to_datetime(df["match_date"], errors="coerce")
    df["season"] = df["match_date"].dt.year
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
