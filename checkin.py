import requests
import json
import time
from datetime import datetime

# ====================== 【配置区域】 ======================
# 1. 多账号 Cookie（每个账号一行）
ACCOUNTS = [
    {
        "name": "账号1",
        "cookie": "uid=28217; email=zhenzhebbe88%40163.com; key=7f55eb61042877a432167fe99ba368380a824f03c0646; ip=0fb0c67b9fe5735b27ebd8a2fc8908f8; expire_in=1779565692"
    },
    {
        "name": "账号2",
        "cookie": "uid=27633; email=xiuff%40foxmail.com; key=64d8ecf6aa688b697590585a72688107ac790fcdcad8a; ip=a0d247b47fea536fcd016c61e432c826; expire_in=1779647947"
    },
    {
        "name": "账号3",
        "cookie": "uid=26936; email=xiu52pojie%40qq.com; key=21c7956727f4047e98b16f70908bce57868313ff67638; ip=409469fb92fcc23eda76724664b9a329; expire_in=1779647372"
    },
]

# 2. Server 酱 SendKey（去 sct.ftqq.com 复制）
SERVER_KEY = "SCT354333T99vc4DlKnPhJMTEauGDFQNYX"

# 基础配置（不用改）
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36 Edg/147.0.0.0"
BASE_URL = "https://justcn2.top"
CHECKIN_URL = f"{BASE_URL}/user/checkin"
ACCOUNT_DELAY = 8
# ==========================================================

def send_server(title, content):
    """Server 酱推送"""
    if not SERVER_KEY:
        return
    url = f"https://sctapi.ftqq.com/{SERVER_KEY}.send"
    data = {
        "title": title,
        "desp": content
    }
    try:
        requests.post(url, data=data, timeout=10)
    except:
        pass

def create_session(cookie):
    session = requests.Session()
    session.headers.update({
        "User-Agent": USER_AGENT,
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": f"{BASE_URL}/user",
        "Origin": BASE_URL,
        "X-Requested-With": "XMLHttpRequest",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Cookie": cookie
    })
    return session

def check_login(session):
    try:
        r = session.get(f"{BASE_URL}/user", timeout=15)
        return r.status_code == 200
    except:
        return False

def checkin(session):
    try:
        r = session.post(CHECKIN_URL, timeout=15)
        return r.status_code == 200
    except:
        return False

def main():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"===== justcn2 自动签到 {now} =====")
    
    success = 0
    fail = 0
    msg_list = []

    for idx, acc in enumerate(ACCOUNTS):
        name = acc["name"]
        ck = acc["cookie"]
        print(f"\n[{idx+1}] {name}")
        
        s = create_session(ck)
        if not check_login(s):
            print("❌ Cookie 无效")
            msg_list.append(f"❌ {name}：Cookie 已失效")
            fail += 1
            continue

        if checkin(s):
            print("✅ 签到成功")
            msg_list.append(f"✅ {name}：签到成功")
            success += 1
        else:
            print("❌ 签到失败")
            msg_list.append(f"❌ {name}：签到失败")
            fail += 1

        if idx != len(ACCOUNTS)-1:
            time.sleep(ACCOUNT_DELAY)

    # 推送结果
    title = f"justcn 签到结果：成功{success}个 | 失败{fail}个"
    content = "\n".join(msg_list)
    send_server(title, content)
    
    print(f"\n===== 完成：成功 {success} | 失败 {fail} =====")

if __name__ == "__main__":
    main()
