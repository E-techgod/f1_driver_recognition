# dashboard.py (upgraded with driver cards and logos)
import os
import requests
import pandas as pd
import streamlit as st
from datetime import datetime
from driverInfo import driver_info
from driverRatioChart import render_podium_rate
from driverStatisticsChart import render_driver_wins
from driverStatisticsChart import render_driver_DNFs
from driverStatisticsChart import render_driver_podiums
from driverRatioChart import render_overall_driver_score
from driverRatioChart import render_pole_conversion_rate   
from driverRatioChart import render_points_conversion_rate
from driverStatisticsChart import render_driver_fastes_laps
from driverRatioChart import render_finished_conversion_rate
from driverStatisticsChart import render_driver_total_points
from driverStatisticsChart import render_driver_pole_position
from driverStatisticsChart import render_driver_championships
from driverStatisticsChart import render_current_season_standings
from driverStatisticsChart import render_driver_total_number_of_races


st.set_page_config(page_title="F1 Dashboard", layout="wide")
st.title("🏁 F1 Driver Fantasy Score")
port= 8505
# Auto-refresh every 10 seconds
#st.markdown("<meta http-equiv='refresh' content='10'>", unsafe_allow_html=True)

# Add refresh button and last updated label
if st.button("🔁 Refresh Now"):
    st.rerun()

st.caption(f"⏳ Last updated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# API endpoint
url = "http://localhost:5006/attendance"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    if data:
        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values("timestamp", ascending=False)
        df.index = df.index + 1
       


        st.subheader("📝 Check-in Table")
        st.dataframe(df, use_container_width=True)
        
        st.subheader("🏎️ Driver Cards")
        render_current_season_standings(df, driver_info)
        render_driver_championships(df, driver_info)
        render_driver_wins(df, driver_info)
        render_driver_pole_position(df, driver_info)
        render_driver_podiums(df, driver_info)
        render_driver_fastes_laps(df, driver_info)
        render_driver_total_number_of_races(df, driver_info)
        render_driver_total_points(df, driver_info)
        render_driver_DNFs(df, driver_info)
        render_pole_conversion_rate(df, driver_info)
        render_podium_rate(df, driver_info)
        render_finished_conversion_rate(df, driver_info)
        render_points_conversion_rate(df, driver_info)
        render_overall_driver_score(df, driver_info)

    else:
        st.info("No attendance records yet.")
else:
    st.error("❌ Failed to fetch data from API.")
