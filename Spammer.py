import requests, json, random, time, os, sys, re, capmonster_python, threading, ctypes, httpx, base64

lock = threading.Lock()

tokens = open("tokens.txt", "r").read()

num = 0
channel = input("Channel ID > ")
message = input("Message > ")
Bypass = input("Bypass? (y/n) > ")
if Bypass == "y" or Bypass == "Y":
    Bypass = True
else:
    Bypass = False

while True:
    def thread():
        global num
        token = random.choice(tokens.splitlines())
        # check if the token is valid
        req = requests.get("https://discord.com/api/v9/users/@me", headers={
            "authorization": token
        })
        while req.status_code != 200:
            token = random.choice(tokens.splitlines())
            req = requests.get("https://discord.com/api/v9/users/@me", headers={
                "authorization": token
            })
        try:
                global Bypass
                if Bypass == False:
                    requests.post(f"https://discord.com/api/v9/channels/{channel}/messages", headers={
                        "authorization": token
                    }, json={
                        "content": message
                    })
                else:
                    requests.post(f"https://discord.com/api/v9/channels/{channel}/messages", headers={
                        "authorization": token
                    }, json={
                        "content": message + " | " + random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") + random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") + random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") + random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") + random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") + random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
                    })
                with lock:
                    num += 1
                    print(f"Sent message {num}")
        except:
            with lock:
                num += 1
                print(f"Failed to send message {num}")
    threading.Thread(target=thread).start()