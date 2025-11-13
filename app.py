from flask import Flask, render_template, request, redirect, abort
import os, hashlib, requests, dns.resolver
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

app = Flask(__name__)

DOMAIN = os.getenv("DOMAIN")
ZONE_ID = os.getenv("ZONE_ID")
IONOS_API_KEY = os.getenv("IONOS_API_KEY")
API_BASE = "https://api.hosting.ionos.com/dns/v1"


def hash_corto(url):
    """Genera un hash corto de 6 caracteres para la URL"""
    return hashlib.sha1(url.encode()).hexdigest()[:6]


def crear_txt(hash_code, url):
    """Crea un registro TXT en IONOS DNS"""
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

    return r.status_code in (200, 201)


def obtener_url_desde_dns(hash_code):
    """Consulta el TXT en DNS y devuelve su contenido"""
    nombre = f"{hash_code}.{DOMAIN}"
    try:
        respuesta = dns.resolver.resolve(nombre, 'TXT')
        for r in respuesta:
            partes = [p.decode('utf-8') for p in r.strings]
            return "".join(partes)
    except Exception as e:
        print("Error resolviendo:", e)
        return None


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


@app.route("/<hash_code>")
def redirigir(hash_code):
    """Redirige al enlace guardado en el DNS"""
    url = obtener_url_desde_dns(hash_code)
    if not url:
        return abort(404, description="No se encontró ese hash en el DNS")
    if not (url.startswith("http://") or url.startswith("https://")):
        url = "https://" + url
    return redirect(url, code=302)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

