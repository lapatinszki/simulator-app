import streamlit as st
import pandas as pd

st.image("header.png", use_container_width=True)
st.subheader("Leaderboard 🏆")

# CSV betöltése
df = pd.read_csv("table_Leaderboard.csv", encoding="utf-8", header=0)  # Feltételezve: Nickname és Profit oszlop
df = df.sort_values("Profit", ascending=False).reset_index(drop=True)

# Helyezés hozzáadása
df["Rank"] = df.index + 1

# Érem színek az első 3 helyezéshez
bg_colors = {1: "#B9A534", 2: "#858585", 3: "#AD7134"}  # arany, ezüst, bronz
border_color = "#FFFFFF"  # keret szín a 4. helytől

for _, row in df.iterrows():
    rank = row["Rank"]
    nickname = row["Nickname"]
    profit = row["Profit"]

    if rank <= 3:
        # Háttérszín az első 3 helynek
        style = f"""
        background-color:{bg_colors[rank]};
        border-radius:12px;
        border:1px solid {border_color};
        padding:12px 20px;
        margin-bottom:8px;
        display:flex;
        justify-content:space-between;
        align-items:center;
        font-family:sans-serif;
        """
    else:
        # Átlátszó doboz csak kerettel
        style = f"""
        background-color:transparent;
        border-radius:12px;
        border:1px solid {border_color};
        padding:12px 20px;
        margin-bottom:8px;
        display:flex;
        justify-content:space-between;
        align-items:center;
        font-family:sans-serif;
        """

    st.markdown(f"""
    <div style="{style}">
        <div style="display:flex; align-items:center; gap:10px;">
            <span style="font-weight:bold; width:40px;">{rank}{"st" if rank==1 else "nd" if rank==2 else "rd" if rank==3 else "th"}</span>
            <span style="font-weight:bold; font-size:16px;">{nickname}</span>
        </div>
        <div style="font-size:16px;">€{profit:.2f}</div>
    </div>
    """, unsafe_allow_html=True)

