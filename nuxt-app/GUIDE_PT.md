# Guia de Uso - Sistema de Gestão de Estoque (SGS)

## 🚀 Como Usar os CRUDs

### Autenticação
1. Acesse `/login`
2. Insira suas credenciais (username e password)
3. Será redirecionado para `/home`

### Navegação Principal
Use a barra de navegação no topo para acessar:
- **Movimentações** - Gerenciar entradas e saídas de estoque
- **Produtos** - Gerenciar catálogo de produtos
- **Categorias** - Gerenciar categorias de produtos
- **Usuários** - Gerenciar usuários do sistema

---

## 📦 MOVIMENTAÇÕES

### Criar Nova Movimentação
1. Clique no botão **"+ Nova Movimentação"**
2. Selecione o tipo (Entrada ou Saída)
3. Escolha a data
4. Adicione uma descrição (opcional)
5. Na seção "Itens da Movimentação":
   - Selecione um produto
   - Digite a quantidade
   - Digite o preço unitário
   - Clique em **"Adicionar"**
6. Repita para adicionar mais itens
7. Clique em **"Salvar"**

### Editar Movimentação
1. Localize a movimentação na tabela
2. Clique no botão **"Editar"**
3. Faça as alterações
4. Clique em **"Salvar"**

### Deletar Movimentação
1. Localize a movimentação na tabela
2. Clique no botão **"Deletar"**
3. Confirme a exclusão

---

## 📦 PRODUTOS

### Criar Novo Produto
1. Clique no botão **"+ Novo Produto"**
2. Preencha os campos:
   - **Nome** (obrigatório)
   - **Descrição** (opcional)
   - **Categoria** (obrigatório)
   - **Preço** (obrigatório)
3. Clique em **"Salvar"**

### Editar Produto
1. Localize o produto na tabela
2. Clique no botão **"Editar"**
3. Atualize os campos desejados
4. Clique em **"Salvar"**

### Deletar Produto
1. Localize o produto na tabela
2. Clique no botão **"Deletar"**
3. Confirme a exclusão

---

## 🏷️ CATEGORIAS

### Criar Nova Categoria
1. Clique no botão **"+ Nova Categoria"**
2. Preencha os campos:
   - **Nome** (obrigatório)
   - **Descrição** (obrigatório)
3. Clique em **"Salvar"**

### Editar Categoria
1. Localize a categoria na tabela
2. Clique no botão **"Editar"**
3. Atualize os campos
4. Clique em **"Salvar"**

### Deletar Categoria
1. Localize a categoria na tabela
2. Clique no botão **"Deletar"**
3. Confirme a exclusão

---

## 👥 USUÁRIOS

### Criar Novo Usuário
1. Clique no botão **"+ Novo Usuário"**
2. Preencha os campos obrigatórios:
   - **Username** (obrigatório)
   - **Email** (obrigatório)
   - **Nome** (obrigatório)
   - **Sobrenome** (obrigatório)
   - **Senha** (obrigatório)
3. Marque a opção **"Admin/Staff"** se necessário
4. Clique em **"Salvar"**

### Editar Usuário
1. Localize o usuário na tabela
2. Clique no botão **"Editar"**
3. Atualize os campos (senha é opcional ao editar)
4. Clique em **"Salvar"**

### Deletar Usuário
1. Localize o usuário na tabela
2. Clique no botão **"Deletar"**
3. Confirme a exclusão

---

## 👤 PERFIL

### Ver Perfil
1. Clique na imagem/ícone do usuário no canto superior direito
2. Selecione **"👤 Meu Perfil"**

### Editar Perfil
1. Na página de perfil, clique em **"Editar"**
2. Atualize os campos disponíveis
3. Clique em **"Salvar Alterações"**

### Logout
1. Clique na imagem/ícone do usuário no canto superior direito
2. Selecione **"🚪 Sair"**

---

## ⚠️ Mensagens e Notificações

### Alertas de Sucesso (Verde)
Aparecem no canto superior direito quando:
- Um item é criado com sucesso
- Um item é atualizado com sucesso
- Um item é deletado com sucesso

### Alertas de Erro (Vermelho)
Aparecem quando:
- Validação de campos falha
- Erro de conexão com o servidor
- Dados inválidos são enviados

Os alertas desaparecem automaticamente após 5 segundos.

---

## 💡 Dicas de Uso

1. **Datas:** Use o formato de data do seu navegador (clique no ícone de calendário)
2. **Preços:** Insira valores numéricos com ponto (ex: 99.99)
3. **Campos Obrigatórios:** Marcados com asterisco (*)
4. **Tabelas:** Passe o mouse sobre as linhas para ver a mudança de cor
5. **Modal:** Clique fora do modal ou no ✕ para fechar

---

## 🔐 Segurança

- Tokens JWT são renovados automaticamente
- Sessão expira automaticamente
- Permissões são verificadas no backend
- Senhas não são exibidas em qualquer lugar

---

## 📱 Responsividade

O sistema é responsivo e funciona em:
- Desktop (1920x1080)
- Tablet (768px)
- Mobile (375px)

---

## ❓ Troubleshooting

### "Erro ao carregar dados"
- Verifique sua conexão com a internet
- Verifique se o backend está rodando
- Tente recarregar a página

### "Token inválido"
- Você foi desconectado
- Faça login novamente

### "Campo obrigatório"
- Preencha todos os campos marcados com *

### Dados não aparecem
- Aguarde o carregamento (ícone de "Carregando...")
- Tente recarregar a página
- Verifique se há dados cadastrados no sistema
