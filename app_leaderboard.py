import streamlit as st
import pandas as pd
import time

# Automatikus frissítés (Streamlit "hack")
refresh_rate = 10  # másodperc

if 'last_refresh' not in st.session_state:
    st.session_state['last_refresh'] = time.time()

if time.time() - st.session_state['last_refresh'] > refresh_rate:
    st.session_state['last_refresh'] = time.time()
    st.experimental_rerun()

# --- Leaderboard kód itt marad ---
st.image("header.png", use_container_width=True)
st.subheader("Leaderboard 🏆")

df = pd.read_csv("table_Leaderboard.csv", encoding="utf-8", header=0)
df = df.sort_values("Profit", ascending=False).reset_index(drop=True)
df["Rank"] = df.index + 1

bg_colors = {1: "#B9A534", 2: "#858585", 3: "#AD7134"}
border_color = "#FFFFFF"

for _, row in df.iterrows():
    rank = row["Rank"]
    nickname = row["Nickname"]
    profit = row["Profit"]

    style = f"""
    background-color:{bg_colors.get(rank, 'transparent')};
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
