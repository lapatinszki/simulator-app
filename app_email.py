import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
import dns.resolver
import os

# Küldés saját Gmailre - bejelentkezés logolása:
def send_email(email, email_hash, nickname):
    
    sender_email = os.environ["GMAIL_EMAIL"]
    app_password = os.environ["GMAIL_APP_PASSWORD"]
    receiver_email = sender_email  # saját magadnak küldjük

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f"Új belépés: {nickname}"

    body = f"Email: {email}\nEmail hash kód: {email_hash}\nNickname: {nickname}"
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, app_password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()



#Eredmény elküldése felhasználó e-mailre:
def send_results(receiver_email, nickname):
    sender_email = os.environ["GMAIL_EMAIL"]
    app_password = os.environ["GMAIL_APP_PASSWORD"]

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email

    msg['Subject'] = f"Új belépés: {nickname}"
    body = ""


    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, app_password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()




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
