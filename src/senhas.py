import secrets
import string

TAMANHO_MINIMO = 4
TAMANHO_MAXIMO = 64

TIPOS = {
    "minusculas": string.ascii_lowercase,
    "maiusculas": string.ascii_uppercase,
    "numeros": string.digits,
    "simbolos": "!@#$%&*?+-_=",
}


def validar_tamanho(valor):
    """Converte o tamanho para int. Levanta ValueError se for inválido."""
    if isinstance(valor, bool):
        raise ValueError("Informe o tamanho da senha como um número.")
    try:
        tamanho = int(str(valor).strip())
    except ValueError:
        raise ValueError("Informe o tamanho da senha como um número inteiro.")
    if not TAMANHO_MINIMO <= tamanho <= TAMANHO_MAXIMO:
        raise ValueError(f"O tamanho deve ficar entre {TAMANHO_MINIMO} e {TAMANHO_MAXIMO}.")
    return tamanho


def validar_tipos(tipos):
    """Devolve a lista de tipos escolhidos. Levanta ValueError se vazia ou desconhecida."""
    escolhidos = [tipo for tipo in TIPOS if tipo in tipos]
    desconhecidos = [tipo for tipo in tipos if tipo not in TIPOS]
    if desconhecidos:
        raise ValueError(f"Tipo de caractere desconhecido: {desconhecidos[0]}.")
    if not escolhidos:
        raise ValueError("Escolha pelo menos um tipo de caractere.")
    return escolhidos


def gerar_senha(tamanho, tipos):
    """Gera uma senha com pelo menos um caractere de cada tipo escolhido."""
    tamanho = validar_tamanho(tamanho)
    tipos = validar_tipos(tipos)
    if tamanho < len(tipos):
        raise ValueError("O tamanho é menor que a quantidade de tipos escolhidos.")

    todos = "".join(TIPOS[tipo] for tipo in tipos)
    caracteres = [secrets.choice(TIPOS[tipo]) for tipo in tipos]
    caracteres += [secrets.choice(todos) for _ in range(tamanho - len(caracteres))]
    secrets.SystemRandom().shuffle(caracteres)
    return "".join(caracteres)
