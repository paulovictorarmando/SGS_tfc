<script setup lang="ts">
import api from "~/composables/api";
import { setTokens } from "~/composables/auth";

definePageMeta({
  layout: "auth",
});

const username = ref("");
const password = ref("");
const erro = ref("");
const isLoading = ref(false);

const handleLogin = async () => {
  if (!username.value || !password.value) {
    erro.value = "Preencha todos os campos";
    return;
  }

  isLoading.value = true;
  erro.value = "";

  try {
    const response = await api.post("/auth/login/", {
      username: username.value,
      password: password.value,
    });

    if (!response.data.access || !response.data.refresh) {
      erro.value = "Erro ao receber tokens do servidor";
      return;
    }

    setTokens(response.data.access, response.data.refresh);

    // Aguarda um pouco para garantir que o token foi salvo
    await new Promise(resolve => setTimeout(resolve, 100));

    await navigateTo("/home");
  } catch (error: any) {
    const status = error.response?.status;
    if (status === 401) {
      erro.value = "Usuário ou senha incorretos";
    } else if (status === 400) {
      erro.value = "Dados inválidos";
    } else {
      erro.value = error.response?.data?.detail || "Erro ao fazer login";
    }
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
  <div class="hero bg-base-200 min-h-screen">
    <div class="hero-content flex-col lg:flex-row-reverse">
      <div class="text-center lg:text-left">
        <h1 class="text-5xl font-bold">SGS</h1>
        <p class="py-4">
          Sistema de Gestão de Estoque <br />
          Informe suas credenciais para ter acesso ao sistema ou fale com o
          administrador!
        </p>
      </div>

      <div class="card bg-base-100 w-full max-w-sm shadow-2xl">
        <form class="card-body" @submit.prevent="handleLogin">
          <div v-if="erro" class="alert alert-error">
            <span>{{ erro }}</span>
          </div>

          <div class="form-control">
            <label class="label">
              <span class="label-text">Nome de usuário</span>
            </label>
            <input
              v-model="username"
              type="text"
              placeholder="nome de usuário"
              class="input input-bordered"
              required
            />
          </div>

          <div class="form-control">
            <label class="label">
              <span class="label-text">Palavra passe</span>
            </label>
            <input
              v-model="password"
              type="password"
              placeholder="Palavra passe"
              class="input input-bordered"
              required
            />
          </div>

          <div class="form-control mt-6">
            <button class="btn btn-primary" type="submit" :disabled="isLoading">
              <span
                v-if="isLoading"
                class="loading loading-spinner loading-sm"
              ></span>
              {{ isLoading ? "Entrando..." : "Login" }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
