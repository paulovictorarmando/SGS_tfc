# Documentação de CRUDs - SGS

## Páginas Implementadas

### 1. **Movimentações** (`/movimentos`)
- ✅ Listar movimentações (Entrada/Saída)
- ✅ Criar nova movimentação com múltiplos itens
- ✅ Editar movimentação
- ✅ Deletar movimentação
- **Funcionalidades especiais:**
  - Suporte a múltiplos itens por movimentação
  - Sistema de adição/remoção dinâmica de itens
  - Cálculo automático de totais
  - Indicador visual de tipo (Entrada/Saída)

### 2. **Produtos** (`/produtos`)
- ✅ Listar produtos com categoria e preço
- ✅ Criar novo produto
- ✅ Editar produto existente
- ✅ Deletar produto
- **Funcionalidades especiais:**
  - Associação com categorias
  - Formatação de preços em BRL
  - Validação de campos obrigatórios

### 3. **Categorias** (`/categorias`)
- ✅ Listar categorias
- ✅ Criar nova categoria
- ✅ Editar categoria
- ✅ Deletar categoria
- **Funcionalidades especiais:**
  - Suporte a descrição
  - Interface minimalista

### 4. **Usuários** (`/usuarios`)
- ✅ Listar usuários
- ✅ Criar novo usuário
- ✅ Editar usuário
- ✅ Deletar usuário
- **Funcionalidades especiais:**
  - Gestão de senha (obrigatória na criação, opcional na edição)
  - Sistema de permissões (Admin/Staff)
  - Validação de email

### 5. **Home** (`/home`)
- ✅ Dashboard com estatísticas
- ✅ Contadores de movimentações, produtos, categorias e usuários
- ✅ Links diretos para cada página

### 6. **Perfil** (`/perfil`)
- ✅ Visualizar dados do usuário
- ✅ Editar perfil pessoal
- ✅ Nome de usuário em apenas leitura

## Componentes de Interface

### AlertContainer
- Exibe alertas de sucesso/erro
- Auto-remove após 5 segundos
- Posicionado no canto superior direito

### Header
- Navegação principal
- Links para: Movimentações, Produtos, Categorias, Usuários
- Menu de perfil e logout

### Aside (disponível para uso futuro)
### Main (disponível para uso futuro)

## Estilos

- **Framework:** Tailwind CSS + DaisyUI
- **Responsividade:** Mobile-first
- **Cores:**
  - Primária: Azul (#3b82f6)
  - Sucesso: Verde (#10b981)
  - Erro: Vermelho (#ef4444)
  - Neutro: Cinza (#6b7280)

## Funcionalidades Comuns

Todos os CRUDs incluem:
- ✅ Carregamento de dados ao montar
- ✅ Modal para criação/edição
- ✅ Validação de formulários
- ✅ Mensagens de erro
- ✅ Indicador de carregamento
- ✅ Confirmação antes de deletar
- ✅ Formatação de datas (pt-BR)
- ✅ Formatação de preços (BRL)

## API Endpoints Utilizados

- `POST /auth/login/` - Login de usuário
- `GET /movimentacoes/` - Listar movimentações
- `POST /movimentacoes/` - Criar movimentação
- `PUT /movimentacoes/{id}/` - Editar movimentação
- `DELETE /movimentacoes/{id}/` - Deletar movimentação
- `GET /produtos/` - Listar produtos
- `POST /produtos/` - Criar produto
- `PUT /produtos/{id}/` - Editar produto
- `DELETE /produtos/{id}/` - Deletar produto
- `GET /categorias/` - Listar categorias
- `POST /categorias/` - Criar categoria
- `PUT /categorias/{id}/` - Editar categoria
- `DELETE /categorias/{id}/` - Deletar categoria
- `GET /usuarios/` - Listar usuários
- `POST /usuarios/` - Criar usuário
- `PUT /usuarios/{id}/` - Editar usuário
- `DELETE /usuarios/{id}/` - Deletar usuário
- `GET /usuarios/me/` - Dados do usuário atual
- `PUT /usuarios/me/` - Atualizar dados do usuário atual

## Middleware de Autenticação

Todas as páginas (exceto `/login`) utilizam o middleware `auth` para:
- Validar token JWT
- Redirecionar para login se não autenticado
- Renovar token automaticamente ao expirar

## Composables

### `api.ts`
- Instância Axios com interceptadores
- Renovação automática de token

### `auth.ts`
- `getAccessToken()` - Recuperar token de acesso
- `getRefreshToken()` - Recuperar token de refresh
- `setTokens()` - Salvar tokens
- `clearTokens()` - Limpar tokens

### `crud.ts` (Novo)
- `useCRUD()` - Composable reutilizável para operações CRUD comuns

## Stores

### `alerts.ts`
- Gerenciamento de alertas globais
- Auto-remover após 5 segundos
- Suporte a múltiplos tipos (success, error)

## Próximos Passos Recomendados

1. **Paginação** - Implementar paginação nas listas
2. **Filtros** - Adicionar filtros por categoria, tipo, etc.
3. **Busca** - Sistema de busca rápida
4. **Exportação** - Exportar dados em CSV/PDF
5. **Relatórios** - Gráficos e análises
6. **Validações** - Validações mais robustas no backend
7. **Testes** - Testes unitários e E2E
