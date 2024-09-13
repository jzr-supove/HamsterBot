import time
import typing
from sys import maxsize as MAXSIZE
from threading import Thread

import requests

from config import USER_AGENT, SEC_CH_UA, AUTH_TOKEN
from helper import timestamp_ms, save_json

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

    return efficiency


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


def buy_until_efficiency(upgrade_id: str, eff: float = 2500):
    tot_errs = 0

    while True:
        try:
            st, resp = buy_upgrade(upgrade_id)
        except requests.exceptions.RequestException as e:
            print(f"[{upgrade_id}] Error while buying upgrade: {e}")

            tot_errs += 1
            if tot_errs == 3:
                print(f"[{upgrade_id}] 3 consecutive errors occurred, stopping...")
                return

            print(f"[{upgrade_id}] Sleeping for 10 seconds...")
            time.sleep(10)
            continue

        if st == 200:
            upgrade = get_upgrade_data(resp, upgrade_id)
            efficiency = get_upgrade_efficiency(upgrade)
            print(f"[{upgrade_id}] Successfully bought, efficiency: {efficiency}")

            if efficiency > eff:
                print(f"[{upgrade_id}] Done buying upgrades till efficiency: {eff}")
                return

            if tot_errs > 0:
                tot_errs = 0

            cd = upgrade["cooldownSeconds"]
            print(f"[{upgrade_id}] Sleeping for {cd} seconds...")
            time.sleep(cd)

        elif st == 400:  # st == 400
            if resp.get("error_code", "") == "UPGRADE_COOLDOWN":
                if cd := resp.get("cooldownSeconds"):
                    print(f"[{upgrade_id}] Still in cooldown. Retrying in {cd} seconds")
                    time.sleep(cd)
            else:
                print(f"[{upgrade_id}] Unknown error_code: {resp.get('error_code')}")
                tot_errs += 1
                if tot_errs == 3:
                    print(f"[{upgrade_id}] 3 consecutive errors occurred, stopping...")
                    return

                print(f"[{upgrade_id}] Sleeping for 10 seconds...")
                time.sleep(10)
        else:
            print(f"[{upgrade_id}] Unexpected status code: {st}; {resp}")
            tot_errs += 1
            if tot_errs == 3:
                print(f"[{upgrade_id}] 3 consecutive errors occurred, stopping...")
                return

            print(f"[{upgrade_id}] Sleeping for 10 seconds...")
            time.sleep(10)


def infinite_buy(efficiency_cap: int):
    upgrades = upgrades_for_buy()
    save_json(upgrades, "upgrades_for_buy.json")

    if not upgrades:
        print("No available upgrades to buy.")
        return

    upgrades_list = get_upgrades_with_efficiency_lte(upgrades, efficiency_cap)

    for upgrade in upgrades_list:
        upgrade_id = upgrade.get("id")
        if upgrade_id:
            print(f"Starting thread for upgrade {upgrade_id}...")
            t = Thread(target=buy_until_efficiency, args=(upgrade["id"], efficiency_cap))
            t.start()
            time.sleep(3)
        else:
            print("Upgrade has no ID")


def main():
    upgrades = upgrades_for_buy()
    save_json(upgrades, "upgrades_for_buy.json")

    if not upgrades:
        print("No available upgrades to buy.")
        return

    user_input = ""
    while user_input != "q":
        upgrades_list = calculate_efficient_upgrades(upgrades)

        print("Top 10 Most Efficient Upgrades:")
        for i, upgrade in enumerate(upgrades_list, 1):
            print(f"{i}. {upgrade['name']}")
            print(f"   Price: {upgrade['price']}")
            print(f"   Profit Increase: {upgrade['profitPerHourDelta']} per hour")
            print(f"   Efficiency: {upgrade['efficiency']:.8f}")
            print(f"   Section: {upgrade['section']}")
            print(f"   Level: {upgrade['level']}")
            print("---")

        user_input = input("Enter upgrade ID to buy (or 'q' to quit): ")

        if user_input.isdigit():
            uid = int(user_input)

            if uid < 1 or uid > len(upgrades_list):
                print("Invalid upgrade ID.")
                continue

            upgrade_id = upgrades_list[uid - 1]['id']

            try:
                st, upgrades = buy_upgrade(upgrade_id)
                print(f"Bought upgrade {upgrade_id}")
                save_json(upgrades, "upgrades_for_buy.json")

            except requests.exceptions.RequestException as e:
                print("Couldn't buy upgrade")
                if hasattr(e, 'response'):
                    print(f"Response text: {e.response.text}")


if __name__ == '__main__':
    # main()
    infinite_buy(2200)
