from flask import Flask, render_template, jsonify, request
from vetor_json import generate_vetor_json

app = Flask(__name__)


@app.route('/')
def index():
    vetor_json = generate_vetor_json()
    if "error" in vetor_json:
        return render_template('error.html', error=vetor_json["error"])
    return render_template('vetor.html', vetor_json=vetor_json)


@app.route('/vetor_json')
def get_vetor_json():
    tamanho_vetor = request.args.get('tamanho_vetor', default=1000, type=int)
    vetor_json = generate_vetor_json(tamanho_vetor)
    return jsonify(vetor_json)


if __name__ == '__main__':
    app.run(debug=True)
