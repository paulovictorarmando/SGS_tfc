<script setup lang="ts">
import api from "~/composables/api";

definePageMeta({
  middleware: 'auth',
});

const perfil = ref({
  nome: "",
  sobrenome: "",
  username: "",
  email: "",
});

const isEditing = ref(false);
const isSaving = ref(false);
const erro = ref('');
const loading = ref(true);

onMounted(async () => {
  try {
    const res = await api.get("/usuarios/me/").catch(err => {
      console.error('Erro ao carregar perfil:', err);
      return { data: {} };
    });
    perfil.value = {
      nome: res.data?.first_name || "",
      sobrenome: res.data?.last_name || "",
      username: res.data?.username || "",
      email: res.data?.email || "",
    };
  } catch (error: any) {
    console.error('Erro geral:', error);
    erro.value = "Erro ao carregar dados do perfil";
  } finally {
    loading.value = false;
  }
});

const handleSave = async () => {
  isSaving.value = true;
  erro.value = '';

  try {
    await api.put("/usuarios/me/", {
      first_name: perfil.value.nome,
      last_name: perfil.value.sobrenome,
      email: perfil.value.email,
    });

    isEditing.value = false;
  } catch (error: any) {
    erro.value = error.response?.data?.detail || "Erro ao atualizar perfil";
  } finally {
    isSaving.value = false;
  }
};

const handleCancel = () => {
  isEditing.value = false;
};
</script>

<template>
  <div class="w-full max-w-2xl mx-auto p-6">
    <div v-if="loading" class="text-center py-12">
      <p class="text-gray-500">Carregando...</p>
    </div>

    <div v-else class="card bg-base-100 shadow-xl">
      <div class="card-body">
        <div class="flex items-center justify-between mb-6">
          <h2 class="card-title text-2xl">👤 Perfil do Usuário</h2>
          <button
            v-if="!isEditing"
            class="btn btn-sm btn-primary"
            @click="isEditing = true"
          >
            Editar
          </button>
        </div>

        <div v-if="erro" class="alert alert-error mb-4">
          <span>{{ erro }}</span>
        </div>

        <div class="divider"></div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="form-control">
            <label class="label">
              <span class="label-text font-semibold">Primeiro Nome</span>
            </label>
            <input
              v-model="perfil.nome"
              type="text"
              class="input input-bordered"
              :disabled="!isEditing"
            />
          </div>

          <div class="form-control">
            <label class="label">
              <span class="label-text font-semibold">Sobrenome</span>
            </label>
            <input
              v-model="perfil.sobrenome"
              type="text"
              class="input input-bordered"
              :disabled="!isEditing"
            />
          </div>

          <div class="form-control">
            <label class="label">
              <span class="label-text font-semibold">Nome de usuário</span>
            </label>
            <input
              v-model="perfil.username"
              type="text"
              class="input input-bordered"
              disabled
            />
          </div>

          <div class="form-control">
            <label class="label">
              <span class="label-text font-semibold">Email</span>
            </label>
            <input
              v-model="perfil.email"
              type="email"
              class="input input-bordered"
              :disabled="!isEditing"
            />
          </div>
        </div>

        <div class="divider"></div>

        <div v-if="isEditing" class="flex gap-2 justify-end">
          <button class="btn btn-ghost" @click="handleCancel" :disabled="isSaving">
            Cancelar
          </button>
          <button
            class="btn btn-primary"
            @click="handleSave"
            :disabled="isSaving"
          >
            <span v-if="isSaving" class="loading loading-spinner loading-sm"></span>
            {{ isSaving ? 'Salvando...' : 'Salvar Alterações' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
