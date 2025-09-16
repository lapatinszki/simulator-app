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
from msal import PublicClientApplication
import requests

st.title("Céges M365 e-mail küldés – Streamlit Cloud (Device Flow)")

client_id = st.secrets["azure"]["client_id"]
tenant_id = st.secrets["azure"]["tenant_id"]
authority = f"https://login.microsoftonline.com/{tenant_id}"
scopes = ["Mail.Send"]

# Public Client Application
app = PublicClientApplication(client_id=client_id, authority=authority)

# --------------------
# 1️⃣ Device Flow generálása
# --------------------
if 'flow' not in st.session_state:
    if st.button("Kód generálása"):
        flow = app.initiate_device_flow(scopes=scopes)
        st.session_state['flow'] = flow
        st.success("Device Flow kód generálva!")

if 'flow' in st.session_state:
    flow = st.session_state['flow']
    st.write("Nyisd meg ezt az oldalt:", flow['verification_uri'])
    st.write("Írd be ezt a kódot:", flow['user_code'])
    st.info("Jelentkezz be a Microsoft fiókoddal és erősítsd meg az MFA-t, ha szükséges.")

    # --------------------
    # 2️⃣ Token lekérése
    # --------------------
    if st.button("Token lekérése"):
        result = app.acquire_token_by_device_flow(flow)  # poll-ol, de egyszeri gombnyomásra
        if "access_token" in result:
            st.session_state['token'] = result['access_token']
            st.session_state['email'] = result['id_token_claims']['preferred_username']
            st.success("Sikeres bejelentkezés!")
        else:
            st.error(f"Token hiba: {result}")

# --------------------
# 3️⃣ E-mail küldés
# --------------------
if 'token' in st.session_state:
    subject = st.text_input("Tárgy", "Teszt Streamlit e-mail")
    body = st.text_area("Üzenet", "Helló! Ez egy teszt e-mail.")

    if st.button("Küldés"):
        email_msg = {
            "message": {
                "subject": subject,
                "body": {"contentType": "Text", "content": body},
                "toRecipients": [{"emailAddress": {"address": st.session_state['email']}}],
            },
            "saveToSentItems": "true",
        }

        headers = {"Authorization": f"Bearer {st.session_state['token']}", "Content-Type": "application/json"}
        response = requests.post(
            "https://graph.microsoft.com/v1.0/me/sendMail",
            headers=headers,
            json=email_msg
        )

        if response.status_code == 202:
            st.success(f"Email elküldve a saját mailboxodra: {st.session_state['email']}")
        else:
            st.error(f"Hiba a küldésnél: {response.status_code} {response.text}")










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
    

















