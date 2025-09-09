import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_email(email, email_hash, nickname):
    # Küldés saját Gmailre
    sender_email = os.environ["GMAIL_EMAIL"]
    app_password = os.environ["GMAIL_APP_PASSWORD"]
    receiver_email = sender_email  # saját magadnak küldjük

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f"Új belépés: {nickname}"

    body = f"Felhasználó email: {email}\nEmail hash kód: {email_hash}\nNickname: {nickname}"
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, app_password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()

