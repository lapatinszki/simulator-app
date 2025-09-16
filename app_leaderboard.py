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

st.title("Céges Outlook e-mail küldés – Streamlit")

# ==========================
# 1. Azure App adatok
# ==========================
client_id = "IDE_JÖN_AZ_APP_CLIENT_ID"   # Azure App Registration Client ID
tenant_id = "IDE_JÖN_A_TENANT_ID"       # Azure Directory (Tenant) ID
authority = f"https://login.microsoftonline.com/{tenant_id}"  # v2.0 is jó: /v2.0
scopes = ["Mail.Send"]  # engedély, hogy küldhessünk e-mailt

# ==========================
# 2. MSAL PublicClientApplication
# ==========================
try:
    app = msal.PublicClientApplication(client_id, authority=authority)
except Exception as e:
    st.error(f"Hiba MSAL init-nél: {e}")
    st.stop()

# ==========================
# 3. Token lekérése (Device Flow)
# ==========================
flow = app.initiate_device_flow(scopes=scopes)
if "user_code" not in flow:
    st.error("Nem sikerült elindítani a Device Flow-t.")
    st.stop()

st.write("1️⃣ Nyisd meg a következő weboldalt a böngésződben:")
st.code(flow['verification_uri'])
st.write("2️⃣ Írd be a következő kódot:")
st.code(flow['user_code'])
st.write("⚠️ Miután beírtad, várj néhány másodpercet, amíg a token megszerezhető.")

result = app.acquire_token_by_device_flow(flow)  # blokkolja a futást, amíg a felhasználó be nem lép

# ==========================
# 4. Token ellenőrzése
# ==========================
if result is None:
    st.error("Token megszerzése sikertelen (None jött vissza).")
    st.stop()
elif "access_token" not in result:
    st.error(f"Token hiba: {result}")
    st.stop()
else:
    token = result["access_token"]
    st.success("✅ Sikeres bejelentkezés! Access token megszerezve.")

# ==========================
# 5. Teszt e-mail küldése
# ==========================
receiver_email = st.text_input("Címzett e-mail", value="sajat.email@ceged.hu")
subject = st.text_input("Tárgy", value="Teszt e-mail Streamlitből")
body = st.text_area("Üzenet tartalma", value="Helló! Ez egy teszt e-mail Microsoft Graph API-val.")

if st.button("Küldés"):
    email_msg = {
        "message": {
            "subject": subject,
            "body": {"contentType": "Text", "content": body},
            "toRecipients": [{"emailAddress": {"address": receiver_email}}],
        },
        "saveToSentItems": "true",
    }

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    response = requests.post("https://graph.microsoft.com/v1.0/me/sendMail",
                             headers=headers, json=email_msg)

    if response.status_code == 202:
        st.success(f"✅ E-mail elküldve a(z) {receiver_email} címre!")
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
    






