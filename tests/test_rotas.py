import pytest

import app as aplicacao


@pytest.fixture
def cliente():
    aplicacao.app.config["TESTING"] = True
    with aplicacao.app.test_client() as cliente:
        yield cliente


@pytest.fixture
def palavra_fixa(monkeypatch):
    """Faz o sorteio da Forca sempre devolver a palavra 'uva'."""
    monkeypatch.setattr("src.forca.sortear_palavra", lambda dificuldade="aleatoria": ("Frutas", "uva"))


def jogar_letras(cliente, letras):
    resposta = None
    for letra in letras:
        resposta = cliente.post("/api/forca/letra", json={"letra": letra})
    return resposta


# ---------- páginas ----------

@pytest.mark.parametrize("rota", ["/", "/forca", "/conversor", "/senhas"])
def test_paginas_carregam(cliente, rota):
    resposta = cliente.get(rota)
    assert resposta.status_code == 200
    assert "text/html" in resposta.content_type


def test_home_tem_um_cartao_para_cada_exercicio(cliente):
    html = cliente.get("/").get_data(as_text=True)
    for exercicio in aplicacao.EXERCICIOS:
        assert exercicio["nome"] in html
    for rota in ["/forca", "/conversor", "/senhas"]:
        assert f'href="{rota}"' in html


def test_todo_exercicio_da_lista_tem_rota_ativa(cliente):
    for exercicio in aplicacao.EXERCICIOS:
        assert exercicio["rota"] in aplicacao.app.view_functions


def test_menu_destaca_a_pagina_atual(cliente):
    html = cliente.get("/senhas").get_data(as_text=True)
    assert 'class="ativo">Gerador de senhas' in html


@pytest.mark.parametrize("arquivo", [
    "estilo.css", "tema.js", "forca.js", "conversor.js", "senhas.js",
])
def test_arquivos_estaticos_existem(cliente, arquivo):
    assert cliente.get(f"/static/{arquivo}").status_code == 200


# ---------- 404 ----------

def test_pagina_inexistente_mostra_404_com_link_para_o_inicio(cliente):
    resposta = cliente.get("/nao-existe")
    assert resposta.status_code == 404
    html = resposta.get_data(as_text=True)
    assert "404" in html
    assert 'href="/"' in html


def test_rota_de_api_inexistente_devolve_json(cliente):
    resposta = cliente.get("/api/nao-existe")
    assert resposta.status_code == 404
    assert resposta.get_json() == {"erro": "Rota não encontrada."}


def test_metodo_nao_permitido(cliente):
    assert cliente.get("/api/senhas/gerar").status_code == 405


# ---------- Forca ----------

def test_forca_estado_inicial(cliente):
    dados = cliente.get("/api/forca").get_json()
    assert dados["situacao"] == "jogando"
    assert dados["erros"] == 0
    assert dados["palavra"] is None
    assert dados["placar"] == {"vitorias": 0, "derrotas": 0}


def test_forca_nao_revela_a_palavra_durante_o_jogo(cliente, palavra_fixa):
    cliente.post("/api/forca/novo", json={})
    resposta = cliente.get("/api/forca")
    assert "uva" not in resposta.get_data(as_text=True).lower()
    dados = resposta.get_json()
    assert dados["palavra"] is None
    assert dados["exibicao"] == "_ _ _"


def test_forca_novo_jogo_com_dificuldade(cliente):
    resposta = cliente.post("/api/forca/novo", json={"dificuldade": "dificil"})
    assert resposta.status_code == 200
    dados = resposta.get_json()
    assert dados["dificuldade"] == "dificil"
    assert len(dados["exibicao"].split(" ")) >= 9


def test_forca_dificuldade_invalida(cliente):
    resposta = cliente.post("/api/forca/novo", json={"dificuldade": "impossivel"})
    assert resposta.status_code == 400
    assert "erro" in resposta.get_json()


def test_forca_letra_certa_e_errada(cliente, palavra_fixa):
    cliente.post("/api/forca/novo", json={})
    certa = cliente.post("/api/forca/letra", json={"letra": "u"}).get_json()
    assert certa["exibicao"] == "U _ _"
    errada = cliente.post("/api/forca/letra", json={"letra": "z"}).get_json()
    assert errada["erros"] == 1
    assert errada["letras_erradas"] == ["z"]


@pytest.mark.parametrize("corpo", [{"letra": ""}, {"letra": "ab"}, {"letra": "1"}, {}])
def test_forca_letra_invalida(cliente, palavra_fixa, corpo):
    cliente.post("/api/forca/novo", json={})
    resposta = cliente.post("/api/forca/letra", json=corpo)
    assert resposta.status_code == 400
    assert "erro" in resposta.get_json()


def test_forca_letra_repetida(cliente, palavra_fixa):
    cliente.post("/api/forca/novo", json={})
    cliente.post("/api/forca/letra", json={"letra": "z"})
    resposta = cliente.post("/api/forca/letra", json={"letra": "z"})
    assert resposta.status_code == 400
    assert resposta.get_json()["erros"] == 1


def test_forca_vitoria_soma_ao_placar_uma_vez(cliente, palavra_fixa):
    cliente.post("/api/forca/novo", json={})
    dados = jogar_letras(cliente, "uva").get_json()
    assert dados["situacao"] == "venceu"
    assert dados["palavra"] == "uva"
    assert dados["placar"] == {"vitorias": 1, "derrotas": 0}

    # jogada depois do fim é recusada e não conta de novo
    assert cliente.post("/api/forca/letra", json={"letra": "x"}).status_code == 400
    assert cliente.get("/api/forca").get_json()["placar"] == {"vitorias": 1, "derrotas": 0}


def test_forca_derrota_soma_ao_placar_e_revela_a_palavra(cliente, palavra_fixa):
    cliente.post("/api/forca/novo", json={})
    dados = jogar_letras(cliente, "bcdefg").get_json()
    assert dados["situacao"] == "perdeu"
    assert dados["palavra"] == "uva"
    assert dados["placar"] == {"vitorias": 0, "derrotas": 1}


def test_forca_placar_acumula_entre_partidas(cliente, palavra_fixa):
    for _ in range(2):
        cliente.post("/api/forca/novo", json={})
        jogar_letras(cliente, "uva")
    cliente.post("/api/forca/novo", json={})
    jogar_letras(cliente, "bcdefg")
    assert cliente.get("/api/forca").get_json()["placar"] == {"vitorias": 2, "derrotas": 1}


def test_forca_sessoes_diferentes_nao_se_misturam(palavra_fixa):
    with aplicacao.app.test_client() as primeiro, aplicacao.app.test_client() as segundo:
        primeiro.post("/api/forca/novo", json={})
        jogar_letras(primeiro, "uva")
        assert segundo.get("/api/forca").get_json()["placar"] == {"vitorias": 0, "derrotas": 0}


# ---------- Conversor ----------

def test_conversor_converte(cliente):
    resposta = cliente.post("/api/conversor", json={"tipo": "c_f", "valor": "100"})
    assert resposta.status_code == 200
    dados = resposta.get_json()
    assert dados["resultado"] == 212
    assert dados["texto"] == "100 °C = 212 °F"


def test_conversor_aceita_virgula(cliente):
    dados = cliente.post("/api/conversor", json={"tipo": "dolar_real", "valor": "2,5"}).get_json()
    assert dados["valor"] == 2.5


@pytest.mark.parametrize("corpo", [
    {"tipo": "c_f", "valor": ""},
    {"tipo": "c_f", "valor": "abc"},
    {"tipo": "km_milhas", "valor": "-5"},
    {"tipo": "invalido", "valor": "10"},
    {"valor": "10"},
    {},
])
def test_conversor_entrada_invalida(cliente, corpo):
    resposta = cliente.post("/api/conversor", json=corpo)
    assert resposta.status_code == 400
    assert resposta.get_json()["erro"]


def test_conversor_sem_corpo_json(cliente):
    assert cliente.post("/api/conversor", data="texto solto").status_code == 400


def test_pagina_do_conversor_lista_todas_as_conversoes(cliente):
    html = cliente.get("/conversor").get_data(as_text=True)
    assert html.count("data-inverso") >= 6


# ---------- Gerador de senhas ----------

def test_senhas_gera_uma_senha_com_forca(cliente):
    resposta = cliente.post("/api/senhas/gerar", json={"tamanho": 16, "tipos": ["minusculas", "numeros"]})
    assert resposta.status_code == 200
    (item,) = resposta.get_json()["senhas"]
    assert len(item["senha"]) == 16
    assert item["forca"]["nivel"] in {"fraca", "media", "forte", "muito_forte"}
    assert item["forca"]["bits"] > 0


def test_senhas_gera_varias(cliente):
    dados = cliente.post(
        "/api/senhas/gerar", json={"tamanho": "10", "quantidade": "4", "tipos": ["maiusculas"]},
    ).get_json()
    assert len(dados["senhas"]) == 4


def test_senhas_evitar_parecidos(cliente):
    dados = cliente.post(
        "/api/senhas/gerar",
        json={"tamanho": 40, "quantidade": 10, "tipos": ["minusculas", "maiusculas", "numeros"], "sem_parecidos": True},
    ).get_json()
    for item in dados["senhas"]:
        assert not any(c in "0O1lI" for c in item["senha"])


@pytest.mark.parametrize("corpo", [
    {"tamanho": "abc", "tipos": ["numeros"]},
    {"tamanho": 2, "tipos": ["numeros"]},
    {"tamanho": 100, "tipos": ["numeros"]},
    {"tamanho": 10, "tipos": []},
    {"tamanho": 10, "tipos": "numeros"},
    {"tamanho": 10, "tipos": ["emojis"]},
    {"tamanho": 10, "tipos": ["numeros"], "quantidade": 0},
    {"tamanho": 10, "tipos": ["numeros"], "quantidade": 11},
    {"tamanho": 10, "tipos": ["numeros"], "quantidade": "x"},
    {},
])
def test_senhas_entrada_invalida(cliente, corpo):
    resposta = cliente.post("/api/senhas/gerar", json=corpo)
    assert resposta.status_code == 400
    assert resposta.get_json()["erro"]
