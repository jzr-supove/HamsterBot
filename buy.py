import argparse
import random
import time
import typing
from sys import maxsize as MAXSIZE
from threading import Thread, Lock

import requests
from loguru import logger

from config import USER_AGENT, SEC_CH_UA, AUTH_TOKEN, DEBUG, configure_logger
from helper import timestamp_ms, save_json, random_sleep


if DEBUG:
    configure_logger("DEBUG")
else:
    configure_logger("INFO")


option_headers = {
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
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en,en-US;q=0.9",
    "Authorization": AUTH_TOKEN,
    "Connection": "keep-alive",
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


user = {
    "profit_increase": 0,
    "coins_spent": 0,
    "cards_bought": 0,
    "no_coins": False,
}

user_lock = Lock()
api_lock = Lock()


def buy_upgrade(upgrade_id: str) -> typing.Tuple[int, dict]:
    url = "https://api.hamsterkombatgame.io/clicker/buy-upgrade"

    r = requests.options(url, headers=option_headers)
    r.raise_for_status()

    data = {"upgradeId": upgrade_id, "timestamp": timestamp_ms()}

    r = requests.post(url, headers=headers, json=data, timeout=15)

    if r.status_code != 200 and r.status_code != 400:
        r.raise_for_status()

    return r.status_code, r.json()


def upgrades_for_buy():
    url = "https://api.hamsterkombatgame.io/clicker/upgrades-for-buy"

    r = requests.options(url, headers=option_headers)
    r.raise_for_status()

    r = requests.post(url, headers=headers)
    r.raise_for_status()

    return r.json()


def get_upgrade_data(data: dict, upgrade_id: str) -> typing.Optional[dict]:
    for i in data["upgradesForBuy"]:
        if i["id"] == upgrade_id:
            return i


def get_upgrade_efficiency(upgrade: dict) -> float:
    try:
        efficiency = upgrade['price'] / upgrade['profitPerHourDelta']
    except ZeroDivisionError:
        efficiency = MAXSIZE

    return round(efficiency, 3)


def display_upgrade(upgrade: dict):
    logger.info("-----------------------")
    logger.info(f"{upgrade['name']} (lvl {upgrade['level']})")
    logger.info(f"  Price: {upgrade['price']:,}")
    logger.info(f"  PPH:   {upgrade['profitPerHourDelta']:,}")
    logger.info(f"  Eff:   {get_upgrade_efficiency(upgrade)}")
    logger.info("-----------------------")


def display_stats():
    logger.info("----------- STATS -------------")
    logger.info(f"Profit Increase: {user['profit_increase']:,}")
    logger.info(f"Coins Spent:     {user['coins_spent']:,}")
    logger.info(f"Cards Bought:    {user['cards_bought']}")
    logger.info("-------------------------------")


def calculate_efficient_upgrades(data: dict, count: int = 10) -> list:
    upgrades = data['upgradesForBuy']
    available_upgrades = [u for u in upgrades if u['isAvailable'] and not u['isExpired']]

    for upgrade in available_upgrades:
        upgrade['efficiency'] = get_upgrade_efficiency(upgrade)

    sorted_upgrades = sorted(available_upgrades, key=lambda x: x['efficiency'])
    return sorted_upgrades[:count]


def get_upgrades_with_efficiency_lte(data: dict, efficiency_cap: float) -> list:
    available_upgrades = [u for u in data['upgradesForBuy'] if u['isAvailable'] and not u['isExpired']]
    result = []

    for upgrade in available_upgrades:
        efficiency = get_upgrade_efficiency(upgrade)

        if efficiency > efficiency_cap:
            continue

        upgrade['efficiency'] = efficiency
        result.append(upgrade)

    return sorted(result, key=lambda x: x['efficiency'])


def buy_until_efficiency(upgrade: dict, eff: float = 2500):
    tot_errs = 0

    while True:
        with user_lock:
            if user["no_coins"]:
                return

        display_upgrade(upgrade)
        upgrade_id = upgrade["id"]
        try:
            with api_lock:
                st, resp = buy_upgrade(upgrade_id)
        except requests.exceptions.RequestException as e:
            logger.info(f"[{upgrade_id}] Error while buying upgrade: {e}")

            tot_errs += 1
            if tot_errs == 3:
                logger.info(f"[{upgrade_id}] 3 consecutive errors occurred, stopping...")
                return

            random_sleep(8, 15, logger, f"[{upgrade_id}] Sleeping for {{secs}} seconds...")
            continue

        if st == 200:
            with user_lock:
                user["profit_increase"] += upgrade["profitPerHourDelta"]
                user["coins_spent"] += upgrade["price"]
                user["cards_bought"] += 1

            upgrade = get_upgrade_data(resp, upgrade_id)
            efficiency = get_upgrade_efficiency(upgrade)

            logger.info(f"[{upgrade_id}] Successfully bought, next efficiency: {efficiency}")

            if efficiency > eff:
                logger.info(f"[{upgrade_id}] Done buying upgrades till efficiency: {eff}")
                return

            if tot_errs > 0:
                tot_errs = 0

            cd = upgrade.get("cooldownSeconds", 0)
            # Additional cooldown to prevent bot detection
            cd += round(random.randint(10, 30) + random.random(), 2)

            logger.info(f"[{upgrade_id}] Sleeping for {cd} seconds...")
            time.sleep(cd)

        elif st == 400:
            err_code = resp.get("error_code", "")

            if err_code == "UPGRADE_COOLDOWN":
                if cd := resp.get("cooldownSeconds"):
                    logger.info(f"[{upgrade_id}] Still in cooldown. Retrying in {cd} seconds")
                    time.sleep(cd)

            elif err_code == "INSUFFICIENT_FUNDS":
                with user_lock:
                    user["no_coins"] = True
                logger.info(f"[{upgrade_id}] Insufficient funds, stopping buying...")
                return

            else:
                logger.info(f"[{upgrade_id}] Unknown error_code: {err_code}; {resp}")
                return
        else:
            logger.info(f"[{upgrade_id}] Unexpected status code: {st}; {resp}")
            tot_errs += 1
            if tot_errs == 3:
                logger.info(f"[{upgrade_id}] 3 consecutive errors occurred, stopping...")
                return

            random_sleep(8, 15, logger, f"[{upgrade_id}] Sleeping for {{secs}} seconds...")


def infinite_buy(efficiency_cap: int):
    logger.info(f"Starting infinite buy with efficiency limit: {efficiency_cap}")

    upgrades = upgrades_for_buy()
    save_json(upgrades, "upgrades_for_buy.json")

    if not upgrades:
        logger.info("No available upgrades to buy.")
        return

    upgrades_list = get_upgrades_with_efficiency_lte(upgrades, efficiency_cap)
    threads = []

    if len(upgrades_list) == 0:
        logger.info(f"No available upgrades with efficiency below {efficiency_cap} to buy.")
        return

    logger.info(f"Preparing to auto-buy {len(upgrades_list)} cards...")
    for upgrade in upgrades_list:
        with user_lock:
            if user["no_coins"]:
                break

        upgrade_id = upgrade.get("id")
        if upgrade_id:
            logger.info(f"Starting auto-buy loop for card '{upgrade_id}'...")
            thread = Thread(target=buy_until_efficiency, args=(upgrade, efficiency_cap), daemon=True)
            thread.start()
            threads.append(thread)
            random_sleep(5, 10)
        else:
            logger.info("Upgrade has no ID")

    try:
        while any(thread.is_alive() for thread in threads) and not user["no_coins"]:
            time.sleep(1)
        logger.info("All threads have completed. Terminating program...")
    except KeyboardInterrupt:
        logger.info("Received interrupt, exiting program")

    display_stats()


def main():
    parser = argparse.ArgumentParser(description="Script to handle efficiency parameter")
    parser.add_argument("-e", "--efficiency", type=int, default=2000,
                        help="Efficiency limit (default: 2000)")

    args = parser.parse_args()
    infinite_buy(args.efficiency)


if __name__ == '__main__':
    main()
