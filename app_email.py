import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re, os
import dns.resolver
from email.utils import formataddr

# Küldés saját Gmailre - bejelentkezés logolása:
def send_email(email, email_hash, nickname):
    
    # Secrets betöltése
    smtp_server = st.secrets["email"]["smtp_server"]
    smtp_port = st.secrets["email"]["smtp_port"]
    smtp_username = st.secrets["email"]["smtp_username"]
    smtp_password = st.secrets["email"]["smtp_password"]
    smtp_helo = st.secrets["email"]["smtp_helo"]

    # Email adatok
    sender_name = "IDM Systems Zrt."
    sender_email = st.secrets["email"]["sender_email"] #"idm@idm-systems.hu"
    receiver_email = st.secrets["email"]["reciever_email"] #"lapatinszki18@gmail.com"
    subject = f"Új belépés: {nickname}"
    body = f"""
    <html>
    <body>
        <b>Email:</b> {email}<br>
        <b>Email hash kód:</b> {email_hash}<br>
        <b>Nickname:</b> {nickname}
    </body>
     </html>
     """

    message = MIMEMultipart()
    message["From"] = formataddr((sender_name, sender_email))
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.ehlo(smtp_helo)
            server.starttls()  # STARTTLS a Mailtrap port 587-hez
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
    except Exception as e:
        st.error(f"Hiba történt: {e}")



#Eredmény elküldése felhasználó e-mailre:
def send_results(receiver_email, nickname, profit):

    # Secrets betöltése
    smtp_server = st.secrets["email"]["smtp_server"]
    smtp_port = st.secrets["email"]["smtp_port"]
    smtp_username = st.secrets["email"]["smtp_username"]
    smtp_password = st.secrets["email"]["smtp_password"]
    smtp_helo = st.secrets["email"]["smtp_helo"]

    # Email adatok
    sender_name = "IDM Systems Zrt."
    sender_email = st.secrets["email"]["sender_email"]
    receiver_email = receiver_email
    subject = "🏆 Factory Manager Challenge – Your results are in!"
    body = f"""
     <html>
     <body>
         Dear <b>{nickname}</b>,<br><br>

         Congratulations, you’ve completed the Mini Factory Challenge! 🏭<br><br>
         
         Your best result: <b>€{profit}</b> out of the maximum possible <b>€619.78</b>. Not bad! 😎<br><br>
         
         But think about it: in real life, every decision has an even bigger impact on costs, quality, sustainability, and profit. This game was just a glimpse into how many parameters, trade-offs, and choices shape modern production processes.<br><br>

         <b>Relax, it’s just a game. Or… is it?</b> 👀<br><br>

         Because in real manufacturing, the same trade-offs decide whether you’re making money, wasting energy, or just stockpiling reject parts.<br>
         That’s where we come in: helping you find the sweet spot before the “Game Over” screen shows up in real life.<br><br>

         <b>Use simulation to untap the hidden potential of your manufacturing today – and profit tomorrow!</b><br><br>

         👉 Learn more: <a href="https://www.idm-systems.hu">www.idm-systems.hu</a><br><br>

         Best regards,<br>
         The IDM - Team
     </body>
     </html>
     """


    message = MIMEMultipart()
    message["From"] = formataddr((sender_name, sender_email))
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.ehlo(smtp_helo)
            server.starttls()  # STARTTLS a Mailtrap port 587-hez
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
    except Exception as e:
        st.error(f"Hiba történt: {e}")




#Checkolja az email címet:
def is_valid_email(email: str) -> bool:
    # 1. Regex: alap szintaktikai ellenőrzés
    regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(regex, email):
        return False
    
    # 2. MX rekord ellenőrzés
    try:
        domain = email.split("@")[1]
        answers = dns.resolver.resolve(domain, "MX")
        return len(answers) > 0
    except Exception:
        return False
