import random

PALAVRAS = {
    "Programação": [
        "python", "programa", "variavel", "funcao", "teclado", "computador", "algoritmo",
        "biblioteca", "servidor", "navegador", "compilador", "banco", "codigo", "rede", "memoria",
    ],
    "Animais": [
        "gato", "cachorro", "elefante", "girafa", "golfinho", "tartaruga", "papagaio",
        "coelho", "cavalo", "leao", "borboleta",
    ],
    "Frutas": [
        "banana", "laranja", "morango", "abacaxi", "melancia", "uva", "manga",
        "cereja", "limao", "framboesa",
    ],
    "Países": [
        "brasil", "portugal", "argentina", "japao", "canada", "mexico",
        "australia", "italia", "franca", "alemanha",
    ],
}
MAX_ERROS = 6

# Faixa de tamanho da palavra (mínimo, máximo) em cada dificuldade.
DIFICULDADES = {
    "facil": (0, 6),
    "medio": (7, 8),
    "dificil": (9, 99),
    "aleatoria": (0, 99),
}


def sortear_palavra(dificuldade="aleatoria"):
    """Devolve (categoria, palavra) respeitando a dificuldade. Levanta ValueError se for desconhecida."""
    if dificuldade not in DIFICULDADES:
        raise ValueError("Dificuldade desconhecida.")
    minimo, maximo = DIFICULDADES[dificuldade]
    candidatas = [
        (categoria, palavra)
        for categoria, palavras in PALAVRAS.items()
        for palavra in palavras
        if minimo <= len(palavra) <= maximo
    ]
    return random.choice(candidatas)


def categoria_da_palavra(palavra):
    for categoria, palavras in PALAVRAS.items():
        if palavra in palavras:
            return categoria
    return None


def novo_jogo(palavra=None, dificuldade="aleatoria"):
    if palavra:
        if dificuldade not in DIFICULDADES:
            raise ValueError("Dificuldade desconhecida.")
        categoria = categoria_da_palavra(palavra)
    else:
        categoria, palavra = sortear_palavra(dificuldade)
    return {
        "palavra": palavra,
        "categoria": categoria,
        "dificuldade": dificuldade,
        "letras_certas": [],
        "letras_erradas": [],
    }


def novo_placar():
    return {"vitorias": 0, "derrotas": 0}


def registrar_resultado(placar, resultado):
    """Soma uma vitória ou derrota ao placar. Ignora o jogo ainda em andamento."""
    if resultado == "venceu":
        placar["vitorias"] += 1
    elif resultado == "perdeu":
        placar["derrotas"] += 1
    return placar


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
        "categoria": estado.get("categoria"),
        "dificuldade": estado.get("dificuldade", "aleatoria"),
        "palavra": estado["palavra"] if revelar else None,
    }
