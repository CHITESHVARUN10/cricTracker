import sys
import pandas as pd
from data_loader import load_matches, load_balls, load_players, load_teams
from style_utils import render_styled_table

print("1. Testing data loader...")
df_matches = load_matches()
df_deliveries = load_balls()
df_players = load_players()
df_teams = load_teams()
print(f" Matches: {len(df_matches)}")
print(f" Deliveries: {len(df_deliveries)}")
print(f" Players: {len(df_players)}")
print(f" Teams: {len(df_teams)}")

print("\n3. Testing table rendering logic...")
sample_df = pd.DataFrame([
    {'Batter': 'Virat Kohli', 'Runs': 741, 'Balls': 479, 'SR': 154.69, '4s': 64, '6s': 38},
    {'Batter': 'Rohit Sharma', 'Runs': 602, 'Balls': 406, 'SR': 148.27, '4s': 71, '6s': 24}
])
try:
    render_styled_table(sample_df, align_right_cols=['Runs', 'Balls', 'SR', '4s', '6s'])
    print(" Styled table rendering passed successfully.")
except Exception as e:
    print(f" Error rendering table: {e}")
    sys.exit(1)

print("\nALL VERIFICATION TESTS PASSED SUCCESSFULLY!")
