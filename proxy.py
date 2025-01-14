from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return "Meu Proxy está online! Use /proxy/<url> para acessar."

@app.route('/proxy/<path:url>', methods=['GET', 'POST'])
def proxy(url):
    method = request.method
    headers = {key: value for key, value in request.headers if key.lower() != 'host'}

    if method == 'GET':
        destino = f'http://{url}'
        response = requests.get(destino, headers=headers, params=request.args)
    elif method == 'POST':
        destino = f'http://{url}'
        response = requests.post(destino, headers=headers, data=request.form)

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    proxied_headers = [(nome, valor) for (nome, valor) in response.raw.headers.items() if nome.lower() not in excluded_headers]

    return Response(response.content, response.status_code, proxied_headers)

if __name__ == '__main__':
    # Rodar localmente para testar
    app.run(debug=True, host='0.0.0.0', port=5000)