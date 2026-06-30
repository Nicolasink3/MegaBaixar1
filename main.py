import libtorrent as lt
from fastapi import FastAPI
import json
import requests
from urllib.parse import quote
import os

app = FastAPI()

API_KEY = "ba349eac86e427a17432453bad9e3a46"

with open("fonte1.json", "r", encoding="utf-8") as f:
    fonte1 = json.load(f)

downloads = fonte1["downloads"]

headers = {"Authorization": f"Bearer {API_KEY}"}

ses = lt.session()
ses.listen_on(6881, 6891)

settings = ses.get_settings()
settings["alert_mask"] = 0
ses.apply_settings(settings)

downloads_ativos = {}

BASE_DIR = os.path.abspath("./downloads")
os.makedirs(BASE_DIR, exist_ok=True)


def pegar_capa(nome):
    nome = quote(nome)

    r = requests.get(
        f"https://www.steamgriddb.com/api/v2/search/autocomplete/{nome}",
        headers=headers
    )

    if r.status_code != 200:
        return None

    data = r.json().get("data", [])
    if not data:
        return None

    game_id = data[0]["id"]

    r = requests.get(
        f"https://www.steamgriddb.com/api/v2/grids/game/{game_id}?limit=1",
        headers=headers
    )

    if r.status_code != 200:
        return None

    data = r.json().get("data", [])
    if not data:
        return None

    return data[0]["thumb"]


@app.get("/buscar/{nome}")
def buscar(nome: str):
    res = []

    for i, item in enumerate(downloads):
        if nome.lower() in item["title"].lower():
            res.append({
                "titulo": item["title"],
                "capa": pegar_capa(item["title"]),
                "download": f"/download/{i}",
                "status": f"/status/{i}"
            })

    return res


@app.get("/download/{id}")
def download(id: int):

    if id < 0 or id >= len(downloads):
        return {"error": "invalid id"}

    item = downloads[id]

    magnet = item["uris"]
    if isinstance(magnet, list):
        magnet = magnet[0]

    params = {
        "save_path": BASE_DIR,
        "storage_mode": lt.storage_mode_t.storage_mode_allocate
    }

    save_path = os.path.join(BASE_DIR, str(id))

    os.makedirs(save_path, exist_ok=True)

    params = {
        "save_path": save_path,
        "storage_mode": lt.storage_mode_t.storage_mode_allocate
    }

    handle = lt.add_magnet_uri(ses, magnet, params)

    downloads_ativos[str(id)] = handle

    return {
        "status": "started",
        "titulo": item["title"]
    }
    

@app.get("/status/{id}")
def status(id: int):

    handle = downloads_ativos.get(str(id))

    if not handle:
        return {"error": "no handle"}

    s = handle.status()

    return {
        "progress": round(float(s.progress) * 100, 2),
        "peers": s.num_peers,
        "download_rate": s.download_rate,
        "state": str(s.state)
    }