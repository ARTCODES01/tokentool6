import random, time, capmonster_python, threading, ctypes, httpx, base64, colorama, yaml, requests
from colorama import Fore, Back, Style
colorama.init()

with open("config.yml", "r") as ymlfile:
    cfg = yaml.safe_load(ymlfile)

capkey = cfg["capmonsterkey"]
proxyless = cfg["proxyless"]
if proxyless == True or proxyless == "True" or proxyless == "true":
    proxyless = True
else:
    proxyless = False
lock = threading.Lock()
tokens = open("tokens.txt", "r").read()
cap = capmonster_python.HCaptchaTask(capkey)
done = 0
total = len(tokens.splitlines())

def title():
    while True:
        cap = capmonster_python.HCaptchaTask(capkey)
        bal = str(f"${cap.get_balance():.2f}")
        ctypes.windll.kernel32.SetConsoleTitleW(f"{bal}")
        time.sleep(0.2)

threading.Thread(target=title).start()

def get_super_properties():
    properties = '''{"os":"Windows","browser":"Chrome","device":"","system_locale":"en-GB","browser_user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36","browser_version":"95.0.4638.54","os_version":"10","referrer":"","referring_domain":"","referrer_current":"","referring_domain_current":"","release_channel":"stable","client_build_number":102113,"client_event_source":null}'''
    properties = base64.b64encode(properties.encode()).decode()
    return properties


def get_fingerprint(s):
    try:
        fingerprint = s.get(f"https://discord.com/api/v9/experiments", timeout=5).json()["fingerprint"]
        return fingerprint
    except Exception as e:
        return "Error"


def get_cookies(s, url):
    try:
        cookieinfo = s.get(url, timeout=5).cookies
        dcf = str(cookieinfo).split('__dcfduid=')[1].split(' ')[0]
        sdc = str(cookieinfo).split('__sdcfduid=')[1].split(' ')[0]
        return dcf, sdc
    except:
        return "", ""


def get_proxy():
    if proxyless == True:
        return None
    else:
        with open("proxies.txt", "r") as f:
            proxies = f.readlines()
            proxy = random.choice(proxies).strip()
            return proxy


def get_headers(token):
    while True:
        s = httpx.Client()
        dcf, sdc = get_cookies(s, "https://discord.com/")
        fingerprint = get_fingerprint(s)
        if fingerprint != "Error": 
            break

    super_properties = get_super_properties()
    headers = {
        'authority': 'discord.com',
        'method': 'POST',
        'path': '/api/v9/users/@me/channels',
        'scheme': 'https',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'en-US',
        'authorization': token,
        'cookie': f'__dcfduid={dcf}; __sdcfduid={sdc}',
        'origin': 'https://discord.com',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',

        'x-debug-options': 'bugReporterEnabled',
        'x-fingerprint': fingerprint,
        'x-super-properties': super_properties,
    }

    return s, headers

invite = input("Invite > ").replace("https://discord.gg/", "").replace("https://discord.com/invite/", "")
lock = threading.Lock()

def capreq(tNum, token):
    try:
        createTask = httpx.post("https://api.capmonster.cloud/createTask", json={
        "clientKey": capkey,
        "task": {
            "type": "HCaptchaTaskProxyless",
            "websiteURL": "https://discord.com/channels/@me",
            "websiteKey": "76edd89a-a91d-4140-9591-ff311e104059",
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }}).json()["taskId"]


        getResults = {}
        getResults["status"] = "processing"
        while getResults["status"] == "processing":
            getResults = httpx.post("https://api.capmonster.cloud/getTaskResult", json={
                "clientKey": capkey,
                "taskId": createTask
                }).json()

        solution = getResults["solution"]["gRecaptchaResponse"]

        s, headers = get_headers(token)

        joinReq = s.post(f"https://discord.com/api/v9/invites/{invite}", headers=headers, json={"captcha_key": solution,}, proxies={"https": "https://" + get_proxy(), "http": "http://" + get_proxy(),}, timeout=5)

        responseStr = ""
        if joinReq.status_code == 200:
            responseStr = f"{Fore.GREEN}Joined https://discord.gg/" + invite
        elif joinReq.status_code == 429:
            responseStr = f"{Fore.YELLOW}Rate Limited"
        elif joinReq.status_code == 400:
            responseStr = f"{Fore.RED}Invalid Invite"
        elif joinReq.status_code == 401:
            responseStr = f"{Fore.RED}Invalid Token"
        elif joinReq.status_code == 403:
            responseStr = f"{Fore.RED}Forbidden"
        elif joinReq.status_code == 404:
            responseStr = f"{Fore.RED}Invite Not Found"
        elif joinReq.status_code == 500:
            responseStr = f"{Fore.RED}Internal Server Error"
        else:
            responseStr = f"{Fore.RED}Unknown Error"

        with lock:
            global done
            global total
            done += 1
            print(f"{Fore.CYAN}[{Fore.WHITE}{tNum}{Fore.CYAN}]{Fore.WHITE} | {responseStr} {Fore.CYAN}[{Fore.WHITE}{done}/{total}{Fore.CYAN}]{Fore.WHITE}")
    except Exception as e:
        print(f"{Fore.CYAN}[{Fore.WHITE}{tNum}{Fore.CYAN}]{Fore.WHITE} | {Fore.RED}Error: {e}")

for token in tokens.splitlines():
    threading.Thread(target=capreq, args=(random.randint(10, 99), token)).start()
    time.sleep(2.5)

time.sleep(5000)