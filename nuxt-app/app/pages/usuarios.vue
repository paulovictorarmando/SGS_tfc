<template>
  <div class="usuarios-container">
    <div class="header">
      <h1>👥 Usuários</h1>
      <button @click="abrirModal()" class="btn-primary">+ Novo Usuário</button>
    </div>

    <div v-if="erro" class="alert-error">{{ erro }}</div>

    <div v-if="loading" class="loading">Carregando...</div>

    <table v-else class="tabela">
      <thead>
        <tr>
          <th>Username</th>
          <th>Email</th>
          <th>Nome</th>
          <th>Admin</th>
          <th>Ações</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="usuario in usuarios" :key="usuario.id">
          <td>{{ usuario.username }}</td>
          <td>{{ usuario.email }}</td>
          <td>{{ usuario.first_name }} {{ usuario.last_name }}</td>
          <td>{{ usuario.is_staff ? "Sim" : "Não" }}</td>
          <td class="acoes">
            <button @click="abrirModal(usuario)" class="btn-small btn-edit">
              Editar
            </button>
            <button
              @click="deletarUsuario(usuario.id)"
              class="btn-small btn-delete"
            >
              Deletar
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-if="usuarios.length === 0 && !loading" class="vazio">
      Nenhum usuário encontrado
    </div>

    <!-- Modal -->
    <div v-if="modalAberto" class="modal-overlay-container">
      <div class="modal-backdrop" @click="fecharModal()"></div>
      <div class="modal-dialog">
        <div class="modal-header">
          <h2>{{ usuarioEditando ? "Editar Usuário" : "Novo Usuário" }}</h2>
          <button type="button" @click="fecharModal()" class="btn-fechar">
            ✕
          </button>
        </div>

        <form @submit.prevent="salvarUsuario" class="formulario">
          <div class="form-group">
            <label>Username *</label>
            <input
              v-model="form.username"
              type="text"
              required
              :disabled="isEditing"
            />
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Email *</label>
              <input v-model="form.email" type="email" required />
            </div>
            <div class="form-group">
              <label>Telefone *</label>
              <input v-model="form.telefone" type="text" />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Nome *</label>
              <input v-model="form.first_name" type="text" required />
            </div>

            <div class="form-group">
              <label>Sobrenome *</label>
              <input v-model="form.last_name" type="text" required />
            </div>
          </div>

          <div class="form-group">
            <label>Senha *</label>
            <input
              v-model="form.password"
              type="password"
              :required="!isEditing"
            />
            <small v-if="isEditing"
              >Deixe em branco para manter a senha atual</small
            >
          </div>

          <div class="form-group">
            <label class="checkbox-label">
              <input v-model="form.is_staff" type="checkbox" />
              Admin/Staff
            </label>
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

interface Usuario {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  is_staff: boolean;
  telefone: string;
}

const usuarios = ref<Usuario[]>([]);
const loading = ref(false);
const salvando = ref(false);
const modalAberto = ref(false);
const usuarioEditando = ref<Usuario | null>(null);
const erro = ref("");

interface form {
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  password?: string;
  is_staff: boolean;
  telefone: string;
}
const form = ref<form>({
  username: "",
  email: "",
  first_name: "",
  last_name: "",
  password: "",
  is_staff: false,
  telefone: "",
});

const isEditing = computed(() => usuarioEditando.value !== null);

const carregarUsuarios = async () => {
  loading.value = true;
  erro.value = "";
  try {
    const response = await api.get("/usuarios/").catch((err) => {
      console.error("Erro ao carregar usuários:", err);
      return { data: [] };
    });
    usuarios.value = Array.isArray(response.data)
      ? response.data
      : response.data.results || [];
  } catch (error: any) {
    console.error("Erro geral:", error);
    erro.value = "Erro ao carregar usuários";
  } finally {
    loading.value = false;
  }
};

const abrirModal = (usuario: Usuario | null = null) => {
  if (usuario) {
    usuarioEditando.value = usuario;
    form.value = {
      username: usuario.username,
      email: usuario.email,
      first_name: usuario.first_name,
      last_name: usuario.last_name,
      password: "",
      is_staff: usuario.is_staff,
      telefone: usuario.telefone,
    };
  } else {
    usuarioEditando.value = null;
    form.value = {
      username: "",
      email: "",
      first_name: "",
      last_name: "",
      password: "",
      is_staff: false,
      telefone: "",
    };
  }
  modalAberto.value = true;
};

const fecharModal = () => {
  modalAberto.value = false;
  usuarioEditando.value = null;
};

const salvarUsuario = async () => {
  salvando.value = true;
  erro.value = "";
  try {
    const dados = { ...form.value };
    console.log("Criando usuário com dados:", dados);
    if (usuarioEditando.value && !dados.password) {
      delete dados.password;
    }

    if (usuarioEditando.value) {
      await api.put(`/usuarios/${usuarioEditando.value.id}/`, dados);
    } else {
      console.log("Criando usuário com dados:", dados);
      await api.post("/usuarios/", dados);
    }

    fecharModal();
    await carregarUsuarios();
  } catch (error: any) {
    erro.value = error.response?.data?.detail || "Erro ao salvar usuário";
  } finally {
    salvando.value = false;
  }
};

const deletarUsuario = async (id: number) => {
  if (!confirm("Tem certeza que deseja deletar este usuário?")) return;

  try {
    await api.delete(`/usuarios/${id}/`);
    await carregarUsuarios();
  } catch (error: any) {
    erro.value = "Erro ao deletar usuário";
  }
};

onMounted(() => {
  carregarUsuarios();
});
</script>

<style scoped>
.usuarios-container {
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

.modal {
  background: white;
  border-radius: 0.5rem;
  max-width: 500px;
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

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-row .form-group {
  margin-bottom: 0;
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
  font-weight: 600;
}

.checkbox-label input {
  width: auto;
}

small {
  display: block;
  margin-top: 0.25rem;
  font-size: 0.875rem;
  color: #6b7280;
}
</style>
