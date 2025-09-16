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
import msal
import requests

client_id = "AZURE_CLIENT_ID"
tenant_id = "6d93b3cc-c87c-42be-8821-f9aa6ff35108"
authority = f"https://login.microsoftonline.com/{tenant_id}"
redirect_uri = "http://localhost:8501"
scopes = ["Mail.Send"]

st.write(authority)
# MSAL app
app = msal.PublicClientApplication(client_id, authority=authority)

# Token beszerzése
flow = app.initiate_device_flow(scopes=scopes)
if "user_code" not in flow:
    st.error("Nem sikerült a device flow indítása.")
else:
    st.write(f"Nyisd meg: {flow['verification_uri']}")
    st.write(f"Írd be a kódot: {flow['user_code']}")
    result = app.acquire_token_by_device_flow(flow)

if "access_token" in result:
    token = result["access_token"]

    # E-mail küldés a Graph API-val
    endpoint = "https://graph.microsoft.com/v1.0/me/sendMail"
    email_msg = {
        "message": {
            "subject": "Céges teszt üzenet",
            "body": {"contentType": "Text", "content": "Helló! Ez egy teszt az MS Graph API-val."},
            "toRecipients": [{"emailAddress": {"address": "cimzett@ceged.hu"}}],
        },
        "saveToSentItems": "true",
    }

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    response = requests.post(endpoint, headers=headers, json=email_msg)

    if response.status_code == 202:
        st.success("Email elküldve!")
    else:
        st.error(f"Hiba: {response.text}")
else:
    st.error(f"Nem sikerült bejelentkezni: {result}")















































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
    


