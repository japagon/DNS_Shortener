from flask import Flask, render_template, request
import os, hashlib, requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

DOMAIN = os.getenv("DOMAIN")
ZONE_ID = os.getenv("ZONE_ID")
IONOS_API_KEY = os.getenv("IONOS_API_KEY")
API_BASE = "https://api.hosting.ionos.com/dns/v1"


def hash_corto(url):
    return hashlib.sha1(url.encode()).hexdigest()[:6]


def crear_txt(hash_code, url):

    headers = {
        "X-API-Key": IONOS_API_KEY,
        "Content-Type": "application/json"
    }

    payload = [
        {
        "name": f"{hash_code}.{DOMAIN}",   
        "type": "TXT",
        "content": url,
        "ttl": 300
        }
    ]

    r = requests.post(
        f"{API_BASE}/zones/{ZONE_ID}/records",
        headers=headers,
        json=payload
    )

    print("STATUS:", r.status_code)
    print("RESPUESTA IONOS:", r.text)

    return r.status_code in (200,201)




@app.route("/", methods=["GET", "POST"])
def index():
    hash_generado = None
    error = None

    if request.method == "POST":
        url = request.form.get("url")

        if not url:
            error = "Introduce una URL"
        else:
            h = hash_corto(url)
            if crear_txt(h, url):
                hash_generado = h
            else:
                error = "Error creando TXT en IONOS"

    return render_template("index.html", hash=hash_generado, domain=DOMAIN, error=error)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
