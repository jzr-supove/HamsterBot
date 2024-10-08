import json
import random
import time
from threading import Event, Thread

import requests
from loguru import logger

from config import configure_logger, DEBUG, USER_AGENT, AUTH_TOKEN, SEC_CH_UA
from emulator import Emulator
from helper import save_json, decompress_response, load_json

if DEBUG:
    configure_logger("DEBUG")
else:
    configure_logger("INFO")

promos = load_json("promos.json")

playlist = {
    "Twerk Race",
    'Train Miner',
    'Chain Cube 2048',
    'Mud Racing',
    "Mow and Trim",
    "Polysphere",
    "Cafe Dash",
    "Gangs Wars",
    "Zoopolis",
    "Stone Age",
    "Tile Trio",
    "Fluff Crusade",
    "Count Masters"
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
        'sec-ch-ua': SEC_CH_UA,
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
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
    url = 'https://api.hamsterkombatgame.io/interlude/apply-promo'

    r = requests.options(url, headers=options_headers)
    r.raise_for_status()

    data = {'promoCode': code}
    response = requests.post(url, headers=headers, json=data, timeout=15)
    response.raise_for_status()

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
        'sec-ch-ua': SEC_CH_UA,
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": USER_AGENT
    }

    headers = {
        'Accept': '*/*',
        "Accept-Encoding": "gzip, deflate, br, zstd",
        'Accept-Language': 'en,en-US;q=0.9',
        "Authorization": AUTH_TOKEN,
        "Connection": "keep-alive",
        "Host": "api.hamsterkombatgame.io",
        'Origin': 'https://hamsterkombatgame.io',
        'Referer': 'https://hamsterkombatgame.io/',
        'sec-ch-ua': SEC_CH_UA,
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': USER_AGENT
    }

    logger.info("Fetching promos...")
    url = 'https://api.hamsterkombatgame.io/interlude/get-promos'

    r = requests.options(url, headers=options_headers)
    r.raise_for_status()

    response = requests.post(url, headers=headers, timeout=15)
    response.raise_for_status()

    content = decompress_response(response)

    try:
        json_data = json.loads(content.decode('utf-8'))
    except Exception as e:
        logger.error(f"Failed to parse JSON: {e}, content saved at 'js_debug' file for debugging")

        with open("js_debug", mode="wb") as f:
            f.write(response.content)

        return False

    promos.update(json_data)

    logger.info("Saving promos...")
    save_json(promos, "promos.json")
    return True


def start_playing():
    logger.info("Starting playing mini-games...")
    gp = Emulator()
    keys_left = {}
    promo_names = {}

    for promo in promos["promos"]:
        pid = promo["promoId"]
        name = promo["title"]["en"]
        if name == "Fluff Crusade":
            keys_left[pid] = 8
        else:
            keys_left[pid] = 4
        promo_names[pid] = name

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
            cd = round(random.randint(15, 60) + random.random(), 3)
            logger.info(f"[{name}] Starting in {cd} seconds...")
            time.sleep(cd)

            logger.info(f"[{name}] Logging the client in...")
            login_data = gp.login(pid)
            if not login_data:
                logger.error(f"[{name}] Failed to login, skipping...")
                continue

            client_id, client_token = login_data

            stop_event = t = None

            if name == "Stone Age":
                stop_event = Event()

                def thread_func(stop: Event):
                    logger.info(f"[{name}] get_client thread started")

                    while not stop.is_set():
                        time.sleep(60 + random.random())
                        if not stop.is_set():
                            gp.get_client(pid, client_token)
                            logger.info(f"[{name}] get_client")

                    logger.info(f"[{name}] get_client thread ended")

                t = Thread(target=thread_func, args=(stop_event,))
                t.start()

            fails = 0
            while left > 0:
                logger.info(f"[{name}] Generating key...")
                key = gp.generate_key(pid, client_id, client_token)
                if key:
                    secs = random.randint(5, 15) + random.random()
                    logger.info(f"[{name}] Applying key {key} in {round(secs, 2)} seconds ...")
                    time.sleep(secs)

                    try:
                        if apply_promo(key):
                            left -= 1
                    except Exception as e:
                        logger.error(f"[{name}] Failed to apply key: {e}")
                        fails += 1
                else:
                    logger.info(f"[{name}] Failed to generate key, trying again...")
                    fails += 1

                if fails >= 3:
                    logger.error(f"[{name}] Failed to generate or apply keys 3 times, skipping...")
                    break

            logger.info(f"Done generating and applying keys for '{name}'")

            if stop_event and t:
                stop_event.set()
                t.join()


def main():
    logger.info("HamsterKombat MiniGame autoplayer is started")
    if get_promos():
        start_playing()


if __name__ == '__main__':
    main()
