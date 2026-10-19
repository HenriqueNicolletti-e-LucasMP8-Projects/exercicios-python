import math

COTACAO_DOLAR = 5.00  # quantos reais vale 1 dólar (cotação fixa)
KM_POR_MILHA = 1.609344


def km_para_milhas(km):
    return km / KM_POR_MILHA


def milhas_para_km(milhas):
    return milhas * KM_POR_MILHA


def celsius_para_fahrenheit(celsius):
    return celsius * 9 / 5 + 32


def fahrenheit_para_celsius(fahrenheit):
    return (fahrenheit - 32) * 5 / 9


def reais_para_dolares(reais):
    return reais / COTACAO_DOLAR


def dolares_para_reais(dolares):
    return dolares * COTACAO_DOLAR


CONVERSOES = {
    "km_milhas": {"nome": "km → milhas", "funcao": km_para_milhas, "de": "km", "para": "milhas", "aceita_negativo": False},
    "milhas_km": {"nome": "milhas → km", "funcao": milhas_para_km, "de": "milhas", "para": "km", "aceita_negativo": False},
    "c_f": {"nome": "°C → °F", "funcao": celsius_para_fahrenheit, "de": "°C", "para": "°F", "aceita_negativo": True},
    "f_c": {"nome": "°F → °C", "funcao": fahrenheit_para_celsius, "de": "°F", "para": "°C", "aceita_negativo": True},
    "real_dolar": {"nome": "real → dólar", "funcao": reais_para_dolares, "de": "R$", "para": "US$", "aceita_negativo": False},
    "dolar_real": {"nome": "dólar → real", "funcao": dolares_para_reais, "de": "US$", "para": "R$", "aceita_negativo": False},
}


def ler_numero(texto):
    """Converte o texto digitado em número. Aceita vírgula ou ponto como separador decimal."""
    texto = str(texto).strip().replace(",", ".")
    if not texto:
        raise ValueError("Digite um valor.")
    try:
        numero = float(texto)
    except ValueError:
        raise ValueError("Digite um número válido.") from None
    if not math.isfinite(numero):
        raise ValueError("Digite um número válido.")
    return numero


def converter(tipo, texto):
    """Faz a conversão escolhida. Levanta ValueError se o tipo ou o valor forem inválidos."""
    if tipo not in CONVERSOES:
        raise ValueError("Escolha um tipo de conversão válido.")
    conversao = CONVERSOES[tipo]
    valor = ler_numero(texto)
    if valor < 0 and not conversao["aceita_negativo"]:
        raise ValueError("Esse valor não pode ser negativo.")
    resultado = round(conversao["funcao"](valor), 2)
    return {
        "valor": valor,
        "resultado": resultado,
        "texto": f"{formatar(valor)} {conversao['de']} = {formatar(resultado)} {conversao['para']}",
    }


def formatar(numero):
    """Mostra o número com até 2 casas decimais e vírgula, no padrão brasileiro."""
    texto = f"{numero:.2f}".rstrip("0").rstrip(".")
    if texto == "-0":
        texto = "0"
    return texto.replace(".", ",")


def opcoes():
    """Lista de conversões para montar o seletor na tela."""
    return [{"tipo": tipo, "nome": conversao["nome"]} for tipo, conversao in CONVERSOES.items()]
