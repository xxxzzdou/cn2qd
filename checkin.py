import requests
import json
import time
from datetime import datetime

# ====================== 多账号配置 ======================
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

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36 Edg/147.0.0.0"
BASE_URL = "https://justcn2.top"
CHECKIN_URL = f"{BASE_URL}/user/checkin"
ACCOUNT_DELAY = 8
# ======================================================

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

def check_login(session, name):
    try:
        r = session.get(f"{BASE_URL}/user", timeout=15)
        return r.status_code == 200
    except:
        return False

def checkin(session, name):
    try:
        r = session.post(CHECKIN_URL, timeout=15)
        if r.status_code == 200:
            print(f"✅ {name} 签到成功")
            return True
        else:
            print(f"❌ {name} 签到失败，状态码：{r.status_code}")
            return False
    except Exception as e:
        print(f"❌ {name} 网络错误：{e}")
        return False

def main():
    print("===== justcn2.top 多账号自动签到 =====")
    ok = 0
    fail = 0
    for idx, acc in enumerate(ACCOUNTS):
        name = acc["name"]
        ck = acc["cookie"]
        print(f"\n[{idx+1}/{len(ACCOUNTS)}] {name}")
        s = create_session(ck)
        if not check_login(s, name):
            print(f"❌ Cookie 无效")
            fail +=1
            continue
        if checkin(s, name):
            ok +=1
        else:
            fail +=1
        if idx != len(ACCOUNTS)-1:
            time.sleep(ACCOUNT_DELAY)
    print(f"\n===== 签到完成：成功 {ok} 个，失败 {fail} 个 =====")

if __name__ == "__main__":
    main()
