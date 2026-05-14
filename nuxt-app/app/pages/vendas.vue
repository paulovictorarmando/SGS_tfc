<script setup lang="ts">
import api from "~/composables/api";

definePageMeta({
  middleware: 'auth',
});

const movimentacoes = ref([]);
const itens = ref([]);
const produtos = ref([]);
const loading = ref(false);
const salvando = ref(false);
const modalAberto = ref(false);
const movEditando = ref(null);
const erro = ref('');

const form = ref({
  tipo: 'entrada',
  descricao: '',
  data: new Date().toISOString().split('T')[0],
});

const itemForm = ref({
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

const abrirModal = (mov: any = null) => {
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
      data: new Date().toISOString().split('T')[0],
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
