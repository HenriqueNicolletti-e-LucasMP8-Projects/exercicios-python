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

# Status
- Forca: pronta (branch `forca`, já na `main`).
- Tela inicial com os 3 cartões: pronta.
- Gerador de senhas: pronto (branch `gerador-senhas`, já na `main`).
- Conversor: pronto (branch `conversor`).

# Estrutura
```
app.py              # rotas Flask e lista EXERCICIOS
src/forca.py        # lógica da forca
src/conversor.py    # lógica do conversor
src/senhas.py       # lógica do gerador de senhas
templates/          # HTML (base.html, inicio.html, um por exercício)
static/             # CSS e JS (estilo.css, um .js por exercício)
tests/              # testes pytest (um test_*.py por exercício)
```

# Como adicionar um exercício
Seguir o padrão da Forca (`src/forca.py`, `templates/forca.html`, `static/forca.js`, `tests/test_forca.py`):
1. Criar a lógica em `src/<exercicio>.py`, sem importar Flask, e os testes em `tests/test_<exercicio>.py`.
2. Criar a página em `templates/<exercicio>.html` (extends `base.html`) e o JS em `static/`.
3. Em `app.py`: criar a rota da página e as rotas `/api/<exercicio>/...`, e trocar `"rota": None` do exercício na lista `EXERCICIOS` pelo nome da função da rota. Isso ativa o cartão na home e o item do menu.
4. Atualizar este arquivo (Status) e a tabela do README.

# Regras
- Lógica separada da interface: os módulos em `src/` não conhecem Flask.
- O estado da Forca fica na sessão do Flask; o navegador só exibe.
- Código simples; nomes de variáveis e funções em português, snake_case.
- Rodar os testes antes de dizer que terminou.
- Nunca commitar `.env` ou chaves.

# Trabalho em dupla
- Cada tela nova (exercício ou página como a home) tem uma branch nova, criada a partir da `main` atualizada (`git pull` antes).
- Não fazer push direto na `main`: abrir pull request e deixar a outra pessoa revisar.
- Dividir os exercícios entre as pessoas para não editar o mesmo arquivo ao mesmo tempo. O ponto de conflito esperado é a lista `EXERCICIOS` em `app.py`: resolver mantendo as duas alterações.
- Cada pessoa commita com o próprio nome do git. Perguntar em qual nome o commit ficará antes de commitar.
- Não reescrever histórico já enviado (sem `push --force`, `reset` ou `rebase` em branch compartilhada).
- Antes de mexer em arquivo existente, ler o conteúdo (já houve um `.gitignore` sobrescrito por engano).

# Comandos
- Instalar: `pip install -r requirements.txt`
- Rodar: `python app.py`
- Testar: `pytest`
