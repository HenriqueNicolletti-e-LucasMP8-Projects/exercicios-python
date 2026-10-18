import os

from flask import Flask, jsonify, redirect, render_template, request, session, url_for

from src import forca

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "chave-apenas-para-desenvolvimento")


def estado_da_sessao():
    if "forca" not in session:
        session["forca"] = forca.novo_jogo()
    return session["forca"]


@app.route("/")
def inicio():
    return redirect(url_for("pagina_forca"))


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


if __name__ == "__main__":
    app.run(debug=True)
