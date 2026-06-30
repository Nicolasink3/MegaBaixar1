import json
from urllib.request import Request, urlopen
from urllib.parse import quote_plus

BASE_URL = "http://127.0.0.1:8000"


class ApiClient:

    def buscar(self, nome):
        r = requests.get(f"{BASE_URL}/buscar/{nome}")
        return r.json()

    def baixar(self, game_id):
        r = requests.get(f"{BASE_URL}/download/{game_id}")
        return r.json()

    def status(self, game_id):
        r = requests.get(f"{BASE_URL}/status/{game_id}")
        return r.json()