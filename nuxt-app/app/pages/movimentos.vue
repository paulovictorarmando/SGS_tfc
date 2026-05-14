<template>
  <div class="movimentacoes-container">
    <div class="header">
      <h1>📦 Movimentações</h1>
      <button @click="abrirModal()" class="btn-primary">
        + Nova Movimentação
      </button>
    </div>

    <div v-if="erro" class="alert-error">{{ erro }}</div>

    <div v-if="loading" class="loading">Carregando...</div>

    <table v-else class="tabela">
      <thead>
        <tr>
          <th>Tipo</th>
          <th>Descrição</th>
          <th>Data</th>
          <th>Ações</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="mov in movimentacoes" :key="mov.id">
          <td>
            <span
              :class="[
                'badge',
                mov.tipo === 'entrada' ? 'badge-entrada' : 'badge-saida',
              ]"
            >
              {{ mov.tipo === "entrada" ? "📥" : "📤" }} {{ mov.tipo }}
            </span>
          </td>
          <td>{{ mov.descricao }}</td>
          <td>{{ formatarData(mov.data) }}</td>
          <td class="acoes">
            <button @click="abrirModal(mov)" class="btn-small btn-edit">
              Editar
            </button>
            <button
              @click="deletarMovimentacao(mov.id)"
              class="btn-small btn-delete"
            >
              Deletar
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
            <select v-model="form.tipo" required>
              <option value="entrada">📥 Entrada</option>
              <option value="saida">📤 Saída</option>
            </select>
          </div>

          <div class="form-group">
            <label>Data *</label>
            <input v-model="form.data" type="date" required />
          </div>

          <div class="form-group">
            <label>Descrição</label>
            <textarea v-model="form.descricao" class="textarea"></textarea>
          </div>

          <div class="form-section">
            <h3>Itens da Movimentação</h3>

            <div class="form-group">
              <label>Produto *</label>
              <select v-model="itemForm.produto">
                <option value="">Selecione um produto</option>
                <option
                  v-for="prod in produtos"
                  :key="prod.id"
                  :value="prod.id"
                >
                  {{ prod.nome }}
                </option>
              </select>
            </div>

            <div class="form-row">
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
                <input
                  v-model="itemForm.preco_unitario"
                  type="number"
                  step="0.01"
                  placeholder="0.00"
                />
              </div>

              <div class="form-group">
                <button
                  type="button"
                  @click="adicionarItem"
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
                    <th>Ação</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(item, idx) in itens" :key="idx">
                    <td>
                      {{
                        produtos.find((p: Produto) => p.id === item.produto)
                          ?.nome || "N/A"
                      }}
                    </td>
                    <td>{{ item.quantidade }}</td>
                    <td>{{ formatarPreco(item.preco_unitario) }}</td>
                    <td>
                      {{ formatarPreco(item.quantidade * item.preco_unitario) }}
                    </td>
                    <td>
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
              Cancelar
            </button>
            <button type="submit" class="btn-primary" :disabled="salvando">
              {{ salvando ? "Salvando..." : "Salvar" }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import api from "~/composables/api";

definePageMeta({
  middleware: "auth",
});

interface Movimentacao {
  id: number;
  tipo: string;
  descricao: string;
  data: string;
}

interface Produto {
  id: number;
  nome: string;
}

interface Item {
  produto: number;
  quantidade: number;
  preco_unitario: number;
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
  tipo: "entrada",
  descricao: "",
  data: new Date().toISOString().split("T")[0],
});

const itemForm = ref({
  produto: "" as any,
  quantidade: "" as any,
  preco_unitario: "" as any,
});

const formatarData = (data: string) => {
  return new Date(data).toLocaleDateString("pt-BR");
};

const formatarPreco = (preco: string | number) => {
  return new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(Number(preco));
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
      tipo: mov.tipo,
      descricao: mov.descricao,
      data: mov.data,
    };
  } else {
    movEditando.value = null;
    form.value = {
      tipo: "entrada",
      descricao: "",
      data: new Date().toISOString().split("T")[0],
    };
  }
  itens.value = [];
  itemForm.value = {
    produto: "",
    quantidade: "",
    preco_unitario: "",
  };
  modalAberto.value = true;
};

const fecharModal = () => {
  modalAberto.value = false;
  movEditando.value = null;
};

const adicionarItem = () => {
  if (
    itemForm.value.produto &&
    itemForm.value.quantidade &&
    itemForm.value.preco_unitario
  ) {
    itens.value.push({
      produto: parseInt(itemForm.value.produto),
      quantidade: parseFloat(itemForm.value.quantidade),
      preco_unitario: parseFloat(itemForm.value.preco_unitario),
    });
    itemForm.value = { produto: "", quantidade: "", preco_unitario: "" };
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
    if (movEditando.value) {
      await api.put(`/movimentacoes/${movEditando.value.id}/`, form.value);
    } else {
      const mov = await api.post("/movimentacoes/", form.value);

      for (const item of itens.value) {
        await api.post("/itens-movimentacao/", {
          movimentacao: mov.data.id,
          ...item,
        });
      }
    }

    fecharModal();
    await carregarDados();
  } catch (error: any) {
    erro.value = error.response?.data?.detail || "Erro ao salvar movimentação";
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

.tabela tbody tr:hover {
  background: #f9fafb;
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
  color:black;
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
