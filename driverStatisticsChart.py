from pathlib import Path

import pandas as pd
import streamlit as st
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

year= 2025

def render_current_season_standings(df, driver_info):
    data = []
    for driver in df['driver_name'].unique():
        info = driver_info.get(driver, "")
        season_points = None
        season_position = None

        if isinstance(info, str):
            for line in info.splitlines():
                if line.startswith("Season position {year}:"):
                    try:
                        season_position = float(line.split(":")[1].strip())
                    except ValueError:
                        pass
                elif line.startswith("Season points {year}:"):
                    try:
                        season_points = int(line.split(":")[1].strip())
                    except ValueError:
                        pass

        if season_points is not None and season_position is not None:
            data.append({
                "driver_name": driver,
                "season_points": season_points,
                "season_position": season_position
            })

    if data:
        df_standings = pd.DataFrame(data).sort_values("season_points", ascending=False)
        st.subheader("📆 Current 2025 Season Standings: Round 8- Monaco GP")
        df_standings.index = df_standings.index + 1
        # This adds a table 
        st.dataframe(df_standings, use_container_width=True)
        
        
        # Bar chart
        df_plot = df_standings.sort_values("season_points", ascending=True)
        fig, ax = plt.subplots(figsize=(10, 4))
        fig.patch.set_facecolor('#333333')
        ax.set_facecolor('#444444')

        bars = ax.barh(df_plot["driver_name"], df_plot["season_points"],
                       color="black", edgecolor="cyan", linewidth=1.5, height=0.5)

        for bar in bars:
            width = bar.get_width()
            ax.text(width + 2, bar.get_y() + bar.get_height() / 2,
                    f"{int(width)} pts", va='center', ha='left', fontsize=10, color="white")

        # Add logo to the top left corner
        # Add logo in a small inset axes
        # Add logo as inset axes in top-left corner
        logo_ax = fig.add_axes([0.01, 0.82, 0.12, 0.15])  # [left, bottom, width, height] in relative figure coords
        logo_ax.imshow(logo_img)
        logo_ax.axis('off')

        ax.set_xlabel("Points", color="white")
        ax.set_title("🏎️ 2025 Driver Points", color="white")
        ax.tick_params(colors='white')
        ax.grid(axis='x', linestyle='--', alpha=0.5)
        st.pyplot(fig)  


def render_driver_championships(df, driver_info):
    # Build DataFrame of drivers with podiums
    championships_data = []
    for driver in df['driver_name'].unique():
        info = driver_info.get(driver, "")
        total_championships = None

        if isinstance(info, str):
            for line in info.splitlines():
                if line.startswith("Championships:"):
                    try:
                        total_championships = int(line.split(":", 1)[1].strip())
                        break
                    except ValueError:
                        pass

        if total_championships is not None:
            championships_data.append({"driver_name": driver, "total_championships": total_championships})

    # Plot if data exists
    if championships_data:
        st.subheader("👑🏁 Drivers Championships")

        df_total_championships = pd.DataFrame(championships_data).sort_values("total_championships", ascending=True)

        # Plotting
        fig, ax = plt.subplots(figsize=(11, 4))
        fig.patch.set_facecolor('#333333') # background
        ax.set_facecolor('#444444') # inside
        
        bars = ax.barh(df_total_championships["driver_name"], df_total_championships["total_championships"], color="black", edgecolor="cyan", linewidth=1, height=0.5)

        # Add win count text to each bar
        for bar in bars:
            width = bar.get_width()
            offset = max(df_total_championships["total_championships"]) * 0.005  # 1% of max bar width
            ax.text(width + offset, bar.get_y() + bar.get_height() / 2,
                f"{int(width)}", va='center', ha='left', fontsize=10, color="white")

               
        # Add logo to the top left corner
        # Add logo in a small inset axes
        # Add logo as inset axes in top-left corner
        logo_ax = fig.add_axes([0.01, 0.82, 0.12, 0.15])  # [left, bottom, width, height] in relative figure coords
        logo_ax.imshow(logo_img)
        logo_ax.axis('off')

        
        ax.set_xlabel("Championships", color= "white")
        ax.set_title("F1 Drivers History Championships", fontsize=13, color='white')
        ax.grid(axis='x', linestyle='--', alpha=0.5)
        ax.tick_params(colors='white')
        st.pyplot(fig)

def render_driver_wins(df, driver_info):
    # Build DataFrame of drivers with wins
    wins_data = []
    for driver in df['driver_name'].unique():
        info = driver_info.get(driver, "")
        wins = None

        if isinstance(info, str):
            for line in info.splitlines():
                if line.startswith("Wins:"):
                    try:
                        wins = int(line.split(":", 1)[1].strip())
                        break
                    except ValueError:
                        pass

        if wins is not None:
            wins_data.append({"driver_name": driver, "wins": wins})

    # Plot if data exists
    if wins_data:
        st.subheader("🏆 Drivers wins")

        df_wins = pd.DataFrame(wins_data).sort_values("wins", ascending=True)

        # Plotting
        fig, ax = plt.subplots(figsize=(11, 4))
        fig.patch.set_facecolor('#333333')
        ax.set_facecolor('#444444')
        
        bars = ax.barh(df_wins["driver_name"], df_wins["wins"], color="black", edgecolor="cyan", linewidth=1, height=0.5)

        # Add win count text to each bar
        for bar in bars:
            width = bar.get_width()
            offset = max(df_wins["wins"]) * 0.01  # 1% of max bar width
            ax.text(width + offset, bar.get_y() + bar.get_height() / 2,
                f"{int(width)}", va='center', ha='left', fontsize=10, color="white")

               
        # Add logo to the top left corner
        # Add logo in a small inset axes
        # Add logo as inset axes in top-left corner
        logo_ax = fig.add_axes([0.01, 0.82, 0.12, 0.15])  # [left, bottom, width, height] in relative figure coords
        logo_ax.imshow(logo_img)
        logo_ax.axis('off')

        
        ax.set_xlabel("Wins", color= "white")
        ax.set_title("F1 Drivers History Wins", fontsize=13, color='white')
        ax.grid(axis='x', linestyle='--', alpha=0.5)
        ax.tick_params(colors='white')
        st.pyplot(fig)

def render_driver_pole_position(df, driver_info):
    # Build DataFrame of drivers with pole
    pole_position_data = []
    for driver in df['driver_name'].unique():
        info = driver_info.get(driver, "")
        pole = None

        if isinstance(info, str):
            for line in info.splitlines():
                if line.startswith("GP Pole Positions:"):
                    try:
                        pole = int(line.split(":", 1)[1].strip())
                        break
                    except ValueError:
                        pass

        if pole is not None:
            pole_position_data.append({"driver_name": driver, "pole": pole})

    # Plot if data exists
    if pole_position_data:
        st.subheader("🥇 Drivers pole")

        df_pole = pd.DataFrame(pole_position_data).sort_values("pole", ascending=True)

        # Plotting
        fig, ax = plt.subplots(figsize=(11, 4))
        fig.patch.set_facecolor('#333333')
        ax.set_facecolor('#444444')
        
        bars = ax.barh(df_pole["driver_name"], df_pole["pole"], color="black", edgecolor="cyan", linewidth=1, height=0.5)

        # Add win count text to each bar
        for bar in bars:
            width = bar.get_width()
            offset = max(df_pole["pole"]) * 0.01  # 1% of max bar width
            ax.text(width + offset, bar.get_y() + bar.get_height() / 2,
                f"{int(width)}", va='center', ha='left', fontsize=10, color="white")

               
        # Add logo to the top left corner
        # Add logo in a small inset axes
        # Add logo as inset axes in top-left corner
        logo_ax = fig.add_axes([0.01, 0.82, 0.12, 0.15])  # [left, bottom, width, height] in relative figure coords
        logo_ax.imshow(logo_img)
        logo_ax.axis('off')

        
        ax.set_xlabel("pole", color= "white")
        ax.set_title("F1 Drivers History pole", fontsize=13, color='white')
        ax.grid(axis='x', linestyle='--', alpha=0.5)
        ax.tick_params(colors='white')
        st.pyplot(fig)

def render_driver_podiums(df, driver_info):
    # Build DataFrame of drivers with podiums
    podiums_data = []
    for driver in df['driver_name'].unique():
        info = driver_info.get(driver, "")
        podiums = None

        if isinstance(info, str):
            for line in info.splitlines():
                if line.startswith("Podiums:"):
                    try:
                        podiums = int(line.split(":", 1)[1].strip())
                        break
                    except ValueError:
                        pass

        if podiums is not None:
            podiums_data.append({"driver_name": driver, "podiums": podiums})

    # Plot if data exists
    if podiums_data:
        st.subheader("🥇🥈🥉 Drivers Podiums")

        df_podiums = pd.DataFrame(podiums_data).sort_values("podiums", ascending=True)

        # Plotting
        fig, ax = plt.subplots(figsize=(11, 4))
        fig.patch.set_facecolor('#333333')
        ax.set_facecolor('#444444')
        
        bars = ax.barh(df_podiums["driver_name"], df_podiums["podiums"], color="black", edgecolor="cyan", linewidth=1, height=0.5)

        # Add win count text to each bar
        for bar in bars:
            width = bar.get_width()
            offset = max(df_podiums["podiums"]) * 0.01  # 1% of max bar width
            ax.text(width + offset, bar.get_y() + bar.get_height() / 2,
                f"{int(width)}", va='center', ha='left', fontsize=10, color="white")

               
        # Add logo to the top left corner
        # Add logo in a small inset axes
        # Add logo as inset axes in top-left corner
        logo_ax = fig.add_axes([0.01, 0.82, 0.12, 0.15])  # [left, bottom, width, height] in relative figure coords
        logo_ax.imshow(logo_img)
        logo_ax.axis('off')

        
        ax.set_xlabel("Podiums", color= "white")
        ax.set_title("F1 Drivers History Podiums", fontsize=13, color='white')
        ax.grid(axis='x', linestyle='--', alpha=0.5)
        ax.tick_params(colors='white')
        st.pyplot(fig)
    
def render_driver_fastes_laps(df, driver_info):
    # Build DataFrame of drivers with podiums
    DNFS_data = []
    for driver in df['driver_name'].unique():
        info = driver_info.get(driver, "")
        total_points = None

        if isinstance(info, str):
            for line in info.splitlines():
                if line.startswith("Fastest Laps:"):
                    try:
                        total_points = int(line.split(":", 1)[1].strip())
                        break
                    except ValueError:
                        pass

        if total_points is not None:
            DNFS_data.append({"driver_name": driver, "total_points": total_points})

    # Plot if data exists
    if DNFS_data:
        st.subheader("🚀 Drivers fastest Laps")

        df_total_points = pd.DataFrame(DNFS_data).sort_values("total_points", ascending=True)

        # Plotting
        fig, ax = plt.subplots(figsize=(11, 4))
        fig.patch.set_facecolor('#333333')
        ax.set_facecolor('#444444')
        
        bars = ax.barh(df_total_points["driver_name"], df_total_points["total_points"], color="black", edgecolor="cyan", linewidth=1, height=0.5)

        # Add win count text to each bar
        for bar in bars:
            width = bar.get_width()
            offset = max(df_total_points["total_points"]) * 0.01  # 1% of max bar width
            ax.text(width + offset, bar.get_y() + bar.get_height() / 2,
                f"{int(width)}", va='center', ha='left', fontsize=10, color="white")

               
        # Add logo to the top left corner
        # Add logo in a small inset axes
        # Add logo as inset axes in top-left corner
        logo_ax = fig.add_axes([0.01, 0.82, 0.12, 0.15])  # [left, bottom, width, height] in relative figure coords
        logo_ax.imshow(logo_img)
        logo_ax.axis('off')

        
        ax.set_xlabel("Fastest Laps", color= "white")
        ax.set_title("F1 Drivers History fastest Laps", fontsize=13, color='white')
        ax.grid(axis='x', linestyle='--', alpha=0.5)
        ax.tick_params(colors='white')
        st.pyplot(fig)

def render_driver_total_number_of_races(df, driver_info):
    # Build DataFrame of drivers with podiums
    races_data = []
    for driver in df['driver_name'].unique():
        info = driver_info.get(driver, "")
        total_races = None

        if isinstance(info, str):
            for line in info.splitlines():
                if line.startswith("Number of races:"):
                    try:
                        total_races = float(line.split(":", 1)[1].strip())
                        break
                    except ValueError:
                        pass

        if total_races is not None:
            races_data.append({"driver_name": driver, "total_races": total_races})

    # Plot if data exists
    if races_data:
        st.subheader("🔢 Drivers Total Races")

        df_total_races = pd.DataFrame(races_data).sort_values("total_races", ascending=True)

        # Plotting
        fig, ax = plt.subplots(figsize=(11, 4))
        fig.patch.set_facecolor('#333333')
        ax.set_facecolor('#444444')
        
        bars = ax.barh(df_total_races["driver_name"], df_total_races["total_races"], color="black", edgecolor="cyan", linewidth=1, height=0.5)

        # Add win count text to each bar
        for bar in bars:
            width = bar.get_width()
            offset = max(df_total_races["total_races"]) * 0.005  # 1% of max bar width
            ax.text(width + offset, bar.get_y() + bar.get_height() / 2,
                f"{width:.1f}" if not width.is_integer() else f"{int(width)}", va='center', ha='left', fontsize=10, color="white")

               
        # Add logo to the top left corner
        # Add logo in a small inset axes
        # Add logo as inset axes in top-left corner
        logo_ax = fig.add_axes([0.01, 0.82, 0.12, 0.15])  # [left, bottom, width, height] in relative figure coords
        logo_ax.imshow(logo_img)
        logo_ax.axis('off')

        ax.set_xlabel("Total Races", color= "white")
        ax.set_title("F1 Drivers History total races", fontsize=13, color='white')
        ax.grid(axis='x', linestyle='--', alpha=0.5)
        ax.tick_params(colors='white')
        st.pyplot(fig)
    
def render_driver_total_points(df, driver_info):
    # Build DataFrame of drivers with podiums
    DNFS_data = []
    for driver in df['driver_name'].unique():
        info = driver_info.get(driver, "")
        total_points = None

        if isinstance(info, str):
            for line in info.splitlines():
                if line.startswith("Total Points:"):
                    try:
                        total_points = float(line.split(":", 1)[1].strip())
                        break
                    except ValueError:
                        pass

        if total_points is not None:
            DNFS_data.append({"driver_name": driver, "total_points": total_points})

    # Plot if data exists
    if DNFS_data:
        st.subheader("📈 Drivers Total Points") 

        df_total_points = pd.DataFrame(DNFS_data).sort_values("total_points", ascending=True)

        # Plotting
        fig, ax = plt.subplots(figsize=(11, 4))
        fig.patch.set_facecolor('#333333')
        ax.set_facecolor('#444444')
        
        bars = ax.barh(df_total_points["driver_name"], df_total_points["total_points"], color="black", edgecolor="cyan", linewidth=1, height=0.5)

        # Add win count text to each bar
        for bar in bars:
            width = bar.get_width()
            offset = max(df_total_points["total_points"]) * 0.005  # 1% of max bar width
            ax.text(width + offset, bar.get_y() + bar.get_height() / 2,
                f"{width:.1f}" if not width.is_integer() else f"{int(width)}", va='center', ha='left', fontsize=10, color="white")

               
        # Add logo to the top left corner
        # Add logo in a small inset axes
        # Add logo as inset axes in top-left corner
        logo_ax = fig.add_axes([0.01, 0.82, 0.12, 0.15])  # [left, bottom, width, height] in relative figure coords
        logo_ax.imshow(logo_img)
        logo_ax.axis('off')

        ax.set_xlabel("Total Points", color= "white")
        ax.set_title("F1 Drivers History total points", fontsize=13, color='white')
        ax.grid(axis='x', linestyle='--', alpha=0.5)
        ax.tick_params(colors='white')
        st.pyplot(fig)
    
def render_driver_DNFs(df, driver_info):
    # Build DataFrame of drivers with podiums
    DNFS_data = []
    for driver in df['driver_name'].unique():
        info = driver_info.get(driver, "")
        total_DNFS = None

        if isinstance(info, str):
            for line in info.splitlines():
                if line.startswith("Retirements (DNFs):"):
                    try:
                        total_DNFS = int(line.split(":", 1)[1].strip())
                        break
                    except ValueError:
                        pass

        if total_DNFS is not None:
            DNFS_data.append({"driver_name": driver, "total_DNFS": total_DNFS})

    # Plot if data exists
    if DNFS_data:
        st.subheader("❌ Drivers Retirements (DNFs)")

        df_total_DNFS = pd.DataFrame(DNFS_data).sort_values("total_DNFS", ascending=False)

        # Plotting
        fig, ax = plt.subplots(figsize=(11, 4))
        fig.patch.set_facecolor('#333333')
        ax.set_facecolor('#444444')
        
        bars = ax.barh(df_total_DNFS["driver_name"], df_total_DNFS["total_DNFS"], color="black", edgecolor="cyan", linewidth=1, height=0.5)

        # Add win count text to each bar
        for bar in bars:
            width = bar.get_width()
            offset = max(df_total_DNFS["total_DNFS"]) * 0.005  # 1% of max bar width
            ax.text(width + offset, bar.get_y() + bar.get_height() / 2,
                f"{int(width)}", va='center', ha='left', fontsize=10, color="white")

               
        # Add logo to the top left corner
        # Add logo in a small inset axes
        # Add logo as inset axes in top-left corner
        logo_ax = fig.add_axes([0.01, 0.82, 0.12, 0.15])  # [left, bottom, width, height] in relative figure coords
        logo_ax.imshow(logo_img)
        logo_ax.axis('off')

        
        ax.set_xlabel("Retirements (DNFs)", color= "white")
        ax.set_title("F1 Drivers History total DNFS", fontsize=13, color='white')
        ax.grid(axis='x', linestyle='--', alpha=0.5)
        ax.tick_params(colors='white')
        st.pyplot(fig)
