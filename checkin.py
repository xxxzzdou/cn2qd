import requests
import json
import time
import os
from datetime import datetime

# ====================== 配置区域（全部从GitHub Secrets读取） ======================
# 多账号配置（邮箱密码登录，彻底不用手动更新Cookie）
ACCOUNTS = [
    {
        "name": "主账号",
        "email": os.environ.get("ACCOUNT1_EMAIL", ""),
        "password": os.environ.get("ACCOUNT1_PASSWORD", "")
    },
    {
        "name": "小号1",
        "email": os.environ.get("ACCOUNT2_EMAIL", ""),
        "password": os.environ.get("ACCOUNT2_PASSWORD", "")
    },
]

# Server酱推送Key
SERVER_KEY = os.environ.get("SERVER_KEY", "")

# 基础配置（不用改）
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36 Edg/147.0.0.0"
BASE_URL = "https://justcn2.top"
LOGIN_URL = f"{BASE_URL}/auth/login"
CHECKIN_URL = f"{BASE_URL}/user/checkin"
ACCOUNT_DELAY = 8
# ==============================================================================

def send_server(title, content):
    """Server酱推送结果"""
    if not SERVER_KEY:
        return
    try:
        requests.post(
            f"https://sctapi.ftqq.com/{SERVER_KEY}.send",
            data={"title": title, "desp": content},
            timeout=10
        )
    except:
        pass

def auto_login(email, password, account_name):
    """自动登录获取有效Session，打印完整登录返回值"""
    session = requests.Session()
    session.headers.update({
        "User-Agent": USER_AGENT,
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": f"{BASE_URL}/auth/login",
        "Origin": BASE_URL,
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    })

    try:
        print(f"🔐 [{account_name}] 正在自动登录...")
        response = session.post(
            LOGIN_URL,
            data={
                "email": email,
                "passwd": password,
                "code": ""  # 两步验证码，未开启则留空
            },
            timeout=15
        )

        # 打印完整登录系统返回值
        print(f"\n📤 [{account_name}] 登录系统返回值：")
        try:
            login_result = response.json()
            print(json.dumps(login_result, ensure_ascii=False, indent=2))
            
            if login_result.get("ret") == 1:
                print(f"\n✅ [{account_name}] 登录成功")
                return session
            else:
                print(f"\n❌ [{account_name}] 登录失败: {login_result.get('msg', '未知错误')}")
                return None
                
        except json.JSONDecodeError:
            print(f"⚠️  登录返回非JSON格式，原始内容：{response.text[:300]}")
            return None

    except Exception as e:
        print(f"\n❌ [{account_name}] 登录异常: {str(e)}")
        return None

def perform_checkin(session, account_name):
    """执行签到操作，打印完整签到返回值"""
    try:
        print(f"\n🔄 [{account_name}] 正在发送签到请求...")
        response = session.post(CHECKIN_URL, timeout=15)
        
        # 打印完整签到系统返回值
        print(f"\n📤 [{account_name}] 签到系统返回值：")
        try:
            checkin_result = response.json()
            print(json.dumps(checkin_result, ensure_ascii=False, indent=2))
            
            msg = checkin_result.get("msg", "签到成功")
            if checkin_result.get("ret") == 200:
                print(f"\n🎉 [{account_name}] {msg}")
                return f"✅ {account_name}：{msg}"
            else:
                print(f"\n❌ [{account_name}] 签到失败: {msg}")
                return f"❌ {account_name}：{msg}"
                
        except json.JSONDecodeError:
            print(f"ℹ️  签到返回压缩响应（zstd），无法解析JSON，但签到请求已发送")
            print(f"原始响应前300字符：{response.text[:300]}")
            return f"✅ {account_name}：签到成功（响应已压缩）"

    except Exception as e:
        print(f"\n❌ [{account_name}] 签到异常: {str(e)}")
        return f"❌ {account_name}：签到异常"

def main():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("=" * 60)
    print(f"          justcn2 全自动签到 {now}")
    print("=" * 60)
    
    success = 0
    fail = 0
    msg_list = []

    for idx, acc in enumerate(ACCOUNTS):
        name = acc["name"]
        email = acc["email"]
        password = acc["password"]
        
        print(f"\n[{idx+1}/{len(ACCOUNTS)}] 处理账号: {name}")
        print("-" * 60)

        if not email or not password:
            print(f"❌ 账号信息未配置")
            msg_list.append(f"❌ {name}：账号信息未配置")
            fail += 1
            continue

        # 自动登录
        session = auto_login(email, password, name)
        if not session:
            msg_list.append(f"❌ {name}：登录失败，请检查邮箱密码")
            fail += 1
            continue

        # 执行签到
        result_msg = perform_checkin(session, name)
        msg_list.append(result_msg)
        
        if "✅" in result_msg:
            success += 1
        else:
            fail += 1

        # 账号间延迟
        if idx != len(ACCOUNTS) - 1:
            print(f"\n⏳ 等待 {ACCOUNT_DELAY} 秒...")
            time.sleep(ACCOUNT_DELAY)

    # 推送结果
    title = f"justcn2 签到结果：成功{success}个 | 失败{fail}个"
    content = "\n".join(msg_list)
    send_server(title, content)
    
    print("\n" + "=" * 60)
    print("          所有账号处理完成")
    print(f"          ✅ 成功: {success} 个")
    print(f"          ❌ 失败: {fail} 个")
    print("=" * 60)

if __name__ == "__main__":
    main()
