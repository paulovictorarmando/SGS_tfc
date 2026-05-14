import api from "./api";
import { useAlertStore } from "~/stores/alerts";

export interface CRUDState {
  items: Ref<any[]>;
  loading: Ref<boolean>;
  salvando: Ref<boolean>;
  modalAberto: Ref<boolean>;
  itemEditando: Ref<any>;
  erro: Ref<string>;
}

export function useCRUD(endpoint: string) {
  const alertStore = useAlertStore();

  const carregarItens = async (items: Ref<any[]>) => {
    try {
      const response = await api.get(endpoint);
      items.value = Array.isArray(response.data)
        ? response.data
        : response.data.results || [];
      return items.value;
    } catch (error: any) {
      const mensagem =
        error.response?.data?.detail || `Erro ao carregar ${endpoint}`;
      alertStore.addAlert(mensagem, "error");
      return [];
    }
  };

  const salvarItem = async (
    dados: any,
    itemEditando: any,
    items: Ref<any[]>,
  ) => {
    try {
      if (itemEditando?.id) {
        await api.put(`${endpoint}${itemEditando.id}/`, dados);
        alertStore.addAlert("Item atualizado com sucesso!", "success");
      } else {
        await api.post(endpoint, dados);
        alertStore.addAlert("Item criado com sucesso!", "success");
      }

      // Recarrega a lista
      await carregarItens(items);
      return true;
    } catch (error: any) {
      const mensagem = error.response?.data?.detail || "Erro ao salvar item";
      alertStore.addAlert(mensagem, "error");
      return false;
    }
  };

  const deletarItem = async (id: number, items: Ref<any[]>) => {
    if (!confirm("Tem certeza que deseja deletar este item?")) return false;

    try {
      await api.delete(`${endpoint}${id}/`);
      alertStore.addAlert("Item deletado com sucesso!", "success");
      await carregarItens(items);
      return true;
    } catch (error: any) {
      const mensagem = error.response?.data?.detail || "Erro ao deletar item";
      alertStore.addAlert(mensagem, "error");
      return false;
    }
  };

  return {
    carregarItens,
    salvarItem,
    deletarItem,
  };
}
