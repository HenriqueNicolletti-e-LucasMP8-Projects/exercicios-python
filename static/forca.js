const LETRAS = "abcdefghijklmnopqrstuvwxyz".split("");

const elPalavra = document.getElementById("palavra");
const elDica = document.getElementById("dica");
const elPlacar = document.getElementById("placar");
const elDificuldade = document.getElementById("dificuldade");
const elErros = document.getElementById("erros");
const elMensagem = document.getElementById("mensagem");
const elTeclado = document.getElementById("teclado");
const partes = document.querySelectorAll("#boneco .partes > *");

const botoes = {};
let jogoAcabou = false;

function montarTeclado() {
  for (const letra of LETRAS) {
    const botao = document.createElement("button");
    botao.type = "button";
    botao.textContent = letra.toUpperCase();
    botao.addEventListener("click", () => tentarLetra(letra));
    elTeclado.appendChild(botao);
    botoes[letra] = botao;
  }
}

function mostrarMensagem(texto, classe) {
  elMensagem.textContent = texto;
  elMensagem.className = "mensagem " + (classe || "");
}

function atualizarTela(estado) {
  jogoAcabou = estado.situacao !== "jogando";

  elPalavra.textContent = estado.exibicao;
  elDica.textContent = estado.categoria ? `Dica: ${estado.categoria} (${estado.exibicao.split(" ").length} letras)` : "";
  elDificuldade.value = estado.dificuldade;
  elPlacar.textContent = `Vitórias: ${estado.placar.vitorias}   Derrotas: ${estado.placar.derrotas}`;
  elErros.textContent =
    `Erros: ${estado.erros}/${estado.max_erros}   Letras erradas: ` +
    estado.letras_erradas.map((l) => l.toUpperCase()).join(" ");

  partes.forEach((parte, i) => parte.classList.toggle("visivel", i < estado.erros));

  for (const letra of LETRAS) {
    const botao = botoes[letra];
    const certa = estado.letras_certas.includes(letra);
    const errada = estado.letras_erradas.includes(letra);
    botao.disabled = certa || errada || jogoAcabou;
    botao.classList.toggle("certa", certa);
    botao.classList.toggle("errada", errada);
  }

  if (estado.situacao === "venceu") {
    mostrarMensagem("Parabéns, você venceu!", "ok");
  } else if (estado.situacao === "perdeu") {
    mostrarMensagem(`Você perdeu! A palavra era: ${estado.palavra}`, "erro");
  }
}

async function chamarApi(url, opcoes) {
  const resposta = await fetch(url, opcoes);
  return { ok: resposta.ok, dados: await resposta.json() };
}

async function tentarLetra(letra) {
  if (jogoAcabou || botoes[letra].disabled) return;
  const { ok, dados } = await chamarApi("/api/forca/letra", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ letra }),
  });
  atualizarTela(dados);
  if (!ok) {
    mostrarMensagem(dados.erro, "erro");
  } else if (dados.situacao === "jogando") {
    const acertou = dados.letras_certas.includes(letra);
    mostrarMensagem(acertou ? "Acertou!" : "Letra errada!", acertou ? "ok" : "erro");
  }
}

async function novoJogo() {
  const { ok, dados } = await chamarApi("/api/forca/novo", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ dificuldade: elDificuldade.value }),
  });
  if (!ok) {
    mostrarMensagem(dados.erro, "erro");
    return;
  }
  atualizarTela(dados);
  mostrarMensagem("Escolha uma letra");
}

async function carregar() {
  const { dados } = await chamarApi("/api/forca");
  atualizarTela(dados);
  if (dados.situacao === "jogando") mostrarMensagem("Escolha uma letra");
}

document.addEventListener("keydown", (evento) => {
  if (evento.ctrlKey || evento.metaKey || evento.altKey) return;
  const letra = evento.key.toLowerCase();
  if (letra in botoes) tentarLetra(letra);
});
document.getElementById("novo-jogo").addEventListener("click", novoJogo);
elDificuldade.addEventListener("change", novoJogo);

montarTeclado();
carregar();
