const botaoTema = document.getElementById("botao-tema");

function temaAtual() {
  const escolhido = document.documentElement.dataset.tema;
  if (escolhido) return escolhido;
  return window.matchMedia("(prefers-color-scheme: dark)").matches ? "escuro" : "claro";
}

function atualizarBotao() {
  const escuro = temaAtual() === "escuro";
  botaoTema.textContent = escuro ? "☀️ Tema claro" : "🌙 Tema escuro";
  botaoTema.setAttribute("aria-label", escuro ? "Mudar para o tema claro" : "Mudar para o tema escuro");
}

botaoTema.addEventListener("click", () => {
  const novo = temaAtual() === "escuro" ? "claro" : "escuro";
  document.documentElement.dataset.tema = novo;
  try {
    localStorage.setItem("tema", novo);
  } catch {
    // sem armazenamento: o tema vale só até recarregar a página
  }
  atualizarBotao();
});

atualizarBotao();
