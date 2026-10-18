import pytest

from src import forca


def test_novo_jogo_comeca_vazio():
    estado = forca.novo_jogo("python")
    assert estado == {"palavra": "python", "letras_certas": [], "letras_erradas": []}
    assert forca.situacao(estado) == "jogando"


def test_sortear_palavra_vem_da_lista():
    assert forca.sortear_palavra() in forca.PALAVRAS


def test_montar_exibicao_esconde_letras_nao_descobertas():
    assert forca.montar_exibicao("casa", ["a"]) == "_ A _ A"
    assert forca.montar_exibicao("casa", []) == "_ _ _ _"


def test_letra_certa_e_errada():
    estado = forca.novo_jogo("casa")
    forca.tentar_letra(estado, "a")
    forca.tentar_letra(estado, "z")
    assert estado["letras_certas"] == ["a"]
    assert estado["letras_erradas"] == ["z"]


def test_letra_aceita_maiuscula_e_espacos():
    estado = forca.novo_jogo("casa")
    forca.tentar_letra(estado, " A ")
    assert estado["letras_certas"] == ["a"]


@pytest.mark.parametrize("entrada", ["", "ab", "1", "!", " "])
def test_entrada_invalida(entrada):
    estado = forca.novo_jogo("casa")
    with pytest.raises(ValueError):
        forca.tentar_letra(estado, entrada)


def test_letra_repetida_nao_conta_erro():
    estado = forca.novo_jogo("casa")
    forca.tentar_letra(estado, "z")
    with pytest.raises(ValueError):
        forca.tentar_letra(estado, "z")
    assert estado["letras_erradas"] == ["z"]


def test_vitoria():
    estado = forca.novo_jogo("ola")
    for letra in "ola":
        forca.tentar_letra(estado, letra)
    assert forca.situacao(estado) == "venceu"


def test_derrota_apos_max_erros():
    estado = forca.novo_jogo("a")
    for letra in "bcdefg":
        forca.tentar_letra(estado, letra)
    assert forca.situacao(estado) == "perdeu"


def test_nao_aceita_jogada_depois_do_fim():
    estado = forca.novo_jogo("a")
    forca.tentar_letra(estado, "a")
    with pytest.raises(ValueError):
        forca.tentar_letra(estado, "b")


def test_estado_publico_esconde_palavra_durante_o_jogo():
    estado = forca.novo_jogo("casa")
    forca.tentar_letra(estado, "c")
    publico = forca.estado_publico(estado)
    assert publico["palavra"] is None
    assert publico["exibicao"] == "C _ _ _"


def test_estado_publico_revela_palavra_ao_perder():
    estado = forca.novo_jogo("a")
    for letra in "bcdefg":
        forca.tentar_letra(estado, letra)
    publico = forca.estado_publico(estado)
    assert publico["palavra"] == "a"
    assert publico["exibicao"] == "A"
