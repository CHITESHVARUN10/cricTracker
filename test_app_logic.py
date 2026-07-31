import sys
import pandas as pd
from data_loader import load_ipl_data, get_filtered_data
from style_utils import render_styled_table

print("1. Testing data loader...")
df_matches, df_deliveries, df_players, df_teams = load_ipl_data()
print(f" Matches: {len(df_matches)}")
print(f" Deliveries: {len(df_deliveries)}")
print(f" Players: {len(df_players)}")

print("\n2. Testing filter engine...")
m_filt, d_filt = get_filtered_data(df_matches, df_deliveries, season_range=(2015, 2024), selected_venue="All", selected_team="All")
print(f" Filtered Matches (2015-2024): {len(m_filt)}")

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
