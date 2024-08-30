import random
import time
import typing
import uuid

import requests
from loguru import logger

from helper import save_json, load_json


def gen_uuid4():
    return str(uuid.uuid4())


def gen_uuid4hex():
    return uuid.uuid4().hex


def gen_uuid4hex_short():
    return uuid.uuid4().hex[:16]


def gen_timestamp_random_id():
    timestamp = int(time.time() * 1000)
    random_numbers = ''.join(str(random.randint(0, 9)) for _ in range(19))
    return f"{timestamp}-{random_numbers}"


def gen_timestamp_id():
    return str(int(time.time() * 1000))


def gen_gangswars_cid():
    unique_id = uuid.uuid4().hex
    return f"duqdh_{unique_id}"


def gen_gangswars_eid():
    uuid1 = uuid.uuid4().hex[:16]
    uuid2 = uuid.uuid4().hex[:16]
    return f"{uuid1}-{uuid2}"


games = {
    "b4170868-cef0-424f-8eb9-be0622e8e8e3": {
        'name': 'Chain Cube 2048',
        'appToken': 'd1690a07-3780-4068-810f-9b5bbf2931b2',
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
        "clientVersion": "1.78.42",
        "eventId": gen_uuid4,
        "eventType": "cube_sent",
        "eventDuration": 120,
        'attempts': 10,
    },
    "c4480ac7-e178-4973-8061-9ed5b2e17954": {
        'name': 'Train Miner',
        'appToken': '82647f43-3f87-402d-88dd-09a90025313f',
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
        "clientVersion": "2.6.3",
        "eventId": gen_uuid4,
        "eventType": "hitStatue",
        "eventDuration": 720,
        'attempts': 3,
    },
    "61308365-9d16-4040-8bb0-2f4a4c69074c": {
        'name': 'Twerk Race',
        'appToken': '61308365-9d16-4040-8bb0-2f4a4c69074c',
        'headers': {
            "Accept": "*/*",
            "Accept-Encoding": "deflate, gzip",
            "Content-Type": "application/json",
            "Host": "api.gamepromo.io",
            "User-Agent": "UnityPlayer/2021.3.15f1 (UnityWebRequest/1.0, libcurl/7.84.0-DEV)",
            "X-Unity-Version": "2021.3.15f1"
        },
        "authLower": True,
        "clientOrigin": "android",
        "clientId": gen_timestamp_random_id,
        "eventId": lambda: "StartLevel",
        "eventDuration": 55,
        'attempts': 20,
    },
    "2aaf5aee-2cbc-47ec-8a3f-0962cc14bc71": {
        'name': 'Polysphere',
        'appToken': '2aaf5aee-2cbc-47ec-8a3f-0962cc14bc71',
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
        "clientVersion": "1.15.30",
        "eventId": gen_uuid4,
        "eventType": "test",
        "eventDuration": 20,
        'attempts': 25,
    },
    "ef319a80-949a-492e-8ee0-424fb5fc20a6": {
        'name': 'Mow and Trim',
        'appToken': 'ef319a80-949a-492e-8ee0-424fb5fc20a6',
        "headers": {
            "Accept": "*/*",
            "Accept-Encoding": "deflate, gzip",
            "Content-Type": "application/json",
            "Host": "api.gamepromo.io",
            "User-Agent": "UnityPlayer/2021.3.17f1 (UnityWebRequest/1.0, libcurl/7.84.0-DEV)",
            "X-Unity-Version": "2021.3.17f1"
        },
        "authLower": True,
        "clientOrigin": "android",
        "clientId": gen_timestamp_random_id,
        "eventId": lambda: "StartLevel",
        "eventDuration": 60,
        'attempts': 12,
    },
    "8814a785-97fb-4177-9193-ca4180ff9da8": {
        'name': 'Mud Racing',
        'appToken': '8814a785-97fb-4177-9193-ca4180ff9da8',
        "headers": {
            "Accept": "*/*",
            "Accept-Encoding": "deflate, gzip",
            "Content-Type": "application/json",
            "Host": "api.gamepromo.io",
            "User-Agent": "UnityPlayer/2022.3.40f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)",
            "X-Unity-Version": "2022.3.40f1"
        },
        "authLower": True,
        "clientOrigin": "android",
        "clientId": gen_uuid4,
        "eventId": gen_uuid4,
        "eventType": "racing",
        "eventDuration": 95,
        'attempts': 15,
    },
    "bc0971b8-04df-4e72-8a3e-ec4dc663cd11": {
        'name': 'Cafe Dash',
        'appToken': 'bc0971b8-04df-4e72-8a3e-ec4dc663cd11',
        "headers": {
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,*",
            "Connection": "Keep-Alive",
            "Content-Type": "application/json",
            "Host": "api.gamepromo.io",
            "User-Agent": "Mozilla/5.0"
        },
        "authLower": True,
        "clientOrigin": "android",
        "clientId": gen_uuid4hex_short,
        "clientVersion": "2.24.0",
        "eventId": gen_timestamp_id,
        "eventType": "5visitorsChecks",
        "eventDuration": 85,
        'attempts': 15,
    },
    "c7821fa7-6632-482c-9635-2bd5798585f9": {
        'name': 'Gangs Wars',
        'appToken': 'b6de60a0-e030-48bb-a551-548372493523',
        "headers": {
            "Accept": "*/*",
            "Accept-Encoding": "deflate, gzip",
            "Content-Type": "application/json",
            "Host": "api.gamepromo.io",
            "User-Agent": "UnityPlayer/2022.3.41f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)",
            "X-Unity-Version": "2022.3.41f1"
        },
        "clientOrigin": "android",
        "clientId": gen_gangswars_cid,
        "eventId": gen_gangswars_eid,
        "eventDuration": 70,
        'attempts': 20,
    },
    "b2436c89-e0aa-4aed-8046-9b0515e1c46b": {
        'name': 'Zoopolis',
        'appToken': 'b2436c89-e0aa-4aed-8046-9b0515e1c46b',
        "headers": {
            "Accept": "application/json",
            "Accept-Encoding": "deflate, gzip",
            "Content-Type": "application/json; charset=utf-8",
            "Host": "api.gamepromo.io",
            "User-Agent": "UnityPlayer/2022.3.15f1 (UnityWebRequest/1.0, libcurl/8.4.0-DEV)",
            "X-Unity-Version": "2022.3.15f1"
        },
        "clientOrigin": "android",
        "clientId": gen_uuid4hex,
        "clientVersion": "1.2.7",
        "eventId": gen_uuid4,
        "eventType": "ZoopolisEvent",
        "eventDuration": 80,
        'attempts': 10
    }
}

client_ids = load_json("client_ids.json")


def generate_client_id(promo_id: str):
    return games[promo_id].get("clientId", lambda: gen_uuid4)()


class Emulator:
    LOGIN_URL = "https://api.gamepromo.io/promo/login-client"
    EVENT_URL = "https://api.gamepromo.io/promo/register-event"
    CODE_URL = "https://api.gamepromo.io/promo/create-code"

    def __init__(self):
        pass

    def login_client(self, promo_id: str) -> str:
        game = games[promo_id]
        body = {
            "appToken": game["appToken"],
            "clientOrigin": game["clientOrigin"],
            "clientId": client_ids[promo_id],
        }

        if version := game.get("clientVersion"):
            body["clientVersion"] = version

        response = requests.post(self.LOGIN_URL, headers=game["headers"], json=body)
        response.raise_for_status()
        data = response.json()
        return data["clientToken"]

    def register_event(self, promo_id: str, client_token: str) -> bool:
        game = games[promo_id]

        auth_key = "authorization" if game.get("authLower") else "Authorization"
        headers = {
            **game["headers"],
            auth_key: f"Bearer {client_token}"
        }

        body = {
            "promoId": promo_id,
            "eventId": game["eventId"](),
            "eventOrigin": "undefined"
        }

        if event_type := game.get("eventType"):
            body["eventType"] = event_type

        response = requests.post(self.EVENT_URL, headers=headers, json=body)
        response.raise_for_status()

        data = response.json()
        return data["hasCode"]

    def create_code(self, promo_id: str, client_token: str) -> str:
        game = games[promo_id]

        auth_key = "authorization" if game.get("authLower") else "Authorization"
        headers = {
            **game["headers"],
            auth_key: f"Bearer {client_token}"
        }

        body = {"promoId": promo_id}
        response = requests.post(self.CODE_URL, headers=headers, json=body)
        response.raise_for_status()

        data = response.json()
        return data["promoCode"]

    def login(self, promo_id: str) -> typing.Optional[tuple[str, str]]:
        assert promo_id in games, f"Invalid promoId: {promo_id}"

        if client_ids.get(promo_id):
            client_id = client_ids[promo_id]
            logger.info(f"Using client ID: {client_id}")
        else:
            client_id = generate_client_id(promo_id)
            client_ids[promo_id] = client_id
            logger.info(f"Generated client ID: {client_id}")
            save_json(client_ids, "client_ids.json")

        client_token = self.login_client(promo_id)
        if not client_token:
            logger.error(f"Failed to generate client token for client ID: {client_id}")
            return None

        return client_id, client_token

    def generate_key(self, promo_id: str, client_id: str, client_token: str):
        assert client_id is not None and client_id != "", "client_id is None or empty"
        assert client_token is not None and client_token != "", "client_token is None or empty"

        assert promo_id in games, f"Invalid promoId: {promo_id}"

        game = games[promo_id]
        attempts = game["attempts"]
        duration = game["eventDuration"]

        for i in range(attempts):
            secs = duration + random.randint(0, 15) + random.random()
            logger.info(f"Emulating event progress {i + 1}/{attempts} in {round(secs, 2)} seconds")
            time.sleep(secs)

            has_code = False
            try:
                has_code = self.register_event(promo_id, client_token)
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
            key = self.create_code(promo_id, client_token)
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
