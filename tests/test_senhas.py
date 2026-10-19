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
