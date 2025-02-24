import requests

# 目标 URL
url = "https://m.mallcoo.cn/api/user/User/GetUserCheckinList"

# Token 变量
token = "{Token}"

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

# 发送 HTTP 请求
try:
    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()

    # 解析返回值
    if response.status_code == 200 and response_data.get("m") == 1:
        # print("请求成功:", response_data["d"].get("Msg", ""))
        print("请求成功:", response_data)
    else:
        print("请求失败:", response_data)

except requests.exceptions.RequestException as e:
    print("请求错误:", str(e))

