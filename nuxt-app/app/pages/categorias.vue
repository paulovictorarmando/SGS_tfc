<template>
  <div class="categorias-container">
    <div class="header">
      <h1>🏷️ Categorias</h1>
      <button @click="abrirModal()" class="btn-primary">
        + Nova Categoria
      </button>
    </div>

    <div v-if="erro" class="alert-error">{{ erro }}</div>

    <div v-if="loading" class="loading">Carregando...</div>

    <table v-else class="tabela">
      <thead>
        <tr>
          <th>Nome</th>
          <th>Descrição</th>
          <th>Ações</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="categoria in categorias" :key="categoria.id">
          <td>{{ categoria.nome }}</td>
          <td>{{ categoria.descricao }}</td>
          <td class="acoes">
            <button @click="abrirModal(categoria)" class="btn-small btn-edit">
              Editar
            </button>
            <button
              @click="deletarCategoria(categoria.id)"
              class="btn-small btn-delete"
            >
              Deletar
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-if="categorias.length === 0 && !loading" class="vazio">
      Nenhuma categoria encontrada
    </div>

    <!-- Modal -->
    <div v-if="modalAberto" class="modal-overlay-container">
      <div class="modal-backdrop" @click="fecharModal()"></div>
      <div class="modal-dialog">
        <div class="modal-header">
          <h2>
            {{ categoriaEditando ? "Editar Categoria" : "Nova Categoria" }}
          </h2>
          <button type="button" @click="fecharModal()" class="btn-fechar">
            ✕
          </button>
        </div>

        <form @submit.prevent="salvarCategoria" class="formulario">
          <div class="form-group">
            <label>Nome *</label>
            <input v-model="form.nome" type="text" required maxlength="50" />
          </div>

          <div class="form-group">
            <label>Descrição *</label>
            <textarea v-model="form.descricao" required rows="4"></textarea>
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

interface Categoria {
  id: number
  nome: string
  descricao: string
}

const categorias = ref<Categoria[]>([]);
const loading = ref(false);
const salvando = ref(false);
const modalAberto = ref(false);
const categoriaEditando = ref<Categoria | null>(null);
const erro = ref("");

const form = ref({
  nome: "",
  descricao: "",
});

const carregarCategorias = async () => {
  loading.value = true;
  erro.value = "";
  try {
    const response = await api.get("/categorias/").catch((err) => {
      console.error("Erro ao carregar categorias:", err);
      return { data: [] };
    });
    categorias.value = Array.isArray(response.data)
      ? response.data
      : response.data.results || [];
  } catch (error: any) {
    console.error("Erro geral:", error);
    erro.value = "Erro ao carregar categorias";
  } finally {
    loading.value = false;
  }
};

const abrirModal = (categoria: Categoria | null = null) => {
  if (categoria) {
    categoriaEditando.value = categoria;
    form.value = {
      nome: categoria.nome,
      descricao: categoria.descricao,
    };
  } else {
    categoriaEditando.value = null;
    form.value = {
      nome: "",
      descricao: "",
    };
  }
  modalAberto.value = true;
};

const fecharModal = () => {
  modalAberto.value = false;
  categoriaEditando.value = null;
};

const salvarCategoria = async () => {
  salvando.value = true;
  erro.value = "";
  try {
    if (categoriaEditando.value) {
      await api.put(`/categorias/${categoriaEditando.value.id}/`, form.value);
    } else {
      await api.post("/categorias/", form.value);
    }

    fecharModal();
    await carregarCategorias();
  } catch (error: any) {
    erro.value = error.response?.data?.detail || "Erro ao salvar categoria";
  } finally {
    salvando.value = false;
  }
};

const deletarCategoria = async (id: number) => {
  if (!confirm("Tem certeza que deseja deletar esta categoria?")) return;

  try {
    await api.delete(`/categorias/${id}/`);
    await carregarCategorias();
  } catch (error: any) {
    erro.value = "Erro ao deletar categoria";
  }
};

onMounted(() => {
  carregarCategorias();
});
</script>

<style scoped>
.categorias-container {
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
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  cursor: pointer;
  font-weight: 500;
  transition: background 0.2s;
}

.btn-primary:hover {
  background: #2563eb;
}

.btn-primary:disabled {
  background: #9ca3af;
  cursor: not-allowed;
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

.tabela th,
.tabela td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
}

.acoes {
  display: flex;
  gap: 0.5rem;
}

.btn-small {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  font-size: 0.875rem;
  transition: all 0.2s;
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

.loading,
.vazio {
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

.modal {
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
  max-width: 500px;
  width: 90%;
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

.formulario {
  padding: 1.5rem;
  color: #000;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #374151;
}

.form-group input[type="text"],
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 1rem;
  font-family: inherit;
  box-sizing: border-box;
}

.form-group textarea {
  resize: vertical;
}

.modal-footer {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  padding: 1.5rem;
  border-top: 1px solid #e5e7eb;
}

.btn-secondary {
  background: #e5e7eb;
  color: #374151;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-secondary:hover {
  background: #d1d5db;
}
</style>
