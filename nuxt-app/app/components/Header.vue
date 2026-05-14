<script setup lang="ts">
import { useClearTokens } from "~/composables/auth";

const handleSair = async () => {
  useClearTokens();
  await navigateTo("/login");
};
</script>

<template>
  <div class="navbar bg-base-100 shadow-sm">
    <div class="flex-1">
      <NuxtLink to="/home" class="btn btn-ghost text-xl">SGS</NuxtLink>
    </div>
    <div class="flex-none">
      <ul class="menu menu-horizontal px-1">
        <li>
          <details>
            <summary>Menu</summary>
            <ul class="bg-base-100 rounded-t-none p-2">
              <li><NuxtLink to="/perfil">Meu Perfil</NuxtLink></li>
              <li><button @click="handleSair">Sair</button></li>
            </ul>
          </details>
        </li>
      </ul>
    </div>
  </div>
</template>
