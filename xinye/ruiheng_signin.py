import json
import os
import smtplib
from email.mime.text import MIMEText

import requests

# 配置信息（需要用户替换）
# 读取环境变量
token = os.getenv("XY_TOKEN")
sender_email = os.getenv("EMAIL_SENDER")
email_password = os.getenv("EMAIL_PASSWORD")
receiver_email = os.getenv("EMAIL_RECEIVER")


def send_alert_email(error_info):
    msg = MIMEText(f"请求失败，错误信息如下：：\n{error_info}", "plain", "utf-8")
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "信业签到失败通知"

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, email_password)
            server.sendmail(sender_email, [receiver_email], msg.as_string())
        print("告警邮件已发送")
    except Exception as e:
        print(f"邮件发送失败：{str(e)}")


def check_api():
    """执行API请求并检查响应"""
    url = "https://ottomall.ruiheng.net.cn/api/app/sign"
    headers = {
        "Authorization": f"Bearer {token}",  # 修正Bearer格式
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.56(0x18003831) NetType/4G Language/zh_CN",
        "Referer": "https://servicewechat.com/wxf7572e0c9b87c29b/26/page-frame.html"
    }

    try:
        response = requests.post(url, headers=headers, json={}, timeout=10)

        # 检查HTTP状态码
        if response.status_code != 200:
            error_info = f"HTTP状态码异常: {response.status_code}\n响应内容: {response.text}"
            send_alert_email(error_info)
            return False

        # 检查业务状态码
        response_data = response.json()
        print("签到返回:", response_data)
        if response_data.get("code") != 200:
            error_info = f"业务状态码异常: {response_data}\n原始响应: {response.text}"
            send_alert_email(error_info)
            return False

        print("签到成功")
        return True

    except requests.exceptions.RequestException as e:
        error_info = f"请求异常: {str(e)}"
        send_alert_email(error_info)
        return False
    except json.JSONDecodeError:
        error_info = f"响应解析失败，原始响应: {response.text}"
        send_alert_email(error_info)
        return False


if __name__ == "__main__":
    check_api()
