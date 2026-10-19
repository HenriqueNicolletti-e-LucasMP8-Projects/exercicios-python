# Exercícios Python

Site com três exercícios básicos de Python, escolhidos por uma tela inicial e usados de forma interativa no navegador. O back-end é feito com Flask e o front-end com HTML, CSS e JavaScript puros.

## Exercícios

| Exercício | O que faz | Status |
|---|---|---|
| **Forca** | Sorteia uma palavra e mostra `_ _ _`. Você escolhe letras por botões ou pelo teclado, vê o boneco sendo desenhado a cada erro e recebe o aviso de vitória ou derrota. Tem o botão "Novo jogo". | Pronto |
| **Conversor** | Converte km↔milhas, °C↔°F e real↔dólar (cotação fixa), com uma função por conversão e tratamento de entrada inválida. | Em breve |
| **Gerador de senhas** | Pede o tamanho e os tipos de caractere (minúsculas, maiúsculas, números, símbolos), valida a entrada e gera a senha, com botão para copiar. | Pronto |

## Como rodar

Requisitos: Python 3.10 ou superior.

```bash
# 1. Clonar o repositório
git clone https://github.com/HenriqueNicolletti/exercicios-python.git
cd exercicios-python

# 2. (Opcional) criar um ambiente virtual
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux/macOS

# 3. Instalar as dependências
pip install -r requirements.txt

# 4. Iniciar o servidor
python app.py
```

Depois abra <http://127.0.0.1:5000> no navegador.

## Testes

```bash
pytest
```

Os testes ficam em `tests/` e cobrem a lógica de cada exercício, sem depender do Flask.

## Estrutura do projeto

```
app.py              # rotas Flask
src/                # lógica dos exercícios (não conhece o Flask)
  forca.py
  senhas.py
templates/          # páginas HTML (base, início e um por exercício)
static/             # CSS e JavaScript
tests/              # testes com pytest
```

A lógica fica separada da interface: os módulos em `src/` só recebem e devolvem dados simples, e o Flask apenas conecta essa lógica à tela.

## Licença

Distribuído sob a licença MIT. Veja o arquivo [LICENSE](LICENSE).
