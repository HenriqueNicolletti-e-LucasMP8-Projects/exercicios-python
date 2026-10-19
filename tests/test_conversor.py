import pytest

from src import conversor


def test_km_e_milhas():
    assert conversor.km_para_milhas(1.609344) == pytest.approx(1)
    assert conversor.milhas_para_km(1) == pytest.approx(1.609344)


def test_celsius_e_fahrenheit():
    assert conversor.celsius_para_fahrenheit(0) == 32
    assert conversor.celsius_para_fahrenheit(100) == 212
    assert conversor.fahrenheit_para_celsius(32) == 0
    assert conversor.fahrenheit_para_celsius(-40) == -40


def test_real_e_dolar_usam_cotacao_fixa():
    assert conversor.dolares_para_reais(1) == conversor.COTACAO_DOLAR
    assert conversor.reais_para_dolares(conversor.COTACAO_DOLAR) == 1


@pytest.mark.parametrize("tipo", list(conversor.CONVERSOES))
def test_ida_e_volta_volta_ao_valor_original(tipo):
    pares = {"km_milhas": "milhas_km", "milhas_km": "km_milhas", "c_f": "f_c",
             "f_c": "c_f", "real_dolar": "dolar_real", "dolar_real": "real_dolar"}
    ida = conversor.CONVERSOES[tipo]["funcao"]
    volta = conversor.CONVERSOES[pares[tipo]]["funcao"]
    assert volta(ida(37.5)) == pytest.approx(37.5)


def test_converter_monta_resultado():
    resposta = conversor.converter("c_f", "100")
    assert resposta["resultado"] == 212
    assert resposta["texto"] == "100 °C = 212 °F"


def test_converter_aceita_virgula_e_espacos():
    resposta = conversor.converter("dolar_real", " 2,5 ")
    assert resposta["valor"] == 2.5
    assert resposta["resultado"] == 12.5
    assert resposta["texto"] == "2,5 US$ = 12,5 R$"


def test_converter_arredonda_em_duas_casas():
    assert conversor.converter("km_milhas", "10")["resultado"] == 6.21


def test_temperatura_aceita_negativo():
    assert conversor.converter("c_f", "-40")["resultado"] == -40


@pytest.mark.parametrize("tipo", ["km_milhas", "milhas_km", "real_dolar", "dolar_real"])
def test_distancia_e_dinheiro_nao_aceitam_negativo(tipo):
    with pytest.raises(ValueError):
        conversor.converter(tipo, "-1")


@pytest.mark.parametrize("entrada", ["", "   ", "abc", "1,2,3", "1e", "nan", "inf", "--5"])
def test_entrada_invalida(entrada):
    with pytest.raises(ValueError):
        conversor.converter("km_milhas", entrada)


def test_tipo_invalido():
    with pytest.raises(ValueError):
        conversor.converter("litros_galoes", "10")


def test_opcoes_tem_pelo_menos_tres_tipos():
    tipos = [opcao["tipo"] for opcao in conversor.opcoes()]
    assert len(tipos) >= 3
    assert "km_milhas" in tipos and "c_f" in tipos and "real_dolar" in tipos
