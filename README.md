# 🍔 LancheDash

API para sistema de gestão e delivery de lanches desenvolvida com FastAPI.

## 📋 Descrição

O **LancheDash** é um sistema de gerenciamento interno completo para lanchonetes. Ele permite o controle total desde o cadastro de cardápio e usuários até o fluxo de caixa diário, controle de estoque automatizado e relatórios gerenciais avançados.

---

## 🛠️ Tecnologias

- **Python** 3.13+
- **FastAPI** (Web Framework)
- **SQLAlchemy** (ORM / Banco de Dados SQLite)
- **Bcrypt** (Segurança e Hash de Senhas)
- **JWT (python-jose)** (Autenticação Segura)
- **python-dotenv** (Gestão de Variáveis de Ambiente)

---

## 📦 Instalação e Setup

### 1. Preparar o Ambiente
```bash
git clone https://github.com/FranciscoBatista83/lanchedash.git
cd lanchedash
python -m venv venv
source venv/Scripts/activate  # Windows
pip install -r requirements.txt
```

### 2. Configurar Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto baseado no `.env.example`:
```env
SECRET_KEY=sua_chave_secreta_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## ▶️ Execução

Para iniciar o servidor de desenvolvimento:
```bash
uvicorn app.main:app --reload
```
Acesse a documentação interativa em: **http://localhost:8000/docs**

---

## 🔐 Perfis de Acesso

O sistema utiliza **JWT para Autenticação** e possui dois níveis de permissão:

- **CAIXA**: 
  - Abrir/Fechar Caixa.
  - Lançar Pedidos, adicionar/remover itens e finalizar vendas.
  - Consultar cardápio e histórico básico.
- **ADMINISTRADOR**:
  - Tudo o que o Caixa faz.
  - CRUD completo de Produtos e Usuários.
  - Reabrir ou Cancelar pedidos já finalizados.
  - Ajustar estoque manualmente.
  - **Acesso total aos Relatórios Gerenciais.**

---

## 🛣️ Módulos Principais (Endpoints)

### 🔑 Autenticação
- `POST /auth/login`: Obtém o Token de acesso.

### 🍔 Cardápio (Produtos)
- `GET /produtos`: Lista itens ativos.
- `POST/PUT/DELETE /produtos`: Gestão do cardápio (🔒 Admin).

### 🛒 Vendas & Pedidos
- `POST /pedidos`: Inicia uma venda.
- `POST/DELETE /pedidos/.../itens`: Gerencia itens no carrinho (Baixa auto. de estoque).
- `POST /pedidos/.../finalizar`: Fecha a conta e registra o pagamento.

### 💰 Fluxo de Caixa
- `POST /caixa/abrir`: Inicia o dia com fundo de troco.
- `POST /caixa/sangria`: Retirada de valores da gaveta.
- `POST /caixa/fechar`: Encerra o dia com cálculo de divergências.

### 📦 Estoque
- `GET /estoque/alertas`: Lista produtos abaixo do mínimo.
- `POST /estoque/ajuste`: Correção manual (🔒 Admin).

### 📊 Relatórios (🔒 Admin)
- `/relatorios/dashboard`: Resumo do faturamento diário.
- `/relatorios/produtos`: Ranking de mais vendidos.
- `/relatorios/financeiro`: Totais por forma de pagamento (Pix, Cartão, Dinheiro).

---

## 📁 Estrutura do Projeto

```text
app/
├── core/       # Segurança e Dependências
├── models/     # Tabelas SQL (SQLAlchemy)
├── schemas/    # Validação e Serialização (Pydantic)
├── services/   # Lógica de Negócio (CRUDs, Cálculos)
├── routes/     # Endpoints da API
└── main.py     # Ponto de entrada
```

## 👤 Autor

Francisco Batista - [GitHub](https://github.com/FranciscoBatista83)
