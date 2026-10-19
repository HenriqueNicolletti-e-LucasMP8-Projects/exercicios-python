import os

from flask import Flask, jsonify, render_template, request, session

from src import conversor, forca, senhas

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "chave-apenas-para-desenvolvimento")


def estado_da_sessao():
    if "forca" not in session:
        session["forca"] = forca.novo_jogo()
    return session["forca"]


def placar_da_sessao():
    if "forca_placar" not in session:
        session["forca_placar"] = forca.novo_placar()
    return session["forca_placar"]


def resposta_forca(estado):
    return jsonify({**forca.estado_publico(estado), "placar": placar_da_sessao()})


EXERCICIOS = [
    {"nome": "Forca", "descricao": "Adivinhe a palavra letra por letra antes que o boneco seja enforcado.", "rota": "pagina_forca"},
    {"nome": "Conversor", "descricao": "Converta km↔milhas, °C↔°F e real↔dólar.", "rota": "pagina_conversor"},
    {"nome": "Gerador de senhas", "descricao": "Gere senhas escolhendo tamanho e tipos de caractere.", "rota": "pagina_senhas"},
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
    return resposta_forca(estado_da_sessao())


@app.post("/api/forca/novo")
def api_forca_novo():
    dados = request.get_json(silent=True) or {}
    try:
        session["forca"] = forca.novo_jogo(dificuldade=str(dados.get("dificuldade", "aleatoria")))
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400
    return resposta_forca(session["forca"])


@app.post("/api/forca/letra")
def api_forca_letra():
    dados = request.get_json(silent=True) or {}
    estado = estado_da_sessao()
    try:
        forca.tentar_letra(estado, str(dados.get("letra", "")))
    except ValueError as erro:
        return jsonify({"erro": str(erro), **forca.estado_publico(estado), "placar": placar_da_sessao()}), 400
    session["forca"] = estado
    resultado = forca.situacao(estado)
    if resultado != "jogando":
        session["forca_placar"] = forca.registrar_resultado(placar_da_sessao(), resultado)
    return resposta_forca(estado)


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


@app.route("/senhas")
def pagina_senhas():
    return render_template(
        "senhas.html", pagina="senhas",
        tamanho_minimo=senhas.TAMANHO_MINIMO, tamanho_maximo=senhas.TAMANHO_MAXIMO,
        quantidade_maxima=senhas.QUANTIDADE_MAXIMA,
    )


@app.post("/api/senhas/gerar")
def api_senhas_gerar():
    dados = request.get_json(silent=True) or {}
    tipos = dados.get("tipos", [])
    if not isinstance(tipos, list):
        return jsonify({"erro": "Os tipos de caractere devem ser uma lista."}), 400
    try:
        lista = senhas.gerar_varias(
            dados.get("tamanho"), tipos, dados.get("quantidade", 1), bool(dados.get("sem_parecidos", False)),
        )
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400
    return jsonify({"senhas": [{"senha": s, "forca": senhas.avaliar_forca(s)} for s in lista]})


@app.errorhandler(404)
def pagina_nao_encontrada(erro):
    if request.path.startswith("/api/"):
        return jsonify({"erro": "Rota não encontrada."}), 404
    return render_template("404.html", pagina="404"), 404


if __name__ == "__main__":
    app.run(debug=True)
