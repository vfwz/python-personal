import os
import requests
import time
import random
from tool.mail_util import send_email

# 读取环境变量
token = os.getenv("TOKEN")

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
            print("签到失败:", response)
            send_email("大橘签到失败通知", f"请求失败，返回信息如下：\n\n{response_data}", response_data)
    except requests.exceptions.RequestException as e:
        print("请求错误:", str(e))
        send_email("大橘签到异常", str(e))

if __name__ == "__main__":
    check_in()
