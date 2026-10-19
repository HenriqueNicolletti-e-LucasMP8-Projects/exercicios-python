const formulario = document.getElementById("form-senha");
const elMensagem = document.getElementById("mensagem-senha");
const elLista = document.getElementById("lista-senhas");

const ROTULOS_FORCA = {
  fraca: "Fraca",
  media: "Média",
  forte: "Forte",
  muito_forte: "Muito forte",
};

function mostrarMensagem(texto, classe) {
  elMensagem.textContent = texto;
  elMensagem.className = "mensagem " + (classe || "");
}

function criarItem({ senha, forca }) {
  const item = document.createElement("li");
  item.className = "item-senha";

  const texto = document.createElement("output");
  texto.className = "senha";
  texto.textContent = senha;

  const medidor = document.createElement("span");
  medidor.className = `forca forca-${forca.nivel}`;
  medidor.textContent = `${ROTULOS_FORCA[forca.nivel]} (${forca.bits} bits)`;

  const botao = document.createElement("button");
  botao.type = "button";
  botao.textContent = "Copiar";
  botao.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(senha);
      botao.textContent = "Copiado!";
    } catch {
      mostrarMensagem("Não foi possível copiar. Selecione a senha e copie manualmente.", "erro");
    }
  });

  item.append(texto, medidor, botao);
  return item;
}

formulario.addEventListener("submit", async (evento) => {
  evento.preventDefault();
  const tipos = [...formulario.querySelectorAll('input[name="tipos"]:checked')].map((c) => c.value);

  const resposta = await fetch("/api/senhas/gerar", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      tamanho: formulario.tamanho.value,
      quantidade: formulario.quantidade.value,
      tipos,
      sem_parecidos: formulario.sem_parecidos.checked,
    }),
  });
  const dados = await resposta.json();

  if (!resposta.ok) {
    elLista.replaceChildren();
    mostrarMensagem(dados.erro, "erro");
    return;
  }

  elLista.replaceChildren(...dados.senhas.map(criarItem));
  mostrarMensagem(dados.senhas.length === 1 ? "Senha gerada!" : `${dados.senhas.length} senhas geradas!`, "ok");
});
