<template>
  <ul class="menu bg-base-200 min-h-full rounded-box w-56 p-4">
    <li class="mb-2">
      <NuxtLink to="/home" class="font-semibold">📊 Home</NuxtLink>
    </li>
    <div class="divider my-2"></div>
    <li>
      <NuxtLink to="/vendas">💰 Vendas</NuxtLink>
    </li>
    <li>
      <NuxtLink to="/produtos">📦 Produtos</NuxtLink>
    </li>
    <li>
      <NuxtLink to="/categorias">🏷️ Categorias</NuxtLink>
    </li>
    <li>
      <NuxtLink to="/usuarios">👥 Usuários</NuxtLink>
    </li>
    <div class="divider my-2"></div>
    <li>
      <NuxtLink to="/perfil">👤 Meu Perfil</NuxtLink>
    </li>
  </ul>
</template>
