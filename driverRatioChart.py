import math
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px
from scipy.ndimage import zoom
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


# Load your logo image
ROOT_DIR = Path(__file__).resolve().parent
logo_path = ROOT_DIR / "data" / "logos" / "f1.png"
logo_img = mpimg.imread(logo_path)

# Resize the logo image
logo_resized = zoom(logo_img, (0.7, 0.7, 1))  # height %, width %, channels (unchanged)

plt.rcParams["font.family"] = "monospace"

def render_pole_conversion_rate(df, driver_info):
    winner_data = []
    for driver in df['driver_name'].unique():
        info = driver_info.get(driver, "")
        wins_from_pole = pole = None

        if isinstance(info, str):
            for line in info.splitlines():
                if line.startswith("Wins from Pole:"):
                    try:
                        wins_from_pole = int(line.split(":")[1].strip())
                    except ValueError:
                        pass
                elif line.startswith("GP Pole Positions:"):
                    try:
                        pole = int(line.split(":")[1].strip())
                    except ValueError:
                        pass
        if pole is not None and pole > 0 and wins_from_pole is not None:
            rate = (wins_from_pole / pole) 
        elif pole == 0:
            rate = 0.0  # No podiums = 0% conversion
        else:
            continue  # Missing data or irrelevant case
        winner_data.append({"driver_name": driver, "conversion_rate": rate})

    if winner_data:
        st.subheader("🔥 Pole-to-Win Conversion Rate")

        df_rate = pd.DataFrame(winner_data).sort_values("conversion_rate", ascending=True)

        fig, ax = plt.subplots(figsize=(10, 4))
        fig.patch.set_facecolor('#333333')
        ax.set_facecolor('#444444')

        bars = ax.barh(df_rate["driver_name"], df_rate["conversion_rate"], 
                       color="black", edgecolor="cyan", linewidth=1.5, height=0.5)

        for bar in bars:
            width = bar.get_width()
            offset = max(df_rate["conversion_rate"]) * 0.01
            label = f"{width * 100:.1f}%"
            ax.text(width + offset, bar.get_y() + bar.get_height() / 2,
                    label, va='center', ha='left', fontsize=10, color="white")
            
        # Add logo to the top left corner
        # Add logo in a small inset axes
        # Add logo as inset axes in top-left corner
        logo_ax = fig.add_axes([0.01, 0.82, 0.12, 0.15])  # [left, bottom, width, height] in relative figure coords
        logo_ax.imshow(logo_img)
        logo_ax.axis('off')

        ax.set_xlabel(" Pole-Win Ratio", color="white")
        ax.set_title("Conversion Rate: How Often Pole Become Wins", fontsize=13, color='white')
        ax.tick_params(colors='white')
        ax.grid(axis='x', linestyle='--', alpha=0.5)
        st.pyplot(fig)

def render_podium_rate(df, driver_info):
    winner_data = []
    for driver in df['driver_name'].unique():
        info = driver_info.get(driver, "")
        wins = podiums = None

        if isinstance(info, str):
            for line in info.splitlines():
                if line.startswith("Podiums:"):
                    try:
                        podiums = int(line.split(":")[1].strip())
                    except ValueError:
                        pass
                elif line.startswith("Number of races:"):
                    try:
                        races = int(line.split(":")[1].strip())
                    except ValueError:
                        pass

        if races is not None and races > 0 and podiums is not None:
            rate = (podiums / races) * 100
        elif podiums == 0:
            rate = 0.0  # No podiums = 0% conversion
        else:
            continue  # Missing data or irrelevant case

        # if rate is not none
        winner_data.append({"driver_name": driver, "conversion_rate": rate})

    if winner_data:
        st.subheader("🥇 Podium Rate")

        df_rate = pd.DataFrame(winner_data).sort_values("conversion_rate", ascending=True)

        fig, ax = plt.subplots(figsize=(10, 4))
        fig.patch.set_facecolor('#333333')
        ax.set_facecolor('#444444')

        bars = ax.barh(df_rate["driver_name"], df_rate["conversion_rate"], 
                       color="black", edgecolor="cyan", linewidth=1.5, height=0.5)

        for bar in bars:
            width = bar.get_width()
            offset = max(df_rate["conversion_rate"]) * 0.01
            label = f"{width:.2f}%"
            ax.text(width + offset, bar.get_y() + bar.get_height() / 2,
                    label, va='center', ha='left', fontsize=10, color="white")
            
        # Add logo to the top left corner
        # Add logo in a small inset axes
        # Add logo as inset axes in top-left corner
        logo_ax = fig.add_axes([0.01, 0.82, 0.12, 0.15])  # [left, bottom, width, height] in relative figure coords
        logo_ax.imshow(logo_img)
        logo_ax.axis('off')

        ax.set_xlabel("Podium Rate", color="white")
        ax.set_title("Conversion Rate: How Often driver gets a podium", fontsize=13, color='white')
        ax.tick_params(colors='white')
        ax.grid(axis='x', linestyle='--', alpha=0.5)
        st.pyplot(fig)

def render_finished_conversion_rate(df, driver_info):
    data = []

    for driver in df['driver_name'].unique():
        info = driver_info.get(driver, "")
        races = dnfs = None

        if isinstance(info, str):
            for line in info.splitlines():
                if line.startswith("Number of races:"):
                    try:
                        races = int(line.split(":")[1].strip())
                    except ValueError:
                        pass
                elif line.startswith("Retirements (DNFs):"):
                    try:
                        dnfs = int(line.split(":")[1].strip())
                    except ValueError:
                        pass

        if races and races > 0 and dnfs is not None:
            races_finished= races - dnfs
            finish_rate = races_finished / races
            data.append({"driver_name": driver, "finish_rate": finish_rate})

    if data:
        st.subheader("🛡️ Race Finish Rate (Consistency)")

        df_finish = pd.DataFrame(data).sort_values("finish_rate", ascending=True)

        fig, ax = plt.subplots(figsize=(10, 4))
        fig.patch.set_facecolor('#333333')
        ax.set_facecolor('#444444')

        bars = ax.barh(df_finish["driver_name"], df_finish["finish_rate"],
                       color="black", edgecolor="cyan", linewidth=1.5, height=0.5)

        for bar in bars:
            width = bar.get_width()
            offset = max(df_finish["finish_rate"]) * 0.01
            ax.text(width + offset, bar.get_y() + bar.get_height() / 2,
                    f"{width:.2%}", va='center', ha='left', fontsize=10, color="white")
            
        # Add logo to the top left corner
        # Add logo in a small inset axes
        # Add logo as inset axes in top-left corner
        logo_ax = fig.add_axes([0.01, 0.82, 0.12, 0.15])  # [left, bottom, width, height] in relative figure coords
        logo_ax.imshow(logo_img)
        logo_ax.axis('off')

        ax.set_xlabel("Finish Rate", color="white")
        ax.set_title("Race Completion Consistency", color="white")
        ax.tick_params(colors='white')
        ax.grid(axis='x', linestyle='--', alpha=0.5)

        st.pyplot(fig)

    
def render_points_conversion_rate(df, driver_info):
    data = []

    for driver in df['driver_name'].unique():
        info = driver_info.get(driver, "")
        points = races = None

        if isinstance(info, str):
            for line in info.splitlines():
                if line.startswith("Total Points:"):
                    try:
                        points = float(line.split(":")[1].strip())
                    except ValueError:
                        pass
                elif line.startswith("Number of races:"):
                    try:
                        races = int(line.split(":")[1].strip())
                    except ValueError:
                        pass

        if points is not None and races and races > 0:
            conversion = points / races
            data.append({"driver_name": driver, "points_per_race": conversion})

    if data:
        st.subheader("🎯 Points Conversion Rate (Points per Race)")

        df_conv = pd.DataFrame(data).sort_values("points_per_race", ascending=True)

        fig, ax = plt.subplots(figsize=(10, 4))
        fig.patch.set_facecolor('#333333')
        ax.set_facecolor('#444444')

        bars = ax.barh(df_conv["driver_name"], df_conv["points_per_race"],
                       color="black", edgecolor="cyan", linewidth=1.5, height=0.5)

        for bar in bars:
            width = bar.get_width()
            offset = max(df_conv["points_per_race"]) * 0.01
            ax.text(width + offset, bar.get_y() + bar.get_height() / 2,
                    f"{width:.2f}", va='center', ha='left', fontsize=10, color="white")
        
         # Add logo to the top left corner
        # Add logo in a small inset axes
        # Add logo as inset axes in top-left corner
        logo_ax = fig.add_axes([0.01, 0.82, 0.12, 0.15])  # [left, bottom, width, height] in relative figure coords
        logo_ax.imshow(logo_img)
        logo_ax.axis('off')

        ax.set_xlabel("Avg Points per Race", color="white")
        ax.set_title("Driver Efficiency: Points Conversion Rate", color="white")
        ax.tick_params(colors='white')
        ax.grid(axis='x', linestyle='--', alpha=0.5)

        st.pyplot(fig)

def render_overall_driver_score(df, driver_info):
    st.subheader("🏁 Overall Driver Performance Score")
    st.caption("ℹ️ Ties in score were resolved using the driver's Win Ratio as a tiebreaker.")
    data = []
    for driver in df['driver_name'].unique():
        info = driver_info.get(driver, "")
        wins = poles = podiums = points = dnfs = races = wins_from_pole = fastest_laps = None

        if isinstance(info, str):
            for line in info.splitlines():
                if line.startswith("Wins:"):
                    wins = int(line.split(":")[1].strip())
                elif line.startswith("Wins from Pole:"):
                    wins_from_pole = int(line.split(":")[1].strip())
                elif line.startswith("GP Pole Positions:"):
                    poles = int(line.split(":")[1].strip())
                elif line.startswith("Podiums:"):
                    podiums = int(line.split(":")[1].strip())
                elif line.startswith("Total Points:"):
                    points = float(line.split(":")[1].strip())
                elif line.startswith("Retirements (DNFs):"):
                    dnfs = int(line.split(":")[1].strip())
                elif line.startswith("Number of races:"):
                    races = int(line.split(":")[1].strip())
                elif line.startswith("Fastest Laps:"):
                    fastest_laps = int(line.split(":")[1].strip())

        if None in (wins, poles, podiums, points, dnfs, races, wins_from_pole, fastest_laps) or races == 0:
            continue

        win_rate = wins / races if races > 0 else 0
        points_per_race = points / races
        win_conversion = wins / podiums if podiums > 0 else 0
        pole_win_conversion = wins_from_pole / poles if poles > 0 else 0
        finish_rate = (races - dnfs) / races
        podium_rate = podiums / races if races > 0 else 0
        fastest_lap_rate = fastest_laps / races if races > 0 else 0

        # === Improved Fantasy Scoring Formula ===
        score = (
            (wins * 2.0) +
            (poles * 1.2) +
            (podiums * 0.7) +
            (points_per_race * 2.5) +
            (podium_rate * 1.5) +
            (win_conversion * 2.0) +
            (finish_rate * 10.0) +
            (pole_win_conversion * 1.5) +
            (fastest_lap_rate * 5.0) +
            (win_rate * 30.0) -
            (dnfs * 0.7)
        )

        import math
        career_length_factor = min(1.0, (1 + math.log1p(races / 50)))
        score *= career_length_factor

        data.append({
            "driver_name": driver,
            "raw_score": score,
            "wins": wins,
            "poles": poles,
            "podiums": podiums,
            "points/race": round(points_per_race, 2),
            "win_ratio": round(win_conversion, 3),
            "pole_win_ratio": round(pole_win_conversion, 3),
            "finish_rate": round(finish_rate, 3),
            "fastest_lap_rate": round(fastest_lap_rate, 3),
            "races": races
        })

    if data:
        df_scores = pd.DataFrame(data)

        q1 = df_scores["raw_score"].quantile(0.25)
        q3 = df_scores["raw_score"].quantile(0.75)
        iqr = q3 - q1

        if iqr > 0:
            df_scores["normalized_score"] = df_scores["raw_score"].apply(
                lambda x: min(100, max(0, (x - q1) / iqr * 25 + 50))
            ).round(1)
        else:
            df_scores["normalized_score"] = 50.0

        df_scores = df_scores.sort_values("normalized_score", ascending=False).reset_index(drop=True)
        df_scores= df_scores.sort_values(by=["normalized_score", "win_ratio"], ascending=[False, False])
                
        df_scores["strengths"] = df_scores.apply(get_strengths, axis=1)
        df_scores["weaknesses"] = df_scores.apply(get_weaknesses, axis=1)

        df_scores.index = df_scores.index + 1

        df_scores["strengths"] = df_scores["strengths"].apply(
            lambda s: s.replace("Race wins", "🏆 Race wins")
                    .replace("High scoring", "💰 High scoring")
                    .replace("Reliability", "🔧 Reliability")
                    .replace("Raw pace", "⚡ Raw pace")
        )

        df_scores["weaknesses"] = df_scores["weaknesses"].apply(
            lambda w: w.replace("Winning conversion", "📉 Low conversion")
                    .replace("DNFs", "💥 DNFs")
                    .replace("Scoring", "🪫 Low points")
        )
        
        st.dataframe(df_scores)

        top = df_scores.iloc[0]
        st.success(f"🏆 Top Driver: {top['driver_name']} — Fantasy Score: {top['normalized_score']} / 100")

        # Strengths section
        """
        st.subheader("🔍 Driver Strengths and Weaknesses")
        for _, row in df_scores.iterrows():
            st.markdown(f"### {row['driver_name']}")
            st.markdown(f"**Fantasy Score:** {row['normalized_score']} / 100")
            st.markdown(f"**Strengths:** {row['strengths']}")
            st.markdown(f"**Weaknesses:** {row['weaknesses']}")
            st.markdown("---")
        """

        # Add bar chart visualization
        st.subheader("📊 Driver Fantasy Score Chart")
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 4))
        fig.patch.set_facecolor('#333333')
        ax.set_facecolor('#444444')
        
        df_plot = df_scores.sort_values(by=["normalized_score", "win_ratio"], ascending=[False, False])
        bars = ax.barh(df_plot[::-1]["driver_name"], df_plot[::-1]["normalized_score"],
               color="black", edgecolor="cyan", linewidth=1.5, height=0.5)

        for bar in bars:
            width = bar.get_width()
            offset = max(df_scores["normalized_score"]) * 0.01
            ax.text(width + offset, bar.get_y() + bar.get_height() / 2,
                    f"{width:.1f}", va='center', ha='left', fontsize=10, color="white")

        # Add logo to the top left corner
        # Add logo in a small inset axes
        # Add logo as inset axes in top-left corner
        logo_ax = fig.add_axes([0.01, 0.82, 0.12, 0.15])  # [left, bottom, width, height] in relative figure coords
        logo_ax.imshow(logo_img)
        logo_ax.axis('off')

        ax.set_xlabel("Score (Out of 100)", color="white")
        ax.set_title("Fantasy Driver Performance Score", color="white")
        ax.tick_params(colors='white')
        ax.grid(axis='x', linestyle='--', alpha=0.5)

        st.pyplot(fig)

def get_strengths(row):
    strengths = []
    if row['win_ratio'] > 0.5:
        strengths.append("Race wins")
    if row['points/race'] > 10:
        strengths.append("High scoring")
    if row['finish_rate'] > 0.9:
        strengths.append("Reliability")
    if row['fastest_lap_rate'] > 0.1:
        strengths.append("Raw pace")
    return ", ".join(strengths) if strengths else "Balanced"

def get_weaknesses(row):
    weaknesses = []
    if row['win_ratio'] < 0.2 and row['podiums'] > 10:
        weaknesses.append("Winning conversion")
    if row['finish_rate'] < 0.8:
        weaknesses.append("DNFs")
    if row['points/race'] < 5:
        weaknesses.append("Scoring")
    return ", ".join(weaknesses) if weaknesses else "None significant"

