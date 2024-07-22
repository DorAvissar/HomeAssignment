import time
import smtplib
import psutil as ps
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

def email_alert(subject, body, to): 
    msg = EmailMessage() 
    msg.set_content(body) 
    msg['subject'] = subject
    msg['to'] = to

    user = os.getenv('EMAIL_USER')
    msg['from'] = user
    password = os.getenv('EMAIL_PASSWORD')

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    server.quit()

def cpu():
    alert_sent = False
    while True:
        cpu_use = ps.cpu_percent(1)
        if cpu_use > 80  and not alert_sent:
            email_alert("cpu alert", "HI, please note that the cpu usage is over 80% ! ", "doravissar1@gmail.com")
            print("alert was sent")
            alert_sent = True
            time.sleep(10)

        elif cpu_use <= 80:
            alert_sent = False
            print(f'Current CPU usage: {cpu_use}%')
            time.sleep(5)

if __name__ =='__main__':
    cpu()



