<template>
  <div class="w-full p-6">
    <div class="max-w-6xl mx-auto">
      <div class="flex items-center justify-between mb-6">
        <h1 class="text-2xl font-bold">💰 Vendas</h1>
        <button class="btn btn-primary" @click="abrirModal()">+ Nova Movimentação</button>
      </div>

      <div v-if="erro" class="alert alert-error mb-4">
        <span>{{ erro }}</span>
      </div>

      <div v-if="loading" class="text-center py-12 text-base-content/70">
        Carregando...
      </div>

      <div v-else class="overflow-x-auto bg-base-100 rounded-box shadow">
        <table class="table">
          <thead>
            <tr>
              <th>Tipo</th>
              <th>Descrição</th>
              <th>Data</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="mov in movimentacoes" :key="mov.id">
              <td class="capitalize">{{ mov.tipo }}</td>
              <td>{{ mov.descricao || "-" }}</td>
              <td>{{ formatarData(mov.data) }}</td>
              <td class="space-x-2">
                <button class="btn btn-sm btn-outline" @click="abrirModal(mov)">Editar</button>
                <button class="btn btn-sm btn-error" @click="deletarMovimentacao(mov.id)">Deletar</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <dialog class="modal" :class="{ 'modal-open': modalAberto }">
    <div class="modal-box max-w-2xl">
      <h3 class="font-bold text-lg mb-4">
        {{ movEditando ? "Editar Movimentação" : "Nova Movimentação" }}
      </h3>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-3 mb-4">
        <label class="form-control">
          <span class="label-text">Tipo</span>
          <select v-model="form.tipo" class="select select-bordered">
            <option value="entrada">Entrada</option>
            <option value="venda">Venda</option>
            <option value="perda">Perda</option>
          </select>
        </label>
        <label class="form-control md:col-span-2">
          <span class="label-text">Descrição</span>
          <input v-model="form.descricao" class="input input-bordered" type="text" />
        </label>
      </div>

      <label class="form-control mb-4">
        <span class="label-text">Data</span>
        <input v-model="form.data" class="input input-bordered" type="date" />
      </label>

      <div class="divider">Itens</div>
      <div class="grid grid-cols-1 md:grid-cols-4 gap-2 mb-3">
        <select v-model="itemForm.produto" class="select select-bordered">
          <option value="">Produto</option>
          <option v-for="produto in produtos" :key="produto.id" :value="String(produto.id)">
            {{ produto.nome }}
          </option>
        </select>
        <input v-model="itemForm.quantidade" class="input input-bordered" type="number" min="1" placeholder="Qtd" />
        <input v-model="itemForm.preco_unitario" class="input input-bordered" type="number" min="0" step="0.01" placeholder="Preço" />
        <button class="btn btn-secondary" type="button" @click="adicionarItem">Adicionar</button>
      </div>

      <ul class="menu bg-base-200 rounded-box mb-4">
        <li v-for="(item, index) in itens" :key="`${item.produto}-${index}`">
          <div class="flex items-center justify-between">
            <span>
              {{ buscarNomeProduto(item.produto) }} — {{ item.quantidade }} x
              {{ formatarPreco(item.preco_unitario) }}
            </span>
            <button class="btn btn-xs btn-error" @click="removerItem(index)">remover</button>
          </div>
        </li>
        <li v-if="itens.length === 0" class="text-base-content/60 px-3 py-2">Nenhum item adicionado</li>
      </ul>

      <div class="modal-action">
        <button class="btn" type="button" @click="fecharModal">Cancelar</button>
        <button class="btn btn-primary" type="button" :disabled="salvando" @click="salvarMovimentacao">
          {{ salvando ? "Salvando..." : "Salvar" }}
        </button>
      </div>
    </div>
    <form method="dialog" class="modal-backdrop">
      <button @click.prevent="fecharModal">close</button>
    </form>
  </dialog>
</template>

<script setup lang="ts">
import api from "~/composables/api";

definePageMeta({
  middleware: 'auth',
});

interface Movimentacao {
  id: number;
  tipo: string;
  descricao: string;
  data: string;
}

interface Produto {
  id: number;
  nome: string;
}

interface ItemMovimentacao {
  produto: number;
  quantidade: number;
  preco_unitario: number;
}

interface MovimentacaoForm {
  tipo: string;
  descricao: string;
  data: string;
}

interface ItemForm {
  produto: string;
  quantidade: string;
  preco_unitario: string;
}

const movimentacoes = ref<Movimentacao[]>([]);
const itens = ref<ItemMovimentacao[]>([]);
const produtos = ref<Produto[]>([]);
const loading = ref(false);
const salvando = ref(false);
const modalAberto = ref(false);
const movEditando = ref<Movimentacao | null>(null);
const erro = ref('');

const form = ref<MovimentacaoForm>({
  tipo: 'entrada',
  descricao: '',
  data: new Date().toISOString().slice(0, 10),
});

const itemForm = ref<ItemForm>({
  produto: '',
  quantidade: '',
  preco_unitario: '',
});

const formatarData = (data: string) => {
  return new Date(data).toLocaleDateString("pt-BR");
};

const formatarPreco = (preco: string | number) => {
  return new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(Number(preco));
};

const carregarDados = async () => {
  loading.value = true;
  erro.value = '';
  try {
    const [movRes, prodRes] = await Promise.all([
      api.get("/movimentacoes/").catch(err => {
        console.error('Erro ao carregar movimentações:', err);
        return { data: [] };
      }),
      api.get("/produtos/").catch(err => {
        console.error('Erro ao carregar produtos:', err);
        return { data: [] };
      }),
    ]);

    movimentacoes.value = Array.isArray(movRes.data) ? movRes.data : movRes.data.results || [];
    produtos.value = Array.isArray(prodRes.data) ? prodRes.data : prodRes.data.results || [];
  } catch (error: any) {
    console.error('Erro geral:', error);
    erro.value = "Erro ao carregar dados";
  } finally {
    loading.value = false;
  }
};

const abrirModal = (mov: Movimentacao | null = null) => {
  if (mov) {
    movEditando.value = mov;
    form.value = {
      tipo: mov.tipo,
      descricao: mov.descricao,
      data: mov.data,
    };
  } else {
    movEditando.value = null;
    form.value = {
      tipo: 'entrada',
      descricao: '',
      data: new Date().toISOString().slice(0, 10),
    };
  }
  itens.value = [];
  itemForm.value = {
    produto: '',
    quantidade: '',
    preco_unitario: '',
  };
  modalAberto.value = true;
};

const fecharModal = () => {
  modalAberto.value = false;
  movEditando.value = null;
};

const buscarNomeProduto = (produtoId: number) => {
  return produtos.value.find(produto => produto.id === produtoId)?.nome || `Produto #${produtoId}`;
};

const adicionarItem = () => {
  if (itemForm.value.produto && itemForm.value.quantidade && itemForm.value.preco_unitario) {
    itens.value.push({
      produto: parseInt(itemForm.value.produto),
      quantidade: parseFloat(itemForm.value.quantidade),
      preco_unitario: parseFloat(itemForm.value.preco_unitario),
    });
    itemForm.value = { produto: '', quantidade: '', preco_unitario: '' };
  }
};

const removerItem = (index: number) => {
  itens.value.splice(index, 1);
};

const salvarMovimentacao = async () => {
  if (itens.value.length === 0) {
    erro.value = 'Adicione pelo menos um item';
    return;
  }

  salvando.value = true;
  erro.value = '';
  try {
    if (movEditando.value) {
      await api.put(`/movimentacoes/${movEditando.value.id}/`, form.value);
    } else {
      const mov = await api.post("/movimentacoes/", form.value);

      for (const item of itens.value) {
        await api.post("/itens-movimentacao/", {
          movimentacao: mov.data.id,
          ...item,
        });
      }
    }

    fecharModal();
    await carregarDados();
  } catch (error: any) {
    erro.value = error.response?.data?.detail || "Erro ao salvar movimentação";
  } finally {
    salvando.value = false;
  }
};

const deletarMovimentacao = async (id: number) => {
  if (!confirm("Tem certeza que deseja deletar esta movimentação?")) return;

  try {
    await api.delete(`/movimentacoes/${id}/`);
    await carregarDados();
  } catch (error: any) {
    erro.value = "Erro ao deletar movimentação";
  }
};

onMounted(() => {
  carregarDados();
});
</script>
