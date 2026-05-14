<template>
  <div class="produtos-container">
    <div class="header">
      <h1>📦 Produtos</h1>
      <button @click="abrirModal()" class="btn-primary">+ Novo Produto</button>
    </div>

    <div v-if="erro" class="alert-error">{{ erro }}</div>

    <div v-if="loading" class="loading">Carregando...</div>

    <table v-else class="tabela">
      <thead>
        <tr>
          <th>Nome</th>
          <th>Descrição</th>
          <th>Preço</th>
          <th>Categoria</th>
          <th>Ações</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="produto in produtos" :key="produto.id">
          <td>{{ produto.nome }}</td>
          <td>{{ produto.descricao }}</td>
          <td>{{ formatarPreco(produto.preco) }}</td>
          <td>{{ produto.categoria_nome || '-' }}</td>
          <td class="acoes">
            <button @click="abrirModal(produto)" class="btn-small btn-edit">
              Editar
            </button>
            <button
              @click="deletarProduto(produto.id)"
              class="btn-small btn-delete"
            >
              Deletar
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-if="produtos.length === 0 && !loading" class="vazio">
      Nenhum produto encontrado
    </div>

    <!-- Modal -->
    <div v-if="modalAberto" class="modal-overlay" @click.self="fecharModal()">
      <div class="modal">
        <div class="modal-header">
          <h2>{{ produtoEditando ? "Editar Produto" : "Novo Produto" }}</h2>
          <button @click="fecharModal()" class="btn-fechar">✕</button>
        </div>

        <form @submit.prevent="salvarProduto" class="formulario">
          <div class="form-group">
            <label>Nome *</label>
            <input v-model="form.nome" type="text" required maxlength="100" />
          </div>

          <div class="form-group">
            <label>Descrição</label>
            <textarea v-model="form.descricao" class="textarea"></textarea>
          </div>

          <div class="form-group">
            <label>Categoria *</label>
            <select v-model="form.categoria" required>
              <option value="">Selecione uma categoria</option>
              <option v-for="cat in categorias" :key="cat.id" :value="cat.id">
                {{ cat.nome }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label>Preço *</label>
            <input
              v-model="form.preco"
              type="number"
              step="0.01"
              required
              placeholder="0.00"
            />
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

interface Produto {
  id: number;
  nome: string;
  descricao: string;
  preco: string | number;
  categoria: number;
  categoria_nome?: string;
}

interface Categoria {
  id: number;
  nome: string;
}

interface ProdutoForm {
  nome: string;
  categoria: string;
  preco: string;
  descricao: string;
}

const produtos = ref<Produto[]>([]);
const categorias = ref<Categoria[]>([]);
const loading = ref(false);
const salvando = ref(false);
const modalAberto = ref(false);
const produtoEditando = ref<Produto | null>(null);
const erro = ref('');

const form = ref<ProdutoForm>({
  nome: "",
  categoria: "",
  preco: "",
  descricao: "",
});

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
    const [produtosRes, categoriasRes] = await Promise.all([
      api.get("/produtos/").catch(err => {
        console.error('Erro ao carregar produtos:', err);
        return { data: [] };
      }),
      api.get("/categorias/").catch(err => {
        console.error('Erro ao carregar categorias:', err);
        return { data: [] };
      }),
    ]);
    produtos.value = Array.isArray(produtosRes.data) ? produtosRes.data : produtosRes.data.results || [];
    categorias.value = Array.isArray(categoriasRes.data) ? categoriasRes.data : categoriasRes.data.results || [];
  } catch (error: any) {
    console.error('Erro geral:', error);
    erro.value = "Erro ao carregar dados";
  } finally {
    loading.value = false;
  }
};

const abrirModal = (produto: Produto | null = null) => {
  if (produto) {
    produtoEditando.value = produto;
    form.value = {
      nome: produto.nome,
      categoria: String(produto.categoria),
      preco: String(produto.preco),
      descricao: produto.descricao || "",
    };
  } else {
    produtoEditando.value = null;
    form.value = {
      nome: "",
      categoria: "",
      preco: "",
      descricao: "",
    };
  }
  modalAberto.value = true;
};

const fecharModal = () => {
  modalAberto.value = false;
  produtoEditando.value = null;
};

const salvarProduto = async () => {
  salvando.value = true;
  erro.value = '';
  try {
    const dados = {
      nome: form.value.nome,
      categoria: parseInt(form.value.categoria),
      preco: parseFloat(form.value.preco),
      descricao: form.value.descricao,
    };

    if (produtoEditando.value) {
      await api.put(`/produtos/${produtoEditando.value.id}/`, dados);
    } else {
      await api.post("/produtos/", dados);
    }

    fecharModal();
    await carregarDados();
  } catch (error: any) {
    erro.value = error.response?.data?.detail || "Erro ao salvar produto";
  } finally {
    salvando.value = false;
  }
};

const deletarProduto = async (id: number) => {
  if (!confirm("Tem certeza que deseja deletar este produto?")) return;

  try {
    await api.delete(`/produtos/${id}/`);
    await carregarDados();
  } catch (error: any) {
    erro.value = "Erro ao deletar produto";
  }
};

onMounted(() => {
  carregarDados();
});
</script>
