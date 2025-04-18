import os
import time

import requests

from daju.mallcoo_checkinlist import isChecked
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
    start_time = time.time()
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        # print(f"签到返回, httpcode[{response.status_code}], body:{response.text}")

        response_data = response.json()
        if response.status_code == 200 and response_data.get("m") == 1:
            print("签到成功")
            ret = True, "大橘签到成功", f"请求成功，返回信息如下：\n\n{response_data}"
        else:
            print("签到失败")
            ret = False, "大橘签到失败", f"请求失败，返回信息如下：\n\n{response_data}"
    except Exception as e:
        print("请求错误:", str(e))
        ret = False, "大橘签到异常", str(e)
    end_time = time.time()  # End time
    print(f"签到用时: {end_time - start_time:.4f} 秒")
    return ret


if __name__ == "__main__":
    if isChecked():
        print("已签到，无需重复签到")
    else:
        flag, subject, body = check_in()
        if not flag:
            send_email(subject, body)
