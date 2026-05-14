<script setup lang="ts">
import { useClearTokens } from "~/composables/auth";

const handleSair = async () => {
  useClearTokens();
  await navigateTo("/login");
};
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
        <div tabindex="0" class="btn btn-ghost gap-2">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            class="w-5 h-5 stroke-current"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M3 12a9 9 0 110 18 9 9 0 010-18z"
            ></path>
          </svg>
          Menu
        </div>
      </div>
      <ul class="menu menu-horizontal px-1 gap-2">
        <li>
          <NuxtLink to="/movimentos" class="btn btn-ghost btn-sm"
            >Movimentações</NuxtLink
          >
        </li>
        <li>
          <NuxtLink to="/produtos" class="btn btn-ghost btn-sm"
            >Produtos</NuxtLink
          >
        </li>
        <li>
          <NuxtLink to="/categorias" class="btn btn-ghost btn-sm"
            >Categorias</NuxtLink
          >
        </li>
        <li>
          <NuxtLink to="/usuarios" class="btn btn-ghost btn-sm"
            >Usuários</NuxtLink
          >
        </li>
      </ul>
      <div class="dropdown dropdown-end">
        <div tabindex="0" class="btn btn-circle btn-ghost">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            class="w-5 h-5 stroke-current"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            ></path>
          </svg>
        </div>
        <ul
          tabindex="0"
          class="dropdown-content z-50 menu p-2 shadow bg-base-100 rounded-box w-52"
        >
          <li><NuxtLink to="/perfil">👤 Meu Perfil</NuxtLink></li>
          <li><button @click="handleSair">🚪 Sair</button></li>
        </ul>
      </div>
    </div>
  </div>
</template>
