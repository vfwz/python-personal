import os
import requests
import smtplib
import time
import random
from email.mime.text import MIMEText
from email.header import Header

# 读取环境变量
token = os.getenv("TOKEN")
sender_email = os.getenv("EMAIL_SENDER")
email_password = os.getenv("EMAIL_PASSWORD")
receiver_email = os.getenv("EMAIL_RECEIVER")

# 目标 URL
url = "https://m.mallcoo.cn/api/user/User/CheckinV2"

# HTTP 请求头
headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.56(0x18003831) NetType/4G Language/zh_CN",
    "Referer": "https://servicewechat.com/wx5ed3b6a20498bd39/6/page-frame.html"
}

# 请求数据
data = {
    "MallID": 12835,
    "Header": {
        "Token": token,
        "systemInfo": {
            "model": "iPhone 15 pro<iPhone16,1>",
            "SDKVersion": "3.7.8",
            "system": "iOS 18.1.1",
            "version": "8.0.56",
            "miniVersion": "2.71.0"
        }
    }
}

# 发送 HTTP 请求
def check_in():
    try:
        # Generate a random delay time in seconds (up to 5 minutes)
        delay_time = random.randint(0, 60)  # 300 seconds = 5 minutes

        print(f"延迟{delay_time}秒后执行")

        # Delay the program execution
        time.sleep(delay_time)
        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()

        if response.status_code == 200 and response_data.get("m") == 1:
            print("签到成功:", response_data["d"].get("Msg", ""))
        else:
            print("签到失败:", response_data)
            send_failure_email(response_data)
    except requests.exceptions.RequestException as e:
        print("请求错误:", str(e))
        send_failure_email(str(e))

# 发送失败通知邮件
def send_failure_email(error_msg):
    subject = "大橘签到请求失败通知"
    body = f"请求失败，错误信息如下：\n\n{error_msg}"

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

if __name__ == "__main__":
    check_in()
