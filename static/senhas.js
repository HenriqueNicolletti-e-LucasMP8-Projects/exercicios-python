const formulario = document.getElementById("form-senha");
const elMensagem = document.getElementById("mensagem-senha");
const elResultado = document.getElementById("resultado-senha");
const elSenha = document.getElementById("senha");
const botaoCopiar = document.getElementById("copiar");

function mostrarMensagem(texto, classe) {
  elMensagem.textContent = texto;
  elMensagem.className = "mensagem " + (classe || "");
}

formulario.addEventListener("submit", async (evento) => {
  evento.preventDefault();
  const tipos = [...formulario.querySelectorAll('input[name="tipos"]:checked')].map((c) => c.value);

  const resposta = await fetch("/api/senhas/gerar", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ tamanho: formulario.tamanho.value, tipos }),
  });
  const dados = await resposta.json();

  if (!resposta.ok) {
    elResultado.hidden = true;
    mostrarMensagem(dados.erro, "erro");
    return;
  }

  elSenha.textContent = dados.senha;
  elResultado.hidden = false;
  botaoCopiar.textContent = "Copiar";
  mostrarMensagem("Senha gerada!", "ok");
});

botaoCopiar.addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(elSenha.textContent);
    botaoCopiar.textContent = "Copiado!";
  } catch {
    mostrarMensagem("Não foi possível copiar. Selecione a senha e copie manualmente.", "erro");
  }
});
