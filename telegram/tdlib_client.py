import json
import os
from ctypes import CDLL, CFUNCTYPE, c_char_p, c_double, c_int
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

        self._td_receive = self.tdjson.td_receive
        self._td_receive.restype = c_char_p
        self._td_receive.argtypes = [c_double]

        self._td_send = self.tdjson.td_send
        self._td_send.argtypes = [c_int, c_char_p]

    def send(self, query: dict):
        self._td_send(self.client_id, json.dumps(query).encode())

    def receive(self, timeout=1.0):
        res = self._td_receive(timeout)
        if res:
            return json.loads(res.decode())
        return None
