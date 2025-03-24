import os
import time

import requests

from tool.mail_util import send_email
from xinye.ruiheng_signinfo import is_today_signed_in

# 配置信息（需要用户替换）
# 读取环境变量
token = os.getenv("XY_TOKEN")


def check_api():
    """执行API请求并检查响应"""
    url = "https://ottomall.ruiheng.net.cn/api/app/sign"
    headers = {
        "Authorization": f"{token}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.56(0x18003831) NetType/4G Language/zh_CN",
        "Referer": "https://servicewechat.com/wxf7572e0c9b87c29b/26/page-frame.html"
    }
    start_time = time.time()

    try:
        response = requests.post(url, headers=headers, json={}, timeout=10)

        # print(f"签到返回, httpcode[{response.status_code}], body:{response.text}")
        # 检查HTTP状态码
        if response.status_code == 200 and response.json().get("code") == 200:
            print("签到成功")
            ret = True, "信业签到成功", f"请求成功，返回信息如下：\n\n{response.json()}"
        else:
            print("签到失败,", response.status_code, response.text)
            ret = False, "信业签到失败", f"原始响应: {response.text}"
    except Exception as e:
        error_info = f"请求异常: {str(e)}"
        ret = False, "信业签到失败", error_info
    end_time = time.time()  # End time
    print(f"签到用时: {end_time - start_time:.4f} 秒")
    return ret


if __name__ == "__main__":
    if is_today_signed_in():
        print('今日已签到, 无需再签到')
    else:
        flag, subject, body = check_api()
        if not flag:
            send_email(subject, body)
