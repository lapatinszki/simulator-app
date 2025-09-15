import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.image("header.png", use_container_width=True)
st.subheader("Leaderboard 🏆")

# CSV betöltése
df = pd.read_csv("table_Leaderboard.csv", encoding="utf-8", header=0)
df = df.sort_values("Profit", ascending=False).reset_index(drop=True)
df["Rank"] = df.index + 1

bg_colors = {1: "#B9A534", 2: "#858585", 3: "#AD7134"}
border_color = "#FFFFFF"

leaderboard_html = ""
for _, row in df.iterrows():
    rank = row["Rank"]
    nickname = row["Nickname"]
    profit = row["Profit"]

    style = f"""
    background-color:{bg_colors.get(rank,'transparent')};
    border-radius:12px;
    border:1px solid {border_color};
    padding:12px 20px;
    margin-bottom:8px;
    display:flex;
    justify-content:space-between;
    align-items:center;
    font-family:sans-serif;
    """
    inner_div_style = "display:flex; align-items:center;"
    nickname_style = "font-weight:bold; font-size:16px; margin-left:10px;"

    leaderboard_html += f"""
    <div style="{style}">
        <div style="{inner_div_style}">
            <span style="font-weight:bold; width:40px;">{rank}{"st" if rank==1 else "nd" if rank==2 else "rd" if rank==3 else "th"}</span>
            <span style="{nickname_style}">{nickname}</span>
        </div>
        <div style="font-size:16px;">€{profit:.2f}</div>
    </div>
    """

# Scroll + automatikus frissítés JS
scroll_html = f"""
<div id="leaderboard" style="height:500px; overflow:auto;">
    {leaderboard_html}
</div>

<script>
var div = document.getElementById("leaderboard");
var scrollHeight = div.scrollHeight - div.clientHeight;
var current = 0;
function scrollDown() {{
    current += 1;
    if(current > scrollHeight) current = 0;
    div.scrollTop = current;
}}
setInterval(scrollDown, 50);

// 10 másodpercenként frissítés
setTimeout(function(){{
    window.location.reload();
}}, 10000);
</script>
"""

st.markdown(scroll_html, unsafe_allow_html=True)
