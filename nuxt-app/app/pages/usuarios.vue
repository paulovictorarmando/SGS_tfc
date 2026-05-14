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
    <div v-if="modalAberto" class="modal-overlay" @click.self="fecharModal()">
      <div class="modal">
        <div class="modal-header">
          <h2>{{ usuarioEditando ? "Editar Usuário" : "Novo Usuário" }}</h2>
          <button @click="fecharModal()" class="btn-fechar">✕</button>
        </div>

        <form @submit.prevent="salvarUsuario" class="formulario">
          <div class="form-group">
            <label>Username *</label>
            <input
              v-model="form.username"
              type="text"
              required
              :disabled="Boolean(usuarioEditando)"
            />
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Email *</label>
              <input v-model="form.email" type="email" required />
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
              :required="!usuarioEditando"
            />
            <small v-if="usuarioEditando"
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
  middleware: 'auth',
});

interface Usuario {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  is_staff: boolean;
}

interface UsuarioForm {
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  password?: string;
  is_staff: boolean;
}

const usuarios = ref<Usuario[]>([]);
const loading = ref(false);
const salvando = ref(false);
const modalAberto = ref(false);
const usuarioEditando = ref<Usuario | null>(null);
const erro = ref('');

const form = ref<UsuarioForm>({
  username: "",
  email: "",
  first_name: "",
  last_name: "",
  password: "",
  is_staff: false,
});

const carregarUsuarios = async () => {
  loading.value = true;
  erro.value = '';
  try {
    const response = await api.get("/usuarios/").catch(err => {
      console.error('Erro ao carregar usuários:', err);
      return { data: [] };
    });
    usuarios.value = Array.isArray(response.data) ? response.data : response.data.results || [];
  } catch (error: any) {
    console.error('Erro geral:', error);
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
  erro.value = '';
  try {
    const dados: UsuarioForm = { ...form.value };

    if (usuarioEditando.value && !dados.password) {
      delete dados.password;
    }

    if (usuarioEditando.value) {
      await api.put(`/usuarios/${usuarioEditando.value.id}/`, dados);
    } else {
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
