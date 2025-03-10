import os
import time
from datetime import datetime

import pytz
import requests

# 目标 URL
url = "https://m.mallcoo.cn/api/user/User/GetUserCheckinList"

# Token 变量
token = os.getenv("TOKEN")

# HTTP 请求头
headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.56(0x18003831) NetType/4G Language/zh_CN",
    "Referer": "https://servicewechat.com/wx5ed3b6a20498bd39/6/page-frame.html"
}

# 请求数据
data = {
    "MallID": 12835,
    "UserID": 11,
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


def is_date_in_response(date, response):
    try:
        # Ensure the response status is successful
        if response.get("m") != 1:
            return False

        # Check if today's date exists in any 'CheckInTime' entry
        return any(date in entry["CheckInTime"] for entry in response.get("d", []))

    except Exception as e:
        print(f"Error occurred: {e}")
        return False  # Return False if any exception occurs


def isChecked():
    start_time = time.time()
    ret = False
    # 发送 HTTP 请求
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response_data = response.json()

        print(f"签到检查返回, httpcode[{response.status_code}], body:{response.text}")
        # 解析返回值
        if response.status_code == 200:
            # Call the function and print result
            # Extract today's date in 'YYYY/MM/DD' format
            today_str = datetime.now(pytz.timezone('Asia/Shanghai')).strftime("%Y/%m/%d")
            ret = is_date_in_response(today_str, response_data)
            print(f"今日[{today_str}]是否已签到: {ret}")

    except requests.exceptions.RequestException as e:
        print("请求错误:", str(e))
    end_time = time.time()  # End time
    print(f"签到检查用时: {end_time - start_time:.4f} 秒")
    return ret


if __name__ == "__main__":
    if (isChecked()):
        print("已签到，无需重复签到")
