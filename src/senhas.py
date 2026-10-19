import math
import secrets
import string

TAMANHO_MINIMO = 4
TAMANHO_MAXIMO = 64
QUANTIDADE_MAXIMA = 10
CARACTERES_PARECIDOS = "0O1lI"

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


def validar_quantidade(valor):
    """Converte a quantidade de senhas para int. Levanta ValueError se for inválida."""
    if isinstance(valor, bool):
        raise ValueError("Informe a quantidade de senhas como um número.")
    try:
        quantidade = int(str(valor).strip())
    except ValueError:
        raise ValueError("Informe a quantidade de senhas como um número inteiro.")
    if not 1 <= quantidade <= QUANTIDADE_MAXIMA:
        raise ValueError(f"A quantidade deve ficar entre 1 e {QUANTIDADE_MAXIMA}.")
    return quantidade


def validar_tipos(tipos):
    """Devolve a lista de tipos escolhidos. Levanta ValueError se vazia ou desconhecida."""
    escolhidos = [tipo for tipo in TIPOS if tipo in tipos]
    desconhecidos = [tipo for tipo in tipos if tipo not in TIPOS]
    if desconhecidos:
        raise ValueError(f"Tipo de caractere desconhecido: {desconhecidos[0]}.")
    if not escolhidos:
        raise ValueError("Escolha pelo menos um tipo de caractere.")
    return escolhidos


def conjunto_do_tipo(tipo, sem_parecidos=False):
    conjunto = TIPOS[tipo]
    if sem_parecidos:
        conjunto = "".join(c for c in conjunto if c not in CARACTERES_PARECIDOS)
    return conjunto


def gerar_senha(tamanho, tipos, sem_parecidos=False):
    """Gera uma senha com pelo menos um caractere de cada tipo escolhido."""
    tamanho = validar_tamanho(tamanho)
    tipos = validar_tipos(tipos)
    if tamanho < len(tipos):
        raise ValueError("O tamanho é menor que a quantidade de tipos escolhidos.")

    conjuntos = [conjunto_do_tipo(tipo, sem_parecidos) for tipo in tipos]
    todos = "".join(conjuntos)
    caracteres = [secrets.choice(conjunto) for conjunto in conjuntos]
    caracteres += [secrets.choice(todos) for _ in range(tamanho - len(caracteres))]
    secrets.SystemRandom().shuffle(caracteres)
    return "".join(caracteres)


def gerar_varias(tamanho, tipos, quantidade=1, sem_parecidos=False):
    quantidade = validar_quantidade(quantidade)
    return [gerar_senha(tamanho, tipos, sem_parecidos) for _ in range(quantidade)]


def avaliar_forca(senha):
    """Estima a força pela entropia (tamanho x variedade de caracteres usados)."""
    universo = 0
    if any(c in string.ascii_lowercase for c in senha):
        universo += 26
    if any(c in string.ascii_uppercase for c in senha):
        universo += 26
    if any(c in string.digits for c in senha):
        universo += 10
    if any(c not in string.ascii_letters + string.digits for c in senha):
        universo += len(TIPOS["simbolos"])
    bits = len(senha) * math.log2(universo) if universo else 0

    if bits < 40:
        nivel = "fraca"
    elif bits < 60:
        nivel = "media"
    elif bits < 80:
        nivel = "forte"
    else:
        nivel = "muito_forte"
    return {"nivel": nivel, "bits": round(bits)}
