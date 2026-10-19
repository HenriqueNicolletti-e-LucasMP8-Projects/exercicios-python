import os

from flask import Flask, jsonify, render_template, request, session

from src import conversor, forca

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "chave-apenas-para-desenvolvimento")


def estado_da_sessao():
    if "forca" not in session:
        session["forca"] = forca.novo_jogo()
    return session["forca"]


EXERCICIOS = [
    {"nome": "Forca", "descricao": "Adivinhe a palavra letra por letra antes que o boneco seja enforcado.", "rota": "pagina_forca"},
    {"nome": "Conversor", "descricao": "Converta km↔milhas, °C↔°F e real↔dólar.", "rota": "pagina_conversor"},
    {"nome": "Gerador de senhas", "descricao": "Gere senhas escolhendo tamanho e tipos de caractere.", "rota": None},
]


@app.context_processor
def injetar_exercicios():
    return {"exercicios": EXERCICIOS}


@app.route("/")
def inicio():
    return render_template("inicio.html", pagina="inicio")


@app.route("/forca")
def pagina_forca():
    return render_template("forca.html", pagina="forca")


@app.get("/api/forca")
def api_forca_estado():
    return jsonify(forca.estado_publico(estado_da_sessao()))


@app.post("/api/forca/novo")
def api_forca_novo():
    session["forca"] = forca.novo_jogo()
    return jsonify(forca.estado_publico(session["forca"]))


@app.post("/api/forca/letra")
def api_forca_letra():
    dados = request.get_json(silent=True) or {}
    estado = estado_da_sessao()
    try:
        forca.tentar_letra(estado, str(dados.get("letra", "")))
    except ValueError as erro:
        return jsonify({"erro": str(erro), **forca.estado_publico(estado)}), 400
    session["forca"] = estado
    return jsonify(forca.estado_publico(estado))


@app.route("/conversor")
def pagina_conversor():
    return render_template(
        "conversor.html",
        pagina="conversor",
        opcoes=conversor.opcoes(),
        cotacao=conversor.formatar(conversor.COTACAO_DOLAR),
    )


@app.post("/api/conversor")
def api_conversor():
    dados = request.get_json(silent=True) or {}
    try:
        resposta = conversor.converter(str(dados.get("tipo", "")), str(dados.get("valor", "")))
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400
    return jsonify(resposta)


if __name__ == "__main__":
    app.run(debug=True)
