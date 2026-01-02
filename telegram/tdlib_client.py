import json
import os
from ctypes import CDLL, c_char_p, c_double, c_int
from ctypes.util import find_library
from dotenv import load_dotenv

load_dotenv()


class TDLibClient:
    def __init__(self):
        self.api_id = int(os.getenv("TELEGRAM_API_ID"))
        self.api_hash = os.getenv("TELEGRAM_API_HASH")

        self._load_library()
        self._setup_functions()
        self.client_id = self._td_create_client_id()

    def _load_library(self):
        path = find_library("tdjson")
        if not path:
            raise RuntimeError("tdjson not found")
        self.tdjson = CDLL(path)

    def _setup_functions(self):
        self._td_create_client_id = self.tdjson.td_create_client_id
        self._td_create_client_id.restype = c_int

        self._td_send = self.tdjson.td_send
        self._td_send.argtypes = [c_int, c_char_p]

        self._td_receive = self.tdjson.td_receive
        self._td_receive.restype = c_char_p
        self._td_receive.argtypes = [c_double]

    def send(self, query: dict):
        self._td_send(self.client_id, json.dumps(query).encode())

    def receive(self, timeout=1.0):
        res = self._td_receive(timeout)
        if res:
            return json.loads(res.decode())
        return None

    def login(self):
        while True:
            event = self.receive()
            if not event or event["@type"] != "updateAuthorizationState":
                continue

            state = event["authorization_state"]["@type"]

            if state == "authorizationStateWaitTdlibParameters":
                self.send({
                    "@type": "setTdlibParameters",
                    "database_directory": "tdlib_data",
                    "use_message_database": True,
                    "use_secret_chats": False,
                    "api_id": self.api_id,
                    "api_hash": self.api_hash,
                    "system_language_code": "en",
                    "device_model": "Python",
                    "application_version": "1.0",
                })

            elif state == "authorizationStateWaitPhoneNumber":
                phone = input("Phone: ")
                self.send({
                    "@type": "setAuthenticationPhoneNumber",
                    "phone_number": phone
                })

            elif state == "authorizationStateWaitCode":
                code = input("OTP: ")
                self.send({
                    "@type": "checkAuthenticationCode",
                    "code": code
                })

            elif state == "authorizationStateReady":
                print("Telegram login complete")
                return
