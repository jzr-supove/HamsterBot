import random
import time
import typing
import uuid

import requests
import urllib3
from loguru import logger

from helper import save_json, load_json


def gen_uuid4():
    return str(uuid.uuid4())


def gen_uuid4hex():
    return uuid.uuid4().hex


def gen_timestamp_id():
    timestamp = int(time.time() * 1000)
    random_numbers = ''.join(str(random.randint(0, 9)) for _ in range(19))
    return f"{timestamp}-{random_numbers}"


games = {
    1: {
        'name': 'Bike Ride 3D',
        'appToken': 'd28721be-fd2d-4b45-869e-9f253b554e50',
        'promoId': '43e35910-c168-4634-ad4f-52fd764a843f',
        "headers": {
            "Connection": "keep-alive",
            "Content-Type": "application/json; charset=utf-8",
            "Host": "api.gamepromo.io",
            "User-Agent": urllib3.util.SKIP_HEADER
        },
        "clientOrigin": "deviceid",
        "clientId": gen_timestamp_id,
        "eventId": gen_uuid4,
        'timing': 85,  # in seconds
        'attempts': 15,
    },
    2: {
        'name': 'Chain Cube 2048',
        'appToken': 'd1690a07-3780-4068-810f-9b5bbf2931b2',
        'promoId': 'b4170868-cef0-424f-8eb9-be0622e8e8e3',
        "headers": {
            "Accept": "application/json",
            "Accept-Encoding": "deflate, gzip",
            "Content-Type": "application/json; charset=utf-8",
            "Host": "api.gamepromo.io",
            "User-Agent": "UnityPlayer/2022.3.20f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)",
            "X-Unity-Version": "2022.3.20f1"
        },
        "clientOrigin": "android",
        "clientId": gen_uuid4,
        "eventId": gen_uuid4,
        'timing': 120,
        'attempts': 10,
    },
    3: {
        'name': 'My Clone Army',
        'appToken': '74ee0b5b-775e-4bee-974f-63e7f4d5bacb',
        'promoId': 'fe693b26-b342-4159-8808-15e3ff7f8767',
        'timing': 180000 / 1000,
        'attempts': 30,
    },
    4: {
        'name': 'Train Miner',
        'appToken': '82647f43-3f87-402d-88dd-09a90025313f',
        'promoId': 'c4480ac7-e178-4973-8061-9ed5b2e17954',
        "headers": {
            "Accept": "*/*",
            "Accept-Encoding": "deflate, gzip",
            "Content-Type": "application/json",
            "Host": "api.gamepromo.io",
            "User-Agent": "UnityPlayer/2022.3.20f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)",
            "X-Unity-Version": "2022.3.20f1"
        },
        "clientOrigin": "android",
        "clientId": gen_uuid4hex,
        "eventId": gen_uuid4,
        'timing': 720,
        'attempts': 3,
    },
    5: {
        'name': 'Merge Away',  # USING WEBSOCKET
        'appToken': '8d1cc2ad-e097-4b86-90ef-7a27e19fb833',
        'promoId': 'dc128d28-c45b-411c-98ff-ac7726fbaea4',
        'timing': 20,
        'attempts': 25,
    },
    6: {
        'name': 'Twerk Race',
        'appToken': '61308365-9d16-4040-8bb0-2f4a4c69074c',
        'promoId': '61308365-9d16-4040-8bb0-2f4a4c69074c',
        'headers': {
            "Accept": "*/*",
            "Accept-Encoding": "deflate, gzip",
            "Content-Type": "application/json",
            "Host": "api.gamepromo.io",
            "User-Agent": "UnityPlayer/2021.3.15f1 (UnityWebRequest/1.0, libcurl/7.84.0-DEV)",
            "X-Unity-Version": "2021.3.15f1"
        },
        "clientOrigin": "android",
        "clientId": gen_timestamp_id,
        "eventId": lambda: "StartLevel",
        'timing': 55,
        'attempts': 20,
    },
    7: {
        'name': 'Polysphere',
        'appToken': '2aaf5aee-2cbc-47ec-8a3f-0962cc14bc71',
        'promoId': '2aaf5aee-2cbc-47ec-8a3f-0962cc14bc71',
        "headers": {
            "Accept": "application/json",
            "Accept-Encoding": "deflate, gzip",
            "Content-Type": "application/json; charset=utf-8",
            "Host": "api.gamepromo.io",
            "User-Agent": "UnityPlayer/2021.3.39f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)",
            "X-Unity-Version": "2021.3.39f1"
        },
        "clientOrigin": "android",
        "clientId": gen_uuid4,
        "eventId": gen_uuid4,
        'timing': 20,
        'attempts': 25,
    },
    8: {
        'name': 'Mow and Trim',
        'appToken': 'ef319a80-949a-492e-8ee0-424fb5fc20a6',
        'promoId': 'ef319a80-949a-492e-8ee0-424fb5fc20a6',
        "headers": {
            "Accept": "*/*",
            "Accept-Encoding": "deflate, gzip",
            "Content-Type": "application/json",
            "Host": "api.gamepromo.io",
            "User-Agent": "UnityPlayer/2021.3.17f1 (UnityWebRequest/1.0, libcurl/7.84.0-DEV)",
            "X-Unity-Version": "2021.3.17f1"
        },
        "clientOrigin": "android",
        "clientId": gen_timestamp_id,
        "eventId": lambda: "StartLevel",
        'timing': 60,
        'attempts': 12,
    },
    9: {
        'name': 'Mud Racing',
        'appToken': '8814a785-97fb-4177-9193-ca4180ff9da8',
        'promoId': '8814a785-97fb-4177-9193-ca4180ff9da8',
        "headers": {
            "Accept": "*/*",
            "Accept-Encoding": "deflate, gzip",
            "Content-Type": "application/json",
            "Host": "api.gamepromo.io",
            "User-Agent": "UnityPlayer/2022.3.40f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)",
            "X-Unity-Version": "2022.3.40f1"
        },
        "clientOrigin": "android",
        "clientId": gen_uuid4,
        "eventId": gen_uuid4,
        'timing': 95,
        'attempts': 15,
    },
    10: {
        'name': 'Cafe Dash',
        'appToken': 'bc0971b8-04df-4e72-8a3e-ec4dc663cd11',
        'promoId': 'bc0971b8-04df-4e72-8a3e-ec4dc663cd11',
        'timing': 20000 / 1000,
        'attempts': 20,
    }
}

client_ids = load_json("client_ids.json")

reverse_ids = {
    '43e35910-c168-4634-ad4f-52fd764a843f': 1,
    'b4170868-cef0-424f-8eb9-be0622e8e8e3': 2,
    'fe693b26-b342-4159-8808-15e3ff7f8767': 3,
    'c4480ac7-e178-4973-8061-9ed5b2e17954': 4,
    'dc128d28-c45b-411c-98ff-ac7726fbaea4': 5,
    '61308365-9d16-4040-8bb0-2f4a4c69074c': 6,
    '2aaf5aee-2cbc-47ec-8a3f-0962cc14bc71': 7,
    'ef319a80-949a-492e-8ee0-424fb5fc20a6': 8,
    '8814a785-97fb-4177-9193-ca4180ff9da8': 9,
    'bc0971b8-04df-4e72-8a3e-ec4dc663cd11': 10
}


def generate_client_id(game_id: int):
    return games[game_id].get("clientId", lambda: gen_uuid4)()


class GamePlayer:
    LOGIN_URL = "https://api.gamepromo.io/promo/login-client"
    EVENT_URL = "https://api.gamepromo.io/promo/register-event"
    CODE_URL = "https://api.gamepromo.io/promo/create-code"

    def __init__(self):
        pass

    def login_client(self, game_id: int) -> str:
        body = {
            "appToken": games[game_id]["appToken"],
            "clientOrigin": games[game_id]["clientOrigin"],
            "clientId": client_ids[game_id],
        }

        if game_id == 2:
            body["clientVersion"] = "1.78.42"
        elif game_id == 4:
            body["clientVersion"] = "2.6.3"
        elif game_id == 7:
            body["clientVersion"] = "1.15.30"

        response = requests.post(self.LOGIN_URL, headers=games[game_id]["headers"], json=body)
        response.raise_for_status()
        data = response.json()
        return data["clientToken"]

    def register_event(self, game_id: int, client_token: str) -> bool:
        game = games[game_id]
        headers = {**game["headers"]}
        if game_id in {6, 9, 8}:  # Twerk, Mud, Mow
            headers["authorization"] = f"Bearer {client_token}"
        else:
            headers["Authorization"] = f"Bearer {client_token}"

        body = {
            "promoId": game["promoId"],
            "eventId": game["eventId"](),
            "eventOrigin": "undefined"
        }

        if game_id == 9:  # Mud Racing
            body["eventType"] = "racing"
        elif game_id == 2:  # Chain Cube
            body["eventType"] = "cube_sent"
        elif game_id == 4:  # Train Miner
            body["eventType"] = "hitStatue"
        elif game_id == 7:  # Polysphere
            body["eventType"] = "test"

        response = requests.post(self.EVENT_URL, headers=headers, json=body)
        response.raise_for_status()
        data = response.json()
        return data["hasCode"]

    def create_code(self, game_id: int, client_token: str) -> str:
        game = games[game_id]
        headers = {**game["headers"]}
        if game_id == 6:  # Twerk
            headers["authorization"] = f"Bearer {client_token}"
        else:
            headers["Authorization"] = f"Bearer {client_token}"

        body = {
            "promoId": game["promoId"]
        }
        response = requests.post(self.CODE_URL, headers=headers, json=body)
        response.raise_for_status()
        data = response.json()
        return data["promoCode"]

    def login(self, promo_id: str) -> typing.Optional[tuple[str, str]]:
        game_id = reverse_ids.get(promo_id)
        assert game_id in games, f"Invalid promoId: {promo_id}"

        if client_ids.get(game_id):
            client_id = client_ids[game_id]
            logger.info(f"Using client ID: {client_id}")
        else:
            client_id = generate_client_id(game_id)
            client_ids[game_id] = client_id
            logger.info(f"Generated client ID: {client_id}")
            save_json(client_ids, "client_ids.json")

        client_token = self.login_client(game_id)
        if not client_token:
            logger.error(f"Failed to generate client token for client ID: {client_id}")
            return None

        return client_id, client_token

    def generate_key(self, promo_id: str, client_id: str, client_token: str):
        assert client_id is not None and client_id != "", "client_id is None or empty"
        assert client_token is not None and client_token != "", "client_token is None or empty"

        game_id = reverse_ids.get(promo_id)
        assert game_id in games, f"Invalid promoId: {promo_id}"

        game = games[game_id]
        attempts = game["attempts"]
        timing = game["timing"]

        for i in range(attempts):
            sl = timing + random.randint(0, 15) + random.random()
            logger.info(f"Emulating event progress {i + 1}/{attempts} in {round(sl, 2)} seconds")
            time.sleep(sl)

            has_code = False
            try:
                has_code = self.register_event(game_id, client_token)
            except requests.RequestException as e:
                logger.error(f"An error occurred: {e}")
                if hasattr(e, 'response'):
                    logger.error(f"Response status code: {e.response.status_code}")
                    logger.error(f"Response text: {e.response.text}")

            except Exception as e:
                logger.error(f"An unexpected error occurred: {e}")

            if has_code:
                logger.info(f"Event triggered key generation, requesting...")
                break

        try:
            key = self.create_code(game_id, client_token)
            logger.info(f"Generated key: {key}")
            return key
        except requests.RequestException as e:
            logger.error(f"An error occurred: {e}")
            if hasattr(e, 'response'):
                logger.error(f"Response status code: {e.response.status_code}")
                logger.error(f"Response text: {e.response.text}")

        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")

        return None
