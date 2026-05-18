<template>
  <div class="movimentacoes-container">
    <div class="header">
      <h1>📦 Movimentações</h1>
      <div class="header-buttons">
        <button @click="imprimirRelatorio()" class="btn-secondary">
          🖨️ Imprimir Relatório
        </button>
        <button @click="abrirModal()" class="btn-primary">
          + Nova Movimentação
        </button>
      </div>
    </div>

    <div v-if="erro" class="alert-error">{{ erro }}</div>

    <div v-if="loading" class="loading">Carregando...</div>

    <table v-else class="tabela">
      <thead>
        <tr>
          <th>Tipo</th>
          <th>Data</th>
          <th>Autor</th>
          <th>Itens</th>
          <th>Total</th>
          <th>Ações</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="mov in movimentacoes" :key="mov.id">
          <td>{{ mov.tipo_movimentacao }}</td>
          <td>{{ formatarData(mov.data_movimentacao) }}</td>
          <td>{{ mov.autor_nome || mov.autor }}</td>
          <td>{{ calcularQuantidadeItens(mov) }}</td>
          <td>{{ formatarPreco(calcularTotalMovimentacao(mov)) }}</td>
          <td class="acoes">
            <button @click="abrirModalDetalhes(mov)" class="btn-small btn-view">
              Ver
            </button>
            <button
              @click="imprimirMovimentacao(mov)"
              class="btn-small btn-print"
            >
              🖨️ Imprimir
            </button>
            <button
              @click="deletarMovimentacao(mov.id)"
              class="btn-small btn-delete"
            >
              ✕ Deletar
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-if="movimentacoes.length === 0 && !loading" class="vazio">
      Nenhuma movimentação encontrada
    </div>

    <!-- Modal -->
    <div v-if="modalAberto" class="modal-overlay-container">
      <div class="modal-backdrop" @click="fecharModal()"></div>
      <div class="modal-dialog">
        <div class="modal-header">
          <h2>
            {{ movEditando ? "Editar Movimentação" : "Nova Movimentação" }}
          </h2>
          <button type="button" @click="fecharModal()" class="btn-fechar">
            ✕
          </button>
        </div>

        <form @submit.prevent="salvarMovimentacao" class="formulario">
          <div class="form-group">
            <label>Tipo *</label>
            <select
              v-model="form.tipo_movimentacao"
              required
              :disabled="!!movEditando"
            >
              <option value="entrada">Entrada</option>
              <option value="venda">Venda</option>
              <option value="perda">Perda</option>
            </select>
          </div>

          <div class="form-section">
            <h3>Itens da Movimentação</h3>

            <div v-if="!movEditando" class="form-group">
              <label>Produto *</label>
              <select v-model="itemForm">
                <option value="">Selecione um produto</option>
                <option v-for="prod in produtos" :key="prod.id" :value="prod">
                  {{ prod.nome }}
                </option>
              </select>
            </div>

            <div v-if="!movEditando" class="form-row">
              <div class="form-group">
                <label>Quantidade *</label>
                <input
                  v-model="itemForm.quantidade"
                  type="number"
                  step="0.01"
                  placeholder="0"
                />
              </div>

              <div class="form-group">
                <label>Preço Unitário *</label>
                <label>{{
                  formatarPreco(
                    itemForm.id
                      ? getPrecoAtual(
                          produtos.find(
                            (p: Produto) => p.id === itemForm.id,
                          ) || {
                            id: 0,
                            nome: "",
                            preco_compra: 0,
                            preco_venda: 0,
                          },
                        )
                      : 0,
                  )
                }}</label>
              </div>

              <div class="form-group">
                <button
                  type="button"
                  @click="adicionarItem(itemForm)"
                  class="btn-secondary"
                >
                  Adicionar
                </button>
              </div>
            </div>

            <div v-if="itens.length > 0" class="itens-list">
              <table>
                <thead>
                  <tr>
                    <th>Produto</th>
                    <th>Quantidade</th>
                    <th>Preço Unit.</th>
                    <th>Total</th>
                    <th v-if="!movEditando">Ação</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(item, idx) in itens" :key="idx">
                    <td>
                      {{
                        produtos.find((p: Produto) => p.id === item.id)?.nome ||
                        "N/A"
                      }}
                    </td>
                    <td>{{ item.quantidade }}</td>
                    <td>{{ item.preco }}</td>
                    <td>
                      {{ formatarPreco(item.quantidade * item.preco) }}
                    </td>
                    <td v-if="!movEditando">
                      <button
                        type="button"
                        @click="removerItem(idx)"
                        class="btn-small btn-delete"
                      >
                        ✕
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div class="modal-footer">
            <button type="button" @click="fecharModal()" class="btn-secondary">
              {{ movEditando ? "Fechar" : "Cancelar" }}
            </button>
            <button
              v-if="!movEditando"
              type="submit"
              class="btn-primary"
              :disabled="salvando"
            >
              {{ salvando ? "Salvando..." : "Salvar" }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Div para imprimir (oculta) -->
    <div id="conteudo-impressao" style="display: none"></div>
  </div>
</template>

<script setup lang="ts">
import api from "~/composables/api";

definePageMeta({
  middleware: "auth",
});

interface Movimentacao {
  id: number;
  autor: number;
  autor_nome?: string;
  tipo_movimentacao: string;
  data_movimentacao: string;
  itens: {
    produto: number;
    quantidade: number;
  }[];
}

interface Produto {
  id: number;
  nome: string;
  preco_compra: number;
  preco_venda: number;
}

interface Item {
  id: number;
  nome: string;
  quantidade: number;
  preco: number;
}

const movimentacoes = ref<Movimentacao[]>([]);
const itens = ref<Item[]>([]);
const produtos = ref<Produto[]>([]);
const loading = ref(false);
const salvando = ref(false);
const modalAberto = ref(false);
const movEditando = ref<Movimentacao | null>(null);
const erro = ref("");

const form = ref({
  tipo_movimentacao: "entrada",
});

const itemForm = ref({
  id: "" as any,
  nome: "" as any,
  quantidade: "" as any,
  preco: "" as any,
});

const formatarData = (data: string | undefined) => {
  if (!data) return "-";
  return new Date(data).toLocaleDateString("pt-BR", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
};

const formatarPreco = (preco: string | number) => {
  return new Intl.NumberFormat("AOA", {
    style: "currency",
    currency: "AOA",
  }).format(Number(preco));
};

const getPrecoAtual = (produto: Produto): number => {
  const tipoMovimentacao = form.value.tipo_movimentacao;
  if (tipoMovimentacao === "venda") {
    return produto.preco_venda;
  } else if (tipoMovimentacao === "entrada" || tipoMovimentacao === "perda") {
    return produto.preco_compra;
  }
  return 0;
};

const calcularQuantidadeItens = (mov: Movimentacao): number => {
  if (!mov.itens) return 0;
  return mov.itens.reduce((total, item) => total + item.quantidade, 0);
};

const calcularTotalMovimentacao = (mov: Movimentacao): number => {
  if (!mov.itens) return 0;
  return mov.itens.reduce((total, item) => {
    const produto = produtos.value.find((p) => p.id === item.produto);
    let preco = 0;
    if (produto) {
      if (mov.tipo_movimentacao === "venda") {
        preco = produto.preco_venda;
      } else if (
        mov.tipo_movimentacao === "entrada" ||
        mov.tipo_movimentacao === "perda"
      ) {
        preco = produto.preco_compra;
      }
    }
    return total + item.quantidade * preco;
  }, 0);
};

const carregarDados = async () => {
  loading.value = true;
  erro.value = "";
  try {
    const [movRes, prodRes] = await Promise.all([
      api.get("/movimentacoes/").catch((err) => {
        console.error("Erro ao carregar movimentações:", err);
        return { data: [] };
      }),
      api.get("/produtos/").catch((err) => {
        console.error("Erro ao carregar produtos:", err);
        return { data: [] };
      }),
    ]);

    movimentacoes.value = Array.isArray(movRes.data)
      ? movRes.data
      : movRes.data.results || [];
    console.log("Movimentações carregadas:", movimentacoes.value);
    produtos.value = Array.isArray(prodRes.data)
      ? prodRes.data
      : prodRes.data.results || [];
  } catch (error: any) {
    console.error("Erro geral:", error);
    erro.value = "Erro ao carregar dados";
  } finally {
    loading.value = false;
  }
};

const abrirModal = (mov: Movimentacao | null = null) => {
  if (mov) {
    movEditando.value = mov;
    form.value = {
      tipo_movimentacao: mov.tipo_movimentacao,
    };
  } else {
    movEditando.value = null;
    form.value = {
      tipo_movimentacao: "entrada",
    };
  }
  itens.value = [];
  itemForm.value = {
    id: "",
    nome: "",
    quantidade: "",
    preco: "",
  };
  modalAberto.value = true;
};

const fecharModal = () => {
  modalAberto.value = false;
  movEditando.value = null;
};

const abrirModalDetalhes = (mov: Movimentacao) => {
  movEditando.value = mov;
  if (mov.itens && mov.itens.length > 0) {
    itens.value = mov.itens.map((item) => {
      const produto = produtos.value.find((p) => p.id === item.produto);
      let preco = 0;
      if (produto) {
        if (mov.tipo_movimentacao === "venda") {
          preco = produto.preco_venda;
        } else if (
          mov.tipo_movimentacao === "entrada" ||
          mov.tipo_movimentacao === "perda"
        ) {
          preco = produto.preco_compra;
        }
      }
      return {
        id: item.produto,
        nome: produto?.nome || "N/A",
        quantidade: item.quantidade,
        preco: preco,
      };
    });
  }
  form.value = {
    tipo_movimentacao: mov.tipo_movimentacao,
  };
  modalAberto.value = true;
};

const adicionarItem = (form: any) => {
  if (form.id && form.nome && form.quantidade) {
    const produto = produtos.value.find((p) => p.id === form.id);
    const preco = produto ? getPrecoAtual(produto) : 0;
    itens.value.push({
      id: parseInt(form.id),
      nome: form.nome,
      quantidade: parseInt(form.quantidade),
      preco: preco,
    });
    itemForm.value = { id: "", nome: "", quantidade: "", preco: "" };
  }
};

const removerItem = (index: number) => {
  itens.value.splice(index, 1);
};

const salvarMovimentacao = async () => {
  if (itens.value.length === 0) {
    erro.value = "Adicione pelo menos um item";
    return;
  }

  salvando.value = true;
  erro.value = "";
  try {
    console.log("form.value:", form.value);
    console.log("form.value.tipo_movimentacao:", form.value.tipo_movimentacao);
    const payload = {
      tipo_movimentacao: form.value.tipo_movimentacao,
      itens: itens.value.map((item) => ({
        produto: item.id,
        quantidade: item.quantidade,
      })),
    };
    console.log("Payload completo enviado:", JSON.stringify(payload, null, 2));
    await api.post("/movimentacoes/", payload);

    fecharModal();
    await carregarDados();
  } catch (error: any) {
    console.error("Erro completo:", error);
    console.error("Response data:", error.response?.data);
    console.error("Response data estoque:", error.response?.data?.estoque);
    erro.value =
      error.response?.data?.detail ||
      JSON.stringify(error.response?.data) ||
      "Erro ao salvar movimentação";
  } finally {
    salvando.value = false;
  }
};

const deletarMovimentacao = async (id: number) => {
  if (!confirm("Tem certeza que deseja deletar esta movimentação?")) return;

  try {
    await api.delete(`/movimentacoes/${id}/`);
    await carregarDados();
  } catch (error: any) {
    erro.value = "Erro ao deletar movimentação";
  }
};

const imprimirMovimentacao = (mov: Movimentacao) => {
  const conteudoImpressao = document.getElementById("conteudo-impressao");
  if (!conteudoImpressao) return;

  let conteudo = `
    <html>
      <head>
        <title>Movimentação #${mov.id}</title>
        <style>
          body { font-family: Arial, sans-serif; margin: 20px; }
          h1 { color: #333; }
          table { width: 100%; border-collapse: collapse; margin-top: 20px; }
          th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
          th { background-color: #1f2937; color: white; }
          .info { margin: 20px 0; }
          .total { font-weight: bold; font-size: 1.2em; margin-top: 20px; }
        </style>
      </head>
      <body>
        <h1>Movimentação #${mov.id}</h1>
        <div class="info">
          <p><strong>Tipo:</strong> ${mov.tipo_movimentacao}</p>
          <p><strong>Data:</strong> ${formatarData(mov.data_movimentacao)}</p>
          <p><strong>Autor:</strong> ${mov.autor_nome || mov.autor}</p>
        </div>
        <table>
          <thead>
            <tr>
              <th>Produto</th>
              <th>Quantidade</th>
              <th>Preço Unitário</th>
              <th>Total</th>
            </tr>
          </thead>
          <tbody>
            ${mov.itens
              .map((item) => {
                const produto = produtos.value.find(
                  (p) => p.id === item.produto,
                );
                let preco = 0;
                if (produto) {
                  if (mov.tipo_movimentacao === "venda") {
                    preco = produto.preco_venda || 0;
                  } else if (
                    mov.tipo_movimentacao === "entrada" ||
                    mov.tipo_movimentacao === "perda"
                  ) {
                    preco = produto.preco_compra || 0;
                  }
                }
                preco = Number(preco) || 0;
                const total = item.quantidade * preco;
                return `
              <tr>
                <td>${produto?.nome || "N/A"}</td>
                <td>${item.quantidade}</td>
                <td>Kz ${preco.toFixed(2)}</td>
                <td>Kz ${total.toFixed(2)}</td>
              </tr>
            `;
              })
              .join("")}
          </tbody>
        </table>
        <div class="total">
          <p>Total: Kz ${calcularTotalMovimentacao(mov).toFixed(2)}</p>
        </div>
      </body>
    </html>
  `;

  conteudoImpressao.innerHTML = conteudo;
  const janelaImpressao = window.open("", "", "height=600,width=800");
  if (janelaImpressao) {
    janelaImpressao.document.write(conteudo);
    janelaImpressao.document.close();
    janelaImpressao.print();
  }
};

const imprimirRelatorio = () => {
  const movPorTipo = {
    entrada: movimentacoes.value.filter(
      (m) => m.tipo_movimentacao === "entrada",
    ),
    venda: movimentacoes.value.filter((m) => m.tipo_movimentacao === "venda"),
    perda: movimentacoes.value.filter((m) => m.tipo_movimentacao === "perda"),
  };

  const totalPorTipo = {
    entrada: movPorTipo.entrada.reduce(
      (total, mov) => total + calcularTotalMovimentacao(mov),
      0,
    ),
    venda: movPorTipo.venda.reduce(
      (total, mov) => total + calcularTotalMovimentacao(mov),
      0,
    ),
    perda: movPorTipo.perda.reduce(
      (total, mov) => total + calcularTotalMovimentacao(mov),
      0,
    ),
  };

  let conteudo = `
    <html>
      <head>
        <title>Relatório de Movimentações</title>
        <style>
          body { font-family: Arial, sans-serif; margin: 20px; }
          h1 { color: #333; }
          h2 { color: #555; margin-top: 30px; border-bottom: 2px solid #1f2937; padding-bottom: 10px; }
          table { width: 100%; border-collapse: collapse; margin-top: 15px; }
          th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
          th { background-color: #1f2937; color: white; }
          .resumo { margin: 20px 0; padding: 10px; background-color: #f0f0f0; border-radius: 5px; }
          .subtotal { background-color: #e8f4f8; font-weight: bold; }
        </style>
      </head>
      <body>
        <h1>Relatório Geral de Movimentações</h1>
        <div class="resumo">
          <p><strong>Data do Relatório:</strong> ${new Date().toLocaleDateString("pt-BR", { year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit" })}</p>
          <p><strong>Total de Movimentações:</strong> ${movimentacoes.value.length}</p>
        </div>

        ${
          movPorTipo.entrada.length > 0
            ? `
          <h2>📥 Movimentações de Entrada</h2>
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Data</th>
                <th>Autor</th>
                <th>Quantidade de Itens</th>
                <th>Total</th>
              </tr>
            </thead>
            <tbody>
              ${movPorTipo.entrada
                .map(
                  (mov) => `
              <tr>
                <td>${mov.id}</td>
                <td>${formatarData(mov.data_movimentacao)}</td>
                <td>${mov.autor_nome || mov.autor}</td>
                <td>${calcularQuantidadeItens(mov)}</td>
                <td>Kz ${calcularTotalMovimentacao(mov).toFixed(2)}</td>
              </tr>
            `,
                )
                .join("")}
              <tr class="subtotal">
                <td colspan="4">Valor investido:</td>
                <td>Kz ${totalPorTipo.entrada.toFixed(2)}</td>
              </tr>
            </tbody>
          </table>
        `
            : ""
        }

        ${
          movPorTipo.venda.length > 0
            ? `
          <h2>🛍️ Movimentações de Venda</h2>
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Data</th>
                <th>Autor</th>
                <th>Quantidade de Itens</th>
                <th>Total</th>
              </tr>
            </thead>
            <tbody>
              ${movPorTipo.venda
                .map(
                  (mov) => `
              <tr>
                <td>${mov.id}</td>
                <td>${formatarData(mov.data_movimentacao)}</td>
                <td>${mov.autor_nome || mov.autor}</td>
                <td>${calcularQuantidadeItens(mov)}</td>
                <td>Kz ${calcularTotalMovimentacao(mov).toFixed(2)}</td>
              </tr>
            `,
                )
                .join("")}
              <tr class="subtotal">
                <td colspan="4">Valor vendido:</td>
                <td>Kz ${totalPorTipo.venda.toFixed(2)}</td>
              </tr>
            </tbody>
          </table>
        `
            : ""
        }

        ${
          movPorTipo.perda.length > 0
            ? `
          <h2>⚠️ Movimentações de Perda</h2>
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Data</th>
                <th>Autor</th>
                <th>Quantidade de Itens</th>
                <th>Total</th>
              </tr>
            </thead>
            <tbody>
              ${movPorTipo.perda
                .map(
                  (mov) => `
              <tr>
                <td>${mov.id}</td>
                <td>${formatarData(mov.data_movimentacao)}</td>
                <td>${mov.autor_nome || mov.autor}</td>
                <td>${calcularQuantidadeItens(mov)}</td>
                <td>Kz ${calcularTotalMovimentacao(mov).toFixed(2)}</td>
              </tr>
            `,
                )
                .join("")}
              <tr class="subtotal">
                <td colspan="4">Subtotal Perdas:</td>
                <td>Kz ${totalPorTipo.perda.toFixed(2)}</td>
              </tr>
            </tbody>
          </table>
        `
            : ""
        }
      </body>
    </html>
  `;

  const janelaImpressao = window.open("", "", "height=600,width=800");
  if (janelaImpressao) {
    janelaImpressao.document.write(conteudo);
    janelaImpressao.document.close();
    janelaImpressao.print();
  }
};

onMounted(() => {
  carregarDados();
});
</script>

<style scoped>
.movimentacoes-container {
  padding: 2rem;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.header h1 {
  margin: 0;
  font-size: 1.5rem;
}

.header-buttons {
  display: flex;
  gap: 1rem;
}

.alert-error {
  background: #fee2e2;
  color: #dc2626;
  padding: 1rem;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
  border-left: 4px solid #dc2626;
}

.btn-primary {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 0.5rem 1.5rem;
  border-radius: 0.5rem;
  cursor: pointer;
  font-weight: 600;
}

.btn-primary:hover {
  background: #2563eb;
}

.btn-primary:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

.btn-secondary {
  background: #6b7280;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
}

.btn-secondary:hover {
  background: #4b5563;
}

.btn-small {
  padding: 0.25rem 0.75rem;
  font-size: 0.875rem;
  border: none;
  border-radius: 0.25rem;
  cursor: pointer;
}

.btn-edit {
  background: #10b981;
  color: white;
}

.btn-edit:hover {
  background: #059669;
}

.btn-delete {
  background: #ef4444;
  color: white;
}

.btn-delete:hover {
  background: #dc2626;
}

.btn-view {
  background: #3b82f6;
  color: white;
}

.btn-view:hover {
  background: #2563eb;
}

.btn-print {
  background: #8b5cf6;
  color: white;
}

.btn-print:hover {
  background: #7c3aed;
}

.tabela {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 2rem;
}

.tabela thead {
  background: #1f2937;
  color: white;
}

.tabela th {
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  border-bottom: 2px solid #e5e7eb;
}

.tabela td {
  padding: 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.acoes {
  display: flex;
  gap: 0.5rem;
}

.badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 600;
}

.badge.entrada {
  background: #d1fae5;
  color: #065f46;
}

.badge.venda {
  background: #fef3c7;
  color: #92400e;
}

.badge.perda {
  background: #fee2e2;
  color: #991b1b;
}

.badge-entrada {
  background: #d1fae5;
  color: #065f46;
}

.badge-saida {
  background: #fee2e2;
  color: #991b1b;
}

.vazio {
  text-align: center;
  padding: 2rem;
  color: #6b7280;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #6b7280;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-overlay-container {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: auto;
}

.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 9998;
}

.modal-dialog {
  position: relative;
  z-index: 9999;
  background: white;
  border-radius: 0.5rem;
  max-width: 600px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

.modal {
  background: white;
  border-radius: 0.5rem;
  max-width: 600px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  position: sticky;
  top: 0;
  background: white;
  z-index: 10;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.25rem;
}

.btn-fechar {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6b7280;
}

.btn-fechar:hover {
  color: #000;
}

.formulario {
  padding: 1.5rem;
  color: black;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #374151;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 0.25rem;
  font-size: 1rem;
  box-sizing: border-box;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.textarea {
  resize: vertical;
  min-height: 100px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr auto;
  gap: 1rem;
}

.form-row .form-group {
  margin-bottom: 0;
}

.form-row .form-group:last-child {
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}

.form-section {
  background: #f9fafb;
  padding: 1.5rem;
  border-radius: 0.5rem;
  margin: 1.5rem 0;
}

.form-section h3 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: #374151;
}

.itens-list {
  margin-top: 1rem;
  overflow-x: auto;
}

.itens-list table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.875rem;
}

.itens-list th {
  background: #e5e7eb;
  padding: 0.5rem;
  text-align: left;
  font-weight: 600;
  border: 1px solid #d1d5db;
}

.itens-list td {
  padding: 0.5rem;
  border: 1px solid #d1d5db;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1.5rem;
  border-top: 1px solid #e5e7eb;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.checkbox-label input {
  width: auto;
}
</style>
