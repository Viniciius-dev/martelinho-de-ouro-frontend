# 🔧 Martelinho de Ouro - Sistema de Gestão Frontend

Um sistema moderno de gestão (Frontend) desenvolvido para oficinas mecânicas estilo "Martelinho de Ouro", focado em controle de estoque, registro de compras e vendas, e relatórios financeiros em tempo real.

Este projeto funciona em conjunto com uma API Java (Backend) para persistência segura dos dados.

## 🚀 Funcionalidades

*   **📊 Dashboard Interativo:** Visão geral de vendas do dia, mês e ano, além de alertas de baixo estoque.
*   **📦 Gestão de Estoque:** Cadastro e monitoramento de peças, controle por categorias e marcas.
*   **🛒 Registrar Compras (Entradas):** Alimentação do estoque com informações do fornecedor e nota fiscal.
*   **💰 Registrar Vendas (Saídas):** Saída de peças com baixa automática de estoque e controle de pagamento.
*   **📈 Relatórios Financeiros:** Geração de gráficos, análise de lucros (Receita vs Despesa) e rankings.
*   **⚙️ Área Administrativa:** Importação e exportação de planilhas de backup.

## 💻 Tecnologias Utilizadas

Este frontend foi construído utilizando as seguintes tecnologias:

*   **Python:** Linguagem base da aplicação.
*   **Streamlit:** Framework para criação de interfaces web interativas de forma rápida.
*   **Pandas:** Biblioteca poderosa para manipulação, leitura e estruturação de dados em formato de tabelas/planilhas.
*   **Plotly Express:** Geração de gráficos bonitos e interativos.
*   **Requests:** Integração (consumo de dados) com a API Backend (Java/Spring Boot).

## 🛠️ Como executar o projeto localmente

**1. Clone este repositório:**
```bash
git clone https://github.com/Viniciius-dev/martelinho-de-ouro-frontend.git
```

**2. Acesse a pasta do projeto:**
```bash
cd martelinho-de-ouro-frontend
```

**3. Crie e ative um ambiente virtual:**
*   No Windows:
    ```bash
    python -m venv .venv
    .\.venv\Scripts\activate
    ```
*   No Linux/Mac:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

**4. Instale as dependências:**
```bash
pip install -r requirements.txt
```

**5. Configure as Variáveis de Ambiente:**
Crie um arquivo `.env` na raiz do projeto contendo a URL da API conectada:
```env
API_URL=https://apiapplication-production.up.railway.app
ADMIN_USER=admin
ADMIN_PASS=suasenha
```

**6. Execute a aplicação:**
```bash
streamlit run app.py
```

## 👨‍💻 Desenvolvedor
Projeto desenvolvido para fins acadêmicos e apresentação de conclusão/automação.
