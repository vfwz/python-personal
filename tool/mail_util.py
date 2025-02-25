import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 发送失败通知邮件
def send_email(subject, body, sender_email=None, email_password=None, receiver_email=None):
    sender_email = sender_email or os.getenv("EMAIL_SENDER")
    email_password = email_password or os.getenv("EMAIL_PASSWORD")
    receiver_email = receiver_email or os.getenv("EMAIL_RECEIVER")

    message = MIMEText(body, "plain", "utf-8")
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = Header(subject, "utf-8")

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender_email, email_password)
        server.sendmail(sender_email, [receiver_email], message.as_string())
        server.quit()
        print("失败通知邮件已发送:", receiver_email)
    except Exception as e:
        print("邮件发送失败:", receiver_email, str(e))