const elForm = document.getElementById("form-conversor");
const elTipo = document.getElementById("tipo");
const elValor = document.getElementById("valor");
const elResultado = document.getElementById("resultado");
const elMensagem = document.getElementById("mensagem");
const elInverter = document.getElementById("inverter");
const elHistorico = document.getElementById("historico");
const elListaHistorico = document.getElementById("lista-historico");
const elLimparHistorico = document.getElementById("limpar-historico");

const CHAVE_HISTORICO = "historico_conversor";
const MAX_HISTORICO = 5;

let ultimoResultado = null;

function lerHistorico() {
  try {
    const lista = JSON.parse(localStorage.getItem(CHAVE_HISTORICO));
    return Array.isArray(lista) ? lista.filter((item) => typeof item === "string") : [];
  } catch {
    return [];
  }
}

function salvarHistorico(lista) {
  try {
    localStorage.setItem(CHAVE_HISTORICO, JSON.stringify(lista));
  } catch {
    // sem armazenamento: o histórico vale só até recarregar a página
  }
}

let historico = lerHistorico();

function mostrarHistorico() {
  elListaHistorico.replaceChildren(
    ...historico.map((texto) => {
      const item = document.createElement("li");
      item.textContent = texto;
      return item;
    }),
  );
  elHistorico.hidden = historico.length === 0;
}

function registrarNoHistorico(texto) {
  if (historico[0] === texto) return;
  historico = [texto, ...historico].slice(0, MAX_HISTORICO);
  salvarHistorico(historico);
  mostrarHistorico();
}

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
    ultimoResultado = dados.resultado;
    mostrar(dados.texto, "");
    registrarNoHistorico(dados.texto);
  } else {
    ultimoResultado = null;
    mostrar("", dados.erro);
    elValor.focus();
  }
}

function inverter() {
  const inverso = elTipo.selectedOptions[0].dataset.inverso;
  elTipo.value = inverso;
  // Com um resultado na tela, ele vira o novo valor; sem resultado, mantém o que foi digitado.
  if (ultimoResultado !== null) elValor.value = String(ultimoResultado).replace(".", ",");
  if (elValor.value.trim()) elForm.requestSubmit();
}

elForm.addEventListener("submit", converter);
elTipo.addEventListener("change", () => {
  if (elValor.value.trim()) elForm.requestSubmit();
});
elInverter.addEventListener("click", inverter);
elLimparHistorico.addEventListener("click", () => {
  historico = [];
  salvarHistorico(historico);
  mostrarHistorico();
});

mostrarHistorico();
