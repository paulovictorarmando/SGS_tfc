<script setup lang="ts">
import api from "~/composables/api";

definePageMeta({
  middleware: "auth",
});

interface Estatisticas {
  entradas: { quantidade: number; valor: number };
  vendas: { quantidade: number; valor: number };
  perdas: { quantidade: number; valor: number };
  totalProdutos: number;
  totalCategorias: number;
  totalUsuarios: number;
  usuariosTopVendas: { nome: string; total: number }[];
  produtosTopVendas: { nome: string; quantidade: number }[];
}

const stats = ref<Estatisticas>({
  entradas: { quantidade: 0, valor: 0 },
  vendas: { quantidade: 0, valor: 0 },
  perdas: { quantidade: 0, valor: 0 },
  totalProdutos: 0,
  totalCategorias: 0,
  totalUsuarios: 0,
  usuariosTopVendas: [],
  produtosTopVendas: [],
});
const loading = ref(true);

const carregarEstatisticas = async () => {
  try {
    const [movRes, prodRes, catRes, usrRes] = await Promise.all([
      api.get("/movimentacoes/").catch((err) => {
        console.error("Erro movimentações:", err);
        return { data: { results: [] } };
      }),
      api.get("/produtos/").catch((err) => {
        console.error("Erro produtos:", err);
        return { data: { results: [] } };
      }),
      api.get("/categorias/").catch((err) => {
        console.error("Erro categorias:", err);
        return { data: { results: [] } };
      }),
      api.get("/usuarios/").catch((err) => {
        console.error("Erro usuários:", err);
        return { data: { results: [] } };
      }),
    ]);

    const movimentacoes = Array.isArray(movRes.data)
      ? movRes.data
      : movRes.data.results || [];
    const produtos = Array.isArray(prodRes.data)
      ? prodRes.data
      : prodRes.data.results || [];

    // Processar movimentações por tipo
    const entradas = movimentacoes.filter(
      (m: any) => m.tipo_movimentacao === "entrada",
    );
    const vendas = movimentacoes.filter(
      (m: any) => m.tipo_movimentacao === "venda",
    );
    const perdas = movimentacoes.filter(
      (m: any) => m.tipo_movimentacao === "perda",
    );

    // Calcular totais por tipo
    const calcularTotais = (movs: any[]) => {
      return movs.reduce(
        (acc, mov) => {
          const qtd =
            mov.itens?.reduce(
              (total: number, item: any) => total + item.quantidade,
              0,
            ) || 0;
          const valor =
            mov.itens?.reduce((total: number, item: any) => {
              const prod = produtos.find((p: any) => p.id === item.produto);
              let preco = 0;
              if (prod) {
                if (mov.tipo_movimentacao === "venda") {
                  preco = prod.preco_venda;
                } else if (
                  mov.tipo_movimentacao === "entrada" ||
                  mov.tipo_movimentacao === "perda"
                ) {
                  preco = prod.preco_compra;
                }
              }
              return total + item.quantidade * preco;
            }, 0) || 0;
          return { quantidade: acc.quantidade + qtd, valor: acc.valor + valor };
        },
        { quantidade: 0, valor: 0 },
      );
    };

    // Top usuários por vendas
    const usuariosVendas: { [key: number]: { nome: string; total: number } } =
      {};
    vendas.forEach((mov: any) => {
      if (!usuariosVendas[mov.autor]) {
        usuariosVendas[mov.autor] = {
          nome: mov.autor_nome || `Usuário ${mov.autor}`,
          total: 0,
        };
      }
      const valor =
        mov.itens?.reduce((total: number, item: any) => {
          const prod = produtos.find((p: any) => p.id === item.produto);
          return total + item.quantidade * (prod?.preco_venda || 0);
        }, 0) || 0;
      usuariosVendas[mov.autor].total += valor;
    });

    // Top produtos vendidos
    const produtosVendas: {
      [key: number]: { nome: string; quantidade: number };
    } = {};
    vendas.forEach((mov: any) => {
      mov.itens?.forEach((item: any) => {
        const prod = produtos.find((p: any) => p.id === item.produto);
        if (!produtosVendas[item.produto]) {
          produtosVendas[item.produto] = {
            nome: prod?.nome || `Produto ${item.produto}`,
            quantidade: 0,
          };
        }
        produtosVendas[item.produto].quantidade += item.quantidade;
      });
    });

    stats.value = {
      entradas: calcularTotais(entradas),
      vendas: calcularTotais(vendas),
      perdas: calcularTotais(perdas),
      totalProdutos: produtos.length,
      totalCategorias: Array.isArray(catRes.data)
        ? catRes.data.length
        : catRes.data.results?.length || 0,
      totalUsuarios: Array.isArray(usrRes.data)
        ? usrRes.data.length
        : usrRes.data.results?.length || 0,
      usuariosTopVendas: Object.values(usuariosVendas)
        .sort((a, b) => b.total - a.total)
        .slice(0, 5),
      produtosTopVendas: Object.values(produtosVendas)
        .sort((a, b) => b.quantidade - a.quantidade)
        .slice(0, 5),
    };
  } catch (error) {
    console.error("Erro geral ao carregar estatísticas:", error);
  } finally {
    loading.value = false;
  }
};

const formatarPreco = (preco: number) => {
  return new Intl.NumberFormat("pt-AO", {
    style: "currency",
    currency: "AOA",
  }).format(preco);
};

onMounted(() => {
  carregarEstatisticas();
});
</script>

<template>
  <div class="w-full p-6">
    <div class="max-w-7xl mx-auto">
      <h1 class="text-3xl font-bold mb-8">📊 Dashboard de Gestão</h1>

      <div v-if="loading" class="text-center py-12">
        <p class="text-gray-500">Carregando estatísticas...</p>
      </div>

      <div v-else class="space-y-8">
        <!-- Cards Principais -->
        <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-3 gap-4">
          <div
            class="bg-green-50 border-l-4 border-green-500 p-6 rounded shadow"
          >
            <div class="flex justify-between items-start">
              <div>
                <h3 class="text-green-700 font-semibold text-sm">
                  📥 Entradas
                </h3>
                <p class="text-2xl font-bold text-green-600 mt-2">
                  {{ stats.entradas.quantidade }}
                </p>
                <p class="text-sm text-gray-600 mt-1">
                  {{ formatarPreco(stats.entradas.valor) }}
                </p>
              </div>
            </div>
          </div>

          <div class="bg-blue-50 border-l-4 border-blue-500 p-6 rounded shadow">
            <div class="flex justify-between items-start">
              <div>
                <h3 class="text-blue-700 font-semibold text-sm">🛍️ Vendas</h3>
                <p class="text-2xl font-bold text-blue-600 mt-2">
                  {{ stats.vendas.quantidade }}
                </p>
                <p class="text-sm text-gray-600 mt-1">
                  {{ formatarPreco(stats.vendas.valor) }}
                </p>
              </div>
            </div>
          </div>

          <div class="bg-red-50 border-l-4 border-red-500 p-6 rounded shadow">
            <div class="flex justify-between items-start">
              <div>
                <h3 class="text-red-700 font-semibold text-sm">⚠️ Perdas</h3>
                <p class="text-2xl font-bold text-red-600 mt-2">
                  {{ stats.perdas.quantidade }}
                </p>
                <p class="text-sm text-gray-600 mt-1">
                  {{ formatarPreco(stats.perdas.valor) }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Cards Informativos -->
        <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-3 gap-4">
          <NuxtLink
            to="/produtos"
            class="bg-white border border-gray-200 p-6 rounded shadow hover:shadow-lg transition cursor-pointer"
          >
            <div>
              <h3 class="text-gray-700 font-semibold text-sm">
                📦 Total de Produtos
              </h3>
              <p class="text-3xl font-bold text-primary mt-2">
                {{ stats.totalProdutos }}
              </p>
            </div>
          </NuxtLink>

          <NuxtLink
            to="/categorias"
            class="bg-white border border-gray-200 p-6 rounded shadow hover:shadow-lg transition cursor-pointer"
          >
            <div>
              <h3 class="text-gray-700 font-semibold text-sm">🏷️ Categorias</h3>
              <p class="text-3xl font-bold text-primary mt-2">
                {{ stats.totalCategorias }}
              </p>
            </div>
          </NuxtLink>

          <NuxtLink
            to="/usuarios"
            class="bg-white border border-gray-200 p-6 rounded shadow hover:shadow-lg transition cursor-pointer"
          >
            <div>
              <h3 class="text-gray-700 font-semibold text-sm">👥 Usuários</h3>
              <p class="text-3xl font-bold text-primary mt-2">
                {{ stats.totalUsuarios }}
              </p>
            </div>
          </NuxtLink>
        </div>

        <!-- Usuários Top Vendas -->
        <div class="bg-white border border-gray-200 rounded shadow p-6">
          <h2 class="text-lg font-bold mb-4 text-black">
            🏆 Top 5 Usuários (Vendas)
          </h2>
          <div v-if="stats.usuariosTopVendas.length > 0" class="space-y-2">
            <div
              v-for="(usuario, idx) in stats.usuariosTopVendas"
              :key="idx"
              class="flex justify-between items-center p-3 bg-gray-50 rounded"
            >
              <div class="flex items-center gap-3">
                <span class="text-xl font-bold text-gray-400">{{
                  idx + 1
                }}</span>
                <span class="font-semibold text-gray-800">{{
                  usuario.nome
                }}</span>
              </div>
              <span class="font-bold text-blue-600">{{
                formatarPreco(usuario.total)
              }}</span>
            </div>
          </div>
          <div v-else class="text-center py-6 text-gray-500">
            Nenhuma venda registrada
          </div>
        </div>

        <!-- Produtos Top Vendas -->
        <div class="bg-white border border-gray-200 rounded shadow p-6">
          <h2 class="text-lg font-bold mb-4 text-black">
            ⭐ Top 5 Produtos (Mais Vendidos)
          </h2>
          <div v-if="stats.produtosTopVendas.length > 0" class="space-y-2">
            <div
              v-for="(produto, idx) in stats.produtosTopVendas"
              :key="idx"
              class="flex justify-between items-center p-3 bg-gray-50 rounded"
            >
              <div class="flex items-center gap-3">
                <span class="text-xl font-bold text-gray-400">{{
                  idx + 1
                }}</span>
                <span class="font-semibold text-gray-800">{{
                  produto.nome
                }}</span>
              </div>
              <span class="font-bold text-green-600"
                >{{ produto.quantidade }} un.</span
              >
            </div>
          </div>
          <div v-else class="text-center py-6 text-gray-500">
            Nenhuma venda registrada
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
