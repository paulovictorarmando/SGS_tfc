<script setup lang="ts">
import { useClearTokens } from "~/composables/auth";

const handleSair = async () => {
  useClearTokens();
  await navigateTo("/login");
};
import api from "~/composables/api";

interface Usuario {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
}

const response = await api.get("/usuarios/me/").catch((err) => {
      return { data: [] };});
const usuario = ref<Usuario>(response.data);
</script>

<template>
  <div class="navbar bg-base-100 shadow-md">
    <div class="flex-1">
      <NuxtLink to="/home" class="btn btn-ghost text-xl font-bold"
        >SGS 📊</NuxtLink
      >
    </div>
    <div class="flex-none gap-2">
      <div class="dropdown dropdown-end">
      </div>
      <ul class="menu menu-horizontal px-1 gap-2">
        <li><NuxtLink to="/perfil">👤 {{ usuario.email }}</NuxtLink></li>
        <li><button @click="handleSair">🚪 Sair</button></li>
      </ul>
    </div>
  </div>
</template>
