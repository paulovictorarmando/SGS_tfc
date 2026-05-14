<template>
  <div class="produtos-container">
    <div class="header">
      <h1>📦 Produtos</h1>
      <button @click="abrirModal()" class="btn-primary">+ Novo Produto</button>
    </div>

    <div v-if="erro" class="alert-error">{{ erro }}</div>

    <div v-if="loading" class="loading">Carregando...</div>

    <table v-else class="tabela">
      <thead>
        <tr>
          <th>Nome</th>
          <th>Preço</th>
          <th>Categoria</th>
          <th>Ações</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="produto in produtos" :key="produto.id">
          <td>{{ produto.nome }}</td>
          <td>{{ formatarPreco(produto.preco) }}</td>
          <td>{{ produto.categoria.nome }}</td>
          <td class="acoes">
            <button @click="abrirModal(produto)" class="btn-small btn-edit">
              Editar
            </button>
            <button
              @click="deletarProduto(produto.id)"
              class="btn-small btn-delete"
            >
              Deletar
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-if="produtos.length === 0 && !loading" class="vazio">
      Nenhum produto encontrado
    </div>

    <!-- Modal -->
    <div v-if="modalAberto" class="modal-overlay-container">
      <div class="modal-backdrop" @click="fecharModal()"></div>
      <div class="modal-dialog">
        <div class="modal-header">
          <h2>{{ produtoEditando ? "Editar Produto" : "Novo Produto" }}</h2>
          <button type="button" @click="fecharModal()" class="btn-fechar">
            ✕
          </button>
        </div>

        <form @submit.prevent="salvarProduto" class="formulario">
          <div class="form-group">
            <label>Nome *</label>
            <input v-model="form.nome" type="text" required maxlength="100" />
          </div>

          <div class="form-group">
            <label>Categoria *</label>
            <select v-model="form.categoria" required>
              <option value="">Selecione uma categoria</option>
              <option v-for="cat in categorias" :key="cat.id" :value="cat.id">
                {{ cat.nome }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label>Preço *</label>
            <input
              v-model="form.preco"
              type="number"
              step="0.01"
              required
              placeholder="0.00"
            />
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

interface Produto {
  id: number;
  nome: string;
  preco: number;
  categoria: number;
  categoria_nome?: string;
}

interface Categoria {
  id: number;
  nome: string;
}

const produtos = ref<Produto[]>([]);
const categorias = ref<Categoria[]>([]);
const loading = ref(false);
const salvando = ref(false);
const modalAberto = ref(false);
const produtoEditando = ref<Produto | null>(null);
const erro = ref("");

const form = ref({
  nome: "",
  categoria: "",
  preco: "",
});

const formatarPreco = (preco: string | number) => {
  return new Intl.NumberFormat("pt-ao", {
    style: "currency",
    currency: "AOA",
  }).format(Number(preco));
};

const carregarDados = async () => {
  loading.value = true;
  erro.value = "";
  try {
    const [produtosRes, categoriasRes] = await Promise.all([
      api.get("/produtos/").catch((err) => {
        console.error("Erro ao carregar produtos:", err);
        return { data: [] };
      }),
      api.get("/categorias/").catch((err) => {
        console.error("Erro ao carregar categorias:", err);
        return { data: [] };
      }),
    ]);
    produtos.value = Array.isArray(produtosRes.data)
      ? produtosRes.data
      : produtosRes.data.results || [];
    categorias.value = Array.isArray(categoriasRes.data)
      ? categoriasRes.data
      : categoriasRes.data.results || [];
  } catch (error: any) {
    console.error("Erro geral:", error);
    erro.value = "Erro ao carregar dados";
  } finally {
    loading.value = false;
  }
};

const abrirModal = (produto: any = null) => {
  if (produto) {
    produtoEditando.value = produto;
    form.value = {
      nome: produto.nome,
      categoria: produto.categoria,
      preco: produto.preco,
    };
  } else {
    produtoEditando.value = null;
    form.value = {
      nome: "",
      categoria: "",
      preco: "",
    };
  }
  modalAberto.value = true;
};

const fecharModal = () => {
  modalAberto.value = false;
  produtoEditando.value = null;
};

const salvarProduto = async () => {
  salvando.value = true;
  erro.value = "";
  try {
    const dados = {
      nome: form.value.nome,
      categoria_id: parseInt(form.value.categoria),
      preco: parseFloat(form.value.preco),
    };

    if (produtoEditando.value) {
      await api.put(`/produtos/${produtoEditando.value.id}/`, dados);
    } else {
      await api.post("/produtos/", dados);
    }

    fecharModal();
    await carregarDados();
  } catch (error: any) {
    erro.value = error.response?.data?.detail || "Erro ao salvar produto";
  } finally {
    salvando.value = false;
  }
};

const deletarProduto = async (id: number) => {
  if (!confirm("Tem certeza que deseja deletar este produto?")) return;

  try {
    await api.delete(`/produtos/${id}/`);
    await carregarDados();
  } catch (error: any) {
    erro.value = "Erro ao deletar produto";
  }
};

onMounted(() => {
  carregarDados();
});
</script>

<style scoped>
.produtos-container {
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

.acoes {
  display: flex;
  gap: 0.5rem;
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
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
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

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1.5rem;
  border-top: 1px solid #e5e7eb;
}
</style>
