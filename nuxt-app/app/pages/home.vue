<script setup lang="ts">
import api from "~/composables/api";

definePageMeta({
  middleware: 'auth',
});

const vendas = ref(0);
const produtos = ref(0);
const categorias = ref(0);
const usuarios = ref(0);
const loading = ref(true);

const carregarEstatisticas = async () => {
  try {
    const [vendasRes, produtosRes, categoriasRes, usuariosRes] = await Promise.all([
      api.get("/movimentacoes/").catch(err => {
        console.error('Erro movimentações:', err);
        return { data: { results: [] } };
      }),
      api.get("/produtos/").catch(err => {
        console.error('Erro produtos:', err);
        return { data: { results: [] } };
      }),
      api.get("/categorias/").catch(err => {
        console.error('Erro categorias:', err);
        return { data: { results: [] } };
      }),
      api.get("/usuarios/").catch(err => {
        console.error('Erro usuários:', err);
        return { data: { results: [] } };
      }),
    ]);

    vendas.value = Array.isArray(vendasRes.data) ? vendasRes.data.length : (vendasRes.data.results?.length || 0);
    produtos.value = Array.isArray(produtosRes.data) ? produtosRes.data.length : (produtosRes.data.results?.length || 0);
    categorias.value = Array.isArray(categoriasRes.data) ? categoriasRes.data.length : (categoriasRes.data.results?.length || 0);
    usuarios.value = Array.isArray(usuariosRes.data) ? usuariosRes.data.length : (usuariosRes.data.results?.length || 0);
  } catch (error) {
    console.error('Erro geral ao carregar estatísticas:', error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  carregarEstatisticas();
});
</script>

<template>
  <div class="w-full p-6">
    <div class="max-w-6xl mx-auto">
      <h1 class="text-3xl font-bold mb-8">📊 Sistema de Gestão de Estoque</h1>

      <div v-if="loading" class="text-center py-12">
        <p class="text-gray-500">Carregando estatísticas...</p>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <NuxtLink to="/vendas" class="card bg-base-100 shadow-md hover:shadow-lg transition cursor-pointer">
          <div class="card-body">
            <h2 class="card-title text-sm">💰 Vendas</h2>
            <p class="text-2xl font-bold text-primary">{{ vendas }}</p>
          </div>
        </NuxtLink>

        <NuxtLink to="/produtos" class="card bg-base-100 shadow-md hover:shadow-lg transition cursor-pointer">
          <div class="card-body">
            <h2 class="card-title text-sm">📦 Produtos</h2>
            <p class="text-2xl font-bold text-primary">{{ produtos }}</p>
          </div>
        </NuxtLink>

        <NuxtLink to="/categorias" class="card bg-base-100 shadow-md hover:shadow-lg transition cursor-pointer">
          <div class="card-body">
            <h2 class="card-title text-sm">🏷️ Categorias</h2>
            <p class="text-2xl font-bold text-primary">{{ categorias }}</p>
          </div>
        </NuxtLink>

        <NuxtLink to="/usuarios" class="card bg-base-100 shadow-md hover:shadow-lg transition cursor-pointer">
          <div class="card-body">
            <h2 class="card-title text-sm">👥 Usuários</h2>
            <p class="text-2xl font-bold text-primary">{{ usuarios }}</p>
          </div>
        </NuxtLink>
      </div>
    </div>
  </div>
</template>
