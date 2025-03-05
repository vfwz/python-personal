import os
from datetime import datetime

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


def is_current_date_in_response(response):
    try:
        # Ensure the response status is successful
        if response.get("m") != 1:
            return False

        # Extract today's date in 'YYYY/MM/DD' format
        today_str = datetime.now().strftime("%Y/%m/%d")

        # Check if today's date exists in any 'CheckInTime' entry
        return any(today_str in entry["CheckInTime"] for entry in response.get("d", []))

    except Exception as e:
        print(f"Error occurred: {e}")
        return False  # Return False if any exception occurs


def isChecked():
    # 发送 HTTP 请求
    try:
        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()

        print(f"签到检查返回, httpcode[{response.status_code}], body:{response.text}")
        # 解析返回值
        if response.status_code == 200 and is_current_date_in_response(response_data):
            # Call the function and print result
            print("今日是否已签到: ",
                  is_current_date_in_response(response_data))  # Output: True or False depending on the current date
            return True
        else:
            print("请求失败:", response_data)

    except requests.exceptions.RequestException as e:
        print("请求错误:", str(e))
    return False
