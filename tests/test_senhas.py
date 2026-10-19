import string

import pytest

from src import senhas


def test_senha_tem_o_tamanho_pedido():
    assert len(senhas.gerar_senha(12, ["minusculas"])) == 12


def test_tamanho_aceita_texto_numerico():
    assert len(senhas.gerar_senha(" 10 ", ["numeros"])) == 10


@pytest.mark.parametrize("tipo, conjunto", [
    ("minusculas", string.ascii_lowercase),
    ("maiusculas", string.ascii_uppercase),
    ("numeros", string.digits),
    ("simbolos", senhas.TIPOS["simbolos"]),
])
def test_senha_usa_somente_o_tipo_escolhido(tipo, conjunto):
    senha = senhas.gerar_senha(20, [tipo])
    assert all(caractere in conjunto for caractere in senha)


def test_senha_tem_pelo_menos_um_de_cada_tipo_escolhido():
    for _ in range(100):
        senha = senhas.gerar_senha(4, list(senhas.TIPOS))
        assert any(c in string.ascii_lowercase for c in senha)
        assert any(c in string.ascii_uppercase for c in senha)
        assert any(c in string.digits for c in senha)
        assert any(c in senhas.TIPOS["simbolos"] for c in senha)


def test_senhas_geradas_variam():
    assert len({senhas.gerar_senha(16, list(senhas.TIPOS)) for _ in range(20)}) > 1


@pytest.mark.parametrize("valor", ["", "abc", "1.5", None, True, 3, 65, 0, -5])
def test_tamanho_invalido(valor):
    with pytest.raises(ValueError):
        senhas.validar_tamanho(valor)


def test_limites_do_tamanho_sao_aceitos():
    assert senhas.validar_tamanho(senhas.TAMANHO_MINIMO) == senhas.TAMANHO_MINIMO
    assert senhas.validar_tamanho(senhas.TAMANHO_MAXIMO) == senhas.TAMANHO_MAXIMO


def test_sem_tipo_escolhido():
    with pytest.raises(ValueError):
        senhas.gerar_senha(10, [])


def test_tipo_desconhecido():
    with pytest.raises(ValueError):
        senhas.gerar_senha(10, ["emojis"])


def test_evitar_caracteres_parecidos():
    for _ in range(200):
        senha = senhas.gerar_senha(30, list(senhas.TIPOS), sem_parecidos=True)
        assert not any(c in senhas.CARACTERES_PARECIDOS for c in senha)


def test_evitar_parecidos_mantem_um_de_cada_tipo():
    for _ in range(100):
        senha = senhas.gerar_senha(4, list(senhas.TIPOS), sem_parecidos=True)
        assert any(c in string.ascii_lowercase for c in senha)
        assert any(c in string.ascii_uppercase for c in senha)
        assert any(c in string.digits for c in senha)
        assert any(c in senhas.TIPOS["simbolos"] for c in senha)


def test_gerar_varias_devolve_a_quantidade_pedida():
    lista = senhas.gerar_varias(12, ["minusculas"], 5)
    assert len(lista) == 5
    assert all(len(senha) == 12 for senha in lista)


def test_gerar_varias_por_padrao_gera_uma():
    assert len(senhas.gerar_varias(12, ["numeros"])) == 1


@pytest.mark.parametrize("valor", ["", "abc", "1.5", None, True, 0, -1, senhas.QUANTIDADE_MAXIMA + 1])
def test_quantidade_invalida(valor):
    with pytest.raises(ValueError):
        senhas.validar_quantidade(valor)


def test_limites_da_quantidade_sao_aceitos():
    assert senhas.validar_quantidade(1) == 1
    assert senhas.validar_quantidade(senhas.QUANTIDADE_MAXIMA) == senhas.QUANTIDADE_MAXIMA


def test_forca_cresce_com_tamanho_e_variedade():
    curta = senhas.avaliar_forca("abc")
    media = senhas.avaliar_forca("abcdefghij")
    longa_variada = senhas.avaliar_forca("aB3!aB3!aB3!aB3!aB3!")
    assert curta["bits"] < media["bits"] < longa_variada["bits"]


@pytest.mark.parametrize("senha, nivel", [
    ("1234", "fraca"),
    ("abcdefghij", "media"),
    ("aB3dE6gH9jK", "forte"),
    ("aB3!dE6?gH9&jK2#mN5", "muito_forte"),
])
def test_niveis_de_forca(senha, nivel):
    assert senhas.avaliar_forca(senha)["nivel"] == nivel


def test_forca_de_senha_vazia():
    assert senhas.avaliar_forca("") == {"nivel": "fraca", "bits": 0}
