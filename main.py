import configparser
import random
import time

import requests

from helper import load_json, save_json
from keygen import GamePlayer
from logconf import logger

config = configparser.ConfigParser()
config.read("config.ini")
client = config["CLIENT"]

AUTH_TOKEN = client["AUTH_TOKEN"]
USER_AGENT = client["USER_AGENT"]
SEC_CH_UA = client["SEC_CH_UA"]

promos = load_json("promos.json")

playlist = {
    "Twerk Race",
    "Bike Ride 3D",
    'Train Miner',
    'Chain Cube 2048',
    'Mud Racing',
    "Mow and Trim",
    "Polysphere"
}


def apply_promo(code: str) -> bool:
    options_headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en,en-US;q=0.9",
        "Access-Control-Request-Headers": "authorization,content-type",
        "Access-Control-Request-Method": "POST",
        "Connection": "keep-alive",
        "Host": "api.hamsterkombatgame.io",
        "Origin": "https://hamsterkombatgame.io",
        "Referer": "https://hamsterkombatgame.io/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": USER_AGENT
    }

    headers = {
        "accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en,en-US;q=0.9",
        "authorization": AUTH_TOKEN,
        "Connection": "keep-alive",
        "content-type": "application/json",
        "Host": "api.hamsterkombatgame.io",
        "Origin": "https://hamsterkombatgame.io",
        "Referer": "https://hamsterkombatgame.io/",
        "sec-ch-ua": SEC_CH_UA,
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": USER_AGENT
    }

    logger.info(f"Applying key '{code}'...")
    url = 'https://api.hamsterkombatgame.io/clicker/apply-promo'

    r = requests.options(url, headers=options_headers)
    r.raise_for_status()

    data = {'promoCode': code}
    response = requests.post(url, headers=headers, json=data)

    logger.info(f"Key '{code}' applied: {response.status_code == 200}")

    if response.status_code == 200:
        logger.info(f"Key '{code}' applied")
        return True
    else:
        logger.error(f"Failed to apply key '{code}': {response.text}")
        return False


def get_promos():
    options_headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en,en-US;q=0.9",
        "Access-Control-Request-Headers": "authorization",
        "Access-Control-Request-Method": "POST",
        "Connection": "keep-alive",
        "Host": "api.hamsterkombatgame.io",
        "Origin": "https://hamsterkombatgame.io",
        "Referer": "https://hamsterkombatgame.io/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": USER_AGENT
    }

    headers = {
        'Accept': '*/*',
        # 'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8',
        "Accept-Encoding": "gzip, deflate, br, zstd",
        'Accept-Language': 'en,en-US;q=0.9',
        "Authorization": AUTH_TOKEN,
        "Connection": "keep-alive",
        "Host": "api.hamsterkombatgame.io",
        'Origin': 'https://hamsterkombatgame.io',
        # 'Priority': 'u=1, i',
        'Referer': 'https://hamsterkombatgame.io/',
        # 'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
        'sec-ch-ua': SEC_CH_UA,
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        # 'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36 Edg/128.0.0.0',
        'User-Agent': USER_AGENT
    }

    logger.info("Fetching promos...")
    url = 'https://api.hamsterkombatgame.io/clicker/get-promos'

    r = requests.options(url, headers=options_headers)
    r.raise_for_status()

    response = requests.post(url, headers=headers)
    response.raise_for_status()

    data = response.json()
    promos.update(data)

    logger.info("Saving promos...")
    save_json(promos, "promos.json")


def start_playing():
    logger.info("Starting playing mini-games...")
    gp = GamePlayer()
    keys_left = {}
    promo_names = {}

    for promo in promos["promos"]:
        pid = promo["promoId"]
        keys_left[pid] = 4
        promo_names[pid] = promo["title"]["en"]

    for promo in promos["states"]:
        pid = promo["promoId"]
        keys = promo["receiveKeysToday"]
        keys_left[pid] -= keys

    for pid in keys_left:
        name = promo_names[pid]
        logger.info(f"Promo '{name}': {keys_left[pid]} keys left")

        if name not in playlist:
            logger.info(f"Skipping '{name}', due to being under-development")
            continue

        left = keys_left[pid]
        if left:
            logger.info(f"[{name}] Logging the client in...")

            login_data = gp.login(pid)
            if not login_data:
                logger.error(f"[{name}] Failed to login, skipping...")
                continue

            client_id, client_token = login_data

            while left > 0:
                logger.info(f"[{name}] Generating key...")
                key = gp.generate_key(pid, client_id, client_token)
                if key:
                    sleeper = random.randint(0, 20) + random.random()
                    logger.info(f"[{name}] Applying key {key} in {round(sleeper, 2)} seconds ...")
                    time.sleep(sleeper)
                    if apply_promo(key):
                        left -= 1
                else:
                    logger.info(f"[{name}] Failed to generate key, trying again...")

            logger.info(f"Done generating and applying keys for '{name}'")


def main():
    logger.info("HamsterKombat MiniGame autoplayer is started")
    get_promos()
    start_playing()


if __name__ == '__main__':
    main()
