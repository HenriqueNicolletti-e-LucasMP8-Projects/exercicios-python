const elForm = document.getElementById("form-conversor");
const elTipo = document.getElementById("tipo");
const elValor = document.getElementById("valor");
const elResultado = document.getElementById("resultado");
const elMensagem = document.getElementById("mensagem");

function mostrar(resultado, erro) {
  elResultado.textContent = resultado || "";
  elMensagem.textContent = erro || "";
}

async function converter(evento) {
  evento.preventDefault();
  const resposta = await fetch("/api/conversor", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ tipo: elTipo.value, valor: elValor.value }),
  });
  const dados = await resposta.json();
  if (resposta.ok) {
    mostrar(dados.texto, "");
  } else {
    mostrar("", dados.erro);
    elValor.focus();
  }
}

elForm.addEventListener("submit", converter);
elTipo.addEventListener("change", () => {
  if (elValor.value.trim()) elForm.requestSubmit();
});
