from flask import Flask, render_template, request, redirect, abort
import dns.resolver
import os
import hashlib
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

# Configuración desde .env
DOMAIN = os.environ.get("DOMAIN", "jxvx.es")
API_PREFIX = os.environ.get("IONOS_API_KEY_PREFIX")
API_SECRET = os.environ.get("IONOS_API_KEY_SECRET")
auth = HTTPBasicAuth(API_PREFIX, API_SECRET)

# Función para consultar registros TXT
def get_txt_for_path(path):
    name = f"{path}.{DOMAIN}"
    try:
        answers = dns.resolver.resolve(name, 'TXT')
    except Exception:
        return None
    for r in answers:
        parts = [p.decode('utf-8') for p in r.strings]
        return "".join(parts)
    return None

# Función para añadir registro TXT en IONOS
def add_txt_record(subdomain, value):
    url = f'https://api.hosting.ionos.com/dns/v1/domains/{DOMAIN}/records'
    data = {
        "name": subdomain,
        "type": "TXT",
        "ttl": 3600,
        "data": value
    }
    response = requests.post(url, json=data, auth=auth)
    if response.status_code in [200, 201]:
        return True
    else:
        print("Error al crear TXT:", response.status_code, response.text)
        return False

# Página principal con formulario
@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    if request.method == 'POST':
        original_url = request.form.get('url', '').strip()
        if not original_url:
            error = "Introduce la URL que quieres acortar."
        elif not (original_url.startswith("http://") or original_url.startswith("https://")):
            error = "La URL debe empezar por http:// o https://."
        else:
            # Generar un hash corto de la URL
            hash_object = hashlib.md5(original_url.encode())
            short_hash = hash_object.hexdigest()[:6]

            # Intentar crear el registro TXT en IONOS
            success = add_txt_record(short_hash, original_url)
            if not success:
                error = "No se pudo crear el registro TXT en IONOS."
            else:
                result = f"{short_hash}.{DOMAIN}"

    return render_template('index.html', domain=DOMAIN, result=result, error=error)

# Redirección a URL original
@app.route('/go/<short>')
def go_short(short):
    url = get_txt_for_path(short)
    if not url:
        return abort(404, description="Short link no encontrado")
    if not (url.startswith("http://") or url.startswith("https://")):
        return abort(500, description="URL en TXT no válida")
    return redirect(url, code=302)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
