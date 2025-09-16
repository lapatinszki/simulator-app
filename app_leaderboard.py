import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# ---------- Automatikus frissítés ----------
# 10 másodpercenként újratölti az oldalt
#st_autorefresh(interval=10 * 1000, key="leaderboard_refresh")

# ---------- Streamlit UI ----------
st.image("header.png", use_container_width=True)
st.subheader("Leaderboard 🏆")



import streamlit as st
from msal import ConfidentialClientApplication
import requests

client_id = st.secrets["azure"]["client_id"]
tenant_id = st.secrets["azure"]["tenant_id"]
client_secret = st.secrets["azure"]["client_secret"]

authority = f"https://login.microsoftonline.com/{tenant_id}"
scopes = ["https://graph.microsoft.com/.default"]  # .default kell confidential client-hez

app = ConfidentialClientApplication(
    client_id=client_id,
    client_credential=client_secret,
    authority=authority
)

# Token megszerzése
result = app.acquire_token_for_client(scopes=scopes)

if "access_token" in result:
    token = result["access_token"]
    st.success("Sikeres token! ✅")

    # Teszt e-mail küldése
    email_msg = {
        "message": {
            "subject": "Teszt e-mail Streamlitből",
            "body": {"contentType": "Text", "content": "Helló! Céges Graph API teszt."},
            "toRecipients": [{"emailAddress": {"address": "sajat.ceges@email.com"}}],
        },
        "saveToSentItems": "true",
    }

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    response = requests.post("https://graph.microsoft.com/v1.0/users/sajat.ceges@email.com/sendMail",
                             headers=headers, json=email_msg)
    if response.status_code == 202:
        st.success("Email elküldve!")
    else:
        st.error(f"Hiba a küldésnél: {response.status_code} {response.text}")
else:
    st.error(f"Token hiba: {result}")














































# # CSV betöltése
# df = pd.read_csv("table_Leaderboard.csv", encoding="utf-8", header=0)  # Feltételezve: Nickname és Profit oszlop
# df = df.sort_values("Profit", ascending=False).reset_index(drop=True)

# # Helyezés hozzáadása
# df["Rank"] = df.index + 1

# # Érem színek az első 3 helyezéshez
# bg_colors = {1: "#B9A534", 2: "#858585", 3: "#AD7134"}  # arany, ezüst, bronz
# border_color = "#FFFFFF"  # keret szín a 4. helytől

# for _, row in df.iterrows():
#     rank = row["Rank"]
#     nickname = row["Nickname"]
#     profit = row["Profit"]

#     if rank <= 3:
#         style = f"""
#         background-color:{bg_colors[rank]};
#         border-radius:12px;
#         border:1px solid {border_color};
#         padding:12px 20px;
#         margin-bottom:8px;
#         display:flex;
#         justify-content:space-between;
#         align-items:center;
#         font-family:sans-serif;
#         """
#     else:
#         style = f"""
#         background-color:transparent;
#         border-radius:12px;
#         border:1px solid {border_color};
#         padding:12px 20px;
#         margin-bottom:8px;
#         display:flex;
#         justify-content:space-between;
#         align-items:center;
#         font-family:sans-serif;
#         """

#     st.markdown(f"""
#     <div style="{style}">
#         <div style="display:flex; align-items:center; gap:10px;">
#             <span style="font-weight:bold; width:40px;">{rank}{"st" if rank==1 else "nd" if rank==2 else "rd" if rank==3 else "th"}</span>
#             <span style="font-weight:bold; font-size:16px;">{nickname}</span>
#         </div>
#         <div style="font-size:16px;">€{profit:.2f}</div>
#     </div>
#     """, unsafe_allow_html=True) 
    









