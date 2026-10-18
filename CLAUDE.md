# Contexto
Este repositório é um site com 3 exercícios, escolhidos por um menu de navegação. Cada exercício tem uma tela interativa:

- **Forca**: sorteia uma palavra de uma lista e mostra `_ _ _`. O usuário escolhe letras (botões ou teclado), a tela mostra os erros e o boneco, avisa vitória ou derrota e tem o botão "Novo jogo".
- **Conversor**: seleção entre pelo menos 3 tipos (km↔milhas, °C↔°F, real↔dólar com cotação fixa). Uma função por conversão, e entrada inválida mostra mensagem na tela.
- **Gerador de senhas**: formulário com o tamanho e os tipos de caractere (maiúsculas, números, símbolos). Valida a entrada e mostra a senha gerada.

# Stack
- Python 3 + Flask (rotas e lógica)
- HTML/CSS/JS puro no front, sem frameworks pesados
- pytest para a lógica
- Dependências listadas em `requirements.txt`

# Estrutura
```
app.py              # rotas Flask
src/forca.py        # lógica da forca
src/conversor.py    # lógica do conversor
src/senhas.py       # lógica do gerador de senhas
templates/          # HTML
static/             # CSS e JS
tests/              # testes pytest
```

# Regras
- Lógica separada da interface: os módulos em `src/` não conhecem Flask.
- O estado da Forca fica na sessão do Flask; o navegador só exibe.
- Código simples; nomes de variáveis e funções em português, snake_case.
- Cada exercício tem uma branch separada.
- Rodar os testes antes de dizer que terminou.
- Nunca commitar `.env` ou chaves.

# Comandos
- Instalar: `pip install -r requirements.txt`
- Rodar: `python app.py`
- Testar: `pytest`
