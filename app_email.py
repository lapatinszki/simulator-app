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
def send_results(receiver_email, nickname, profit):

    sender_email = os.environ["GMAIL_EMAIL"]
    app_password = os.environ["GMAIL_APP_PASSWORD"]

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Factory Manager Challenge – Your results are in!"

    body = "Teszt"
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, app_password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()


    #msg['Subject'] = Header("🏆 Factory Manager Challenge – Your results are in!", 'utf-8')

    body = f"""
    <html>
    <body>
        Dear <b>{nickname}</b>,<br><br>

        Congratulations, you’ve completed the Mini Factory Challenge! 🏭<br>
        Your best result: <b>€{profit}</b> out of the maximum possible <b>€619.78</b>.<br>
        Not bad! 😎<br>
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
