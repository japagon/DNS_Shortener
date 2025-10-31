from flask import Flask, render_template, request, redirect, abort
import dns.resolver

app = Flask(__name__)
DOMAIN = "jxvx.es"  
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

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    if request.method == 'POST':
        short = request.form.get('short', '').strip()
        if not short:
            error = "Introduce la clave corta (ej. abc)."
        else:
            url = get_txt_for_path(short)
            if not url:
                error = f"No se encontró TXT para: {short}.{DOMAIN}"
            else:
                # comprobación básica
                if not (url.startswith("http://") or url.startswith("https://")):
                    error = "La URL encontrada no es válida (debe empezar por http:// o https://)."
                    result = url
                else:
                    result = url
    return render_template('index.html', domain=DOMAIN, result=result, error=error)

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