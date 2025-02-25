import json
import os
import smtplib
from email.mime.text import MIMEText
from tool.mail_util import send_email

import requests

# 配置信息（需要用户替换）
# 读取环境变量
token = os.getenv("XY_TOKEN")

def check_api():
    """执行API请求并检查响应"""
    url = "https://ottomall.ruiheng.net.cn/api/app/sign"
    headers = {
        "Authorization": {token},
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.56(0x18003831) NetType/4G Language/zh_CN",
        "Referer": "https://servicewechat.com/wxf7572e0c9b87c29b/26/page-frame.html"
    }

    try:
        response = requests.post(url, headers=headers, json={}, timeout=10)

        # 检查HTTP状态码
        if response.status_code != 200:
            error_info = f"HTTP状态码异常: {response.status_code}\n响应内容: {response.text}"
            send_email("信业签到失败通知", error_info)
            return False

        # 检查业务状态码
        response_data = response.json()
        print("签到返回:", response_data)
        if response_data.get("code") != 200:
            error_info = f"业务状态码异常: {response_data}\n原始响应: {response.text}"
            send_email("信业签到失败通知", error_info)
            return False

        print("签到成功")
        return True

    except requests.exceptions.RequestException as e:
        error_info = f"请求异常: {str(e)}"
        send_email("信业签到失败通知", error_info)
        return False
    except json.JSONDecodeError:
        error_info = f"响应解析失败，原始响应: {response.text}"
        send_email("信业签到失败通知", error_info)
        return False

if __name__ == "__main__":
    check_api()
