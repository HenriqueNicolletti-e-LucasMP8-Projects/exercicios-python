import random

PALAVRAS = ["python", "programa", "variavel", "funcao", "teclado", "computador", "algoritmo", "biblioteca"]
MAX_ERROS = 6


def sortear_palavra():
    return random.choice(PALAVRAS)


def novo_jogo(palavra=None):
    return {
        "palavra": palavra or sortear_palavra(),
        "letras_certas": [],
        "letras_erradas": [],
    }


def montar_exibicao(palavra, letras_certas):
    return " ".join(letra.upper() if letra in letras_certas else "_" for letra in palavra)


def situacao(estado):
    if all(letra in estado["letras_certas"] for letra in estado["palavra"]):
        return "venceu"
    if len(estado["letras_erradas"]) >= MAX_ERROS:
        return "perdeu"
    return "jogando"


def tentar_letra(estado, letra):
    """Registra a tentativa no estado. Levanta ValueError se a jogada for inválida."""
    letra = letra.strip().lower()
    if len(letra) != 1 or not letra.isalpha():
        raise ValueError("Digite apenas uma letra.")
    if situacao(estado) != "jogando":
        raise ValueError("O jogo já terminou.")
    if letra in estado["letras_certas"] or letra in estado["letras_erradas"]:
        raise ValueError("Você já tentou essa letra.")

    if letra in estado["palavra"]:
        estado["letras_certas"].append(letra)
    else:
        estado["letras_erradas"].append(letra)
    return estado


def estado_publico(estado):
    """Dados que podem ir para a tela. A palavra só é revelada quando o jogo termina."""
    resultado = situacao(estado)
    revelar = resultado != "jogando"
    letras_visiveis = set(estado["palavra"]) if revelar else set(estado["letras_certas"])
    return {
        "exibicao": montar_exibicao(estado["palavra"], letras_visiveis),
        "letras_certas": estado["letras_certas"],
        "letras_erradas": estado["letras_erradas"],
        "erros": len(estado["letras_erradas"]),
        "max_erros": MAX_ERROS,
        "situacao": resultado,
        "palavra": estado["palavra"] if revelar else None,
    }
