import json
import os
from datetime import datetime

import pytz
import requests

token = os.getenv("XY_TOKEN")


def is_today_signed_in():
    """执行API请求并检查响应"""
    month = datetime.now(pytz.timezone('Asia/Shanghai')).strftime("%Y-%m")
    url = "https://ottomall.ruiheng.net.cn/api/app/sign?month=" + month
    headers = {
        "Authorization": token,  # 修正Bearer格式
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.56(0x18003831) NetType/4G Language/zh_CN",
        "Referer": "https://servicewechat.com/wxf7572e0c9b87c29b/26/page-frame.html"
    }

    try:
        response = requests.get(url, headers=headers, json={}, timeout=10)

        # 检查HTTP状态码
        if response.status_code != 200:
            print(f"HTTP状态码异常: {response.status_code}, 响应内容: {response.text}")
            return False
        # print("签到检查数据返回:", response.text)
        respJson = response.json()
        # Ensure the response status is successful
        if respJson.get("code") != 200:
            return False

        # print(f"HTTP状态码: {response.status_code}, 响应内容: {response.text}")

        # Extract today's date in 'YYYY-MM-DD' format
        today_str = datetime.now(pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d")

        # Get the list of records
        records = respJson.get("data", {}).get("records", [])
        ret = any(today_str == record.get("signDate") for record in records)
        signDay = max((record["signDay"] for record in records), default=None)
        print(f"今日[{today_str}]是否已签到: {ret}, 已连续签到[{signDay}]天")
        # Check if today's date exists in any 'signDate' entry
        return ret
    except Exception as e:
        print(f"签到检查报错: {e}")
        return False  # Return False if any exception occurs


if __name__ == "__main__":
    print("今日是否已签到: ", is_today_signed_in())
