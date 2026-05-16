"""
Páginas do Streamlit — Martelinho de Ouro (Oficina Mecânica).
"""
import os
import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:8081")   ## apiapplication-production.up.railway.app
ADMIN_USER = os.getenv("ADMIN_USER", "admin")
ADMIN_PASS = os.getenv("ADMIN_PASS", "admin")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DADOS_DIR = os.path.join(BASE_DIR, "dados")
VENDAS_PATH = os.path.join(DADOS_DIR, "vendas.xlsx")
COMPRAS_PATH = os.path.join(DADOS_DIR, "compras.xlsx")
ESTOQUE_PATH = os.path.join(DADOS_DIR, "estoque_pecas.xlsx")


def _existe(path):
    return os.path.exists(path)


def _aviso():
    st.warning("⚠️ Dados não encontrados! Use **⚙️ Gerar Dados Exemplo** primeiro.")


def _ler(path):
    return pd.read_excel(path, engine="openpyxl")


def _salvar_peca_api(codigo, nome, categoria, marca, veiculos, custo, venda, margem, est_atual, est_minimo=10):
    codigo = codigo.strip() if codigo and codigo.strip() else "S/C"
    nome = nome.strip() if nome and nome.strip() else "Peça Desconhecida"
    try:
        url = f"{API_URL}/pecas"
        payload = {"codigo": codigo, "nome": nome, "categoria": categoria, "marca": marca, "veiculos": veiculos, "precoCusto": custo, "precoVenda": venda, "margem": margem, "estoqueAtual": est_atual, "estoqueMinimo": est_minimo}
        requests.post(url, json=payload, timeout=2)
    except: pass

def _salvar_venda_api(peca, cliente, veiculo, placa, qtd, preco_unit, total, pagamento, vendedor):
    peca = peca.strip() if peca and peca.strip() else "Peça Desconhecida"
    vendedor = vendedor.strip() if vendedor and vendedor.strip() else "Não informado"
    try:
        url = f"{API_URL}/vendas"
        agora = datetime.now()
        payload = {"data": agora.strftime("%d/%m/%Y"), "hora": agora.strftime("%H:%M"), "peca": peca, "cliente": cliente, "veiculo": veiculo, "placa": placa, "quantidade": qtd, "precoUnitario": preco_unit, "total": total, "formaPagamento": pagamento, "vendedor": vendedor, "status": "Concluída"}
        requests.post(url, json=payload, timeout=2)
    except: pass

def _salvar_compra_api(peca, fornecedor, qtd, preco_unit, total, nf):
    peca = peca.strip() if peca and peca.strip() else "Peça Desconhecida"
    try:
        url = f"{API_URL}/compras"
        agora = datetime.now()
        payload = {"data": agora.strftime("%d/%m/%Y"), "hora": agora.strftime("%H:%M"), "peca": peca, "fornecedor": fornecedor, "quantidade": qtd, "precoUnitario": preco_unit, "total": total, "notaFiscal": nf}
        requests.post(url, json=payload, timeout=2)
    except: pass

def _atualizar_estoque_api(nome, novo_estoque):
    try:
        url = f"{API_URL}/pecas/estoque?nome={nome}&novoEstoque={novo_estoque}"
        requests.put(url, timeout=2)
    except: pass

def _gerar_resumo_dados():
    resumo = []
    if _existe(ESTOQUE_PATH):
        try:
            estoque = _ler(ESTOQUE_PATH)
            resumo.append(f"Estoque: {len(estoque)} peças")
        except: pass
    if _existe(VENDAS_PATH):
        try:
            vendas = _ler(VENDAS_PATH)
            total = vendas[vendas["Status"] == "Concluída"]["Total"].sum()
            resumo.append(f"Vendas: R$ {total:.2f}")
        except: pass
    if _existe(COMPRAS_PATH):
        try:
            compras = _ler(COMPRAS_PATH)
            total = compras["Total"].sum()
            resumo.append(f"Compras: R$ {total:.2f}")
        except: pass
    return " | ".join(resumo) if resumo else "Sistema sem dados reais."

def _salvar_log_api(tipo_operacao, usuario):
    resumo = _gerar_resumo_dados()
    if not usuario or not usuario.strip():
        usuario = "Usuário Desconhecido"
    try:
        url = f"{API_URL}/logs"
        payload = {
            "tipoOperacao": tipo_operacao,
            "usuario": usuario.strip(),
            "resumoDados": resumo
        }
        requests.post(url, json=payload, timeout=2)
    except Exception as e:
        pass


# ═══════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════
def pagina_dashboard():
    st.header("📊 Dashboard — Martelinho de Ouro")
    if not _existe(VENDAS_PATH):
        _aviso(); return

    vendas = _ler(VENDAS_PATH)
    vendas["Data"] = pd.to_datetime(vendas["Data"], format="%d/%m/%Y", dayfirst=True)
    concluidas = vendas[vendas["Status"] == "Concluída"]

    hoje = pd.Timestamp.now().normalize()
    mes_atual = hoje.month
    ano_atual = hoje.year

    vendas_dia = concluidas[concluidas["Data"] == hoje]["Total"].sum()
    vendas_mes = concluidas[(concluidas["Data"].dt.month == mes_atual) &
                            (concluidas["Data"].dt.year == ano_atual)]["Total"].sum()
    vendas_ano = concluidas[concluidas["Data"].dt.year == ano_atual]["Total"].sum()

    # KPIs
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("💰 Vendas Hoje", f"R$ {vendas_dia:,.2f}")
    c2.metric("📅 Vendas do Mês", f"R$ {vendas_mes:,.2f}")
    c3.metric("📆 Vendas do Ano", f"R$ {vendas_ano:,.2f}")
    c4.metric("🔢 Total de Vendas", f"{len(concluidas)}")

    # Estoque baixo
    if _existe(ESTOQUE_PATH):
        estoque = _ler(ESTOQUE_PATH)
        baixo = estoque[estoque["Estoque Atual"] <= estoque["Estoque Mínimo"]]
        if not baixo.empty:
            st.error(f"🚨 **{len(baixo)} peça(s) com estoque baixo!**")
            st.dataframe(baixo[["Código", "Peça", "Estoque Atual", "Estoque Mínimo"]],
                         use_container_width=True, hide_index=True)

    # Gráfico vendas mensais
    st.subheader("📈 Vendas Mensais")
    concluidas = concluidas.copy()
    concluidas["Mes"] = concluidas["Data"].dt.to_period("M").astype(str)
    mensal = concluidas.groupby("Mes")["Total"].sum().reset_index()
    fig = px.area(mensal, x="Mes", y="Total", title="Evolução Mensal de Vendas",
                  markers=True, labels={"Total": "Receita (R$)", "Mes": "Mês"})
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    # Vendas por categoria
    col1, col2 = st.columns(2)
    with col1:
        cat = concluidas.groupby("Categoria")["Total"].sum().reset_index()
        fig2 = px.pie(cat, values="Total", names="Categoria", title="Vendas por Categoria", hole=0.4)
        fig2.update_layout(template="plotly_dark")
        st.plotly_chart(fig2, use_container_width=True)
    with col2:
        vend = concluidas.groupby("Vendedor")["Total"].sum().reset_index().sort_values("Total")
        fig3 = px.bar(vend, x="Total", y="Vendedor", orientation="h",
                      title="Vendas por Vendedor", text_auto=",.0f")
        fig3.update_layout(template="plotly_dark")
        st.plotly_chart(fig3, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════
# ESTOQUE
# ═══════════════════════════════════════════════════════════════════════════
def pagina_estoque():
    st.header("📦 Estoque de Peças")
    if not _existe(ESTOQUE_PATH):
        _aviso(); return

    estoque = _ler(ESTOQUE_PATH)

    # Filtros
    col1, col2 = st.columns(2)
    cats = ["Todas"] + sorted(estoque["Categoria"].unique().tolist())
    cat_sel = col1.selectbox("Categoria", cats)
    marcas = ["Todas"] + sorted(estoque["Marca"].unique().tolist())
    marca_sel = col2.selectbox("Marca", marcas)

    df = estoque.copy()
    if cat_sel != "Todas":
        df = df[df["Categoria"] == cat_sel]
    if marca_sel != "Todas":
        df = df[df["Marca"] == marca_sel]

    # Métricas
    c1, c2, c3 = st.columns(3)
    c1.metric("Total de Peças", len(df))
    c2.metric("Valor em Estoque", f"R$ {(df['Preço Custo'] * df['Estoque Atual']).sum():,.2f}")
    baixo = df[df["Estoque Atual"] <= df["Estoque Mínimo"]]
    c3.metric("⚠️ Estoque Baixo", len(baixo))

    st.dataframe(df, use_container_width=True, hide_index=True, height=400)

    # Cadastrar nova peça
    st.subheader("➕ Cadastrar Nova Peça")
    with st.form("form_peca"):
        cols = st.columns(3)
        codigo = cols[0].text_input("Código", placeholder="FLT-004")
        nome = cols[1].text_input("Nome da Peça", placeholder="Filtro de Cabine")
        categoria = cols[2].selectbox("Categoria",
            ["Filtros", "Freios", "Motor", "Suspensão", "Elétrica", "Lubrificantes", "Acessórios"])
        cols2 = st.columns(4)
        marca = cols2[0].text_input("Marca", placeholder="Bosch")
        custo = cols2[1].number_input("Preço Custo", min_value=0.0, format="%.2f")
        venda = cols2[2].number_input("Preço Venda", min_value=0.0, format="%.2f")
        est_atual = cols2[3].number_input("Estoque", min_value=0, value=10)
        
        cols3 = st.columns(2)
        veiculos = cols3[0].text_input("Veículos Compatíveis", placeholder="Gol, Onix, HB20")
        responsavel = cols3[1].text_input("Seu Nome (Responsável pelo cadastro)")

        if st.form_submit_button("✅ Cadastrar Peça", type="primary"):
            from utils.escrita import adicionar_linha
            margem = round(((venda - custo) / custo) * 100, 1) if custo > 0 else 0
            novo_id = len(estoque) + 1
            adicionar_linha(ESTOQUE_PATH,
                [novo_id, codigo, nome, categoria, marca, veiculos, custo, venda, margem, est_atual, 10])
            
            # Salva o log e espelha no MySQL (API Java)
            _salvar_log_api("CADASTRO_PECA", responsavel)
            _salvar_peca_api(codigo, nome, categoria, marca, veiculos, custo, venda, margem, est_atual)
            
            nome_resp = responsavel if responsavel else "Usuário"
            st.success(f"✅ Peça '{nome}' cadastrada por {nome_resp} (Excel + MySQL)!")
            st.rerun()


# ═══════════════════════════════════════════════════════════════════════════
# REGISTRAR COMPRA
# ═══════════════════════════════════════════════════════════════════════════
def pagina_compra():
    st.header("🛒 Registrar Compra de Peça")
    if not _existe(ESTOQUE_PATH):
        _aviso(); return

    estoque = _ler(ESTOQUE_PATH)
    os.makedirs(DADOS_DIR, exist_ok=True)

    with st.form("form_compra"):
        cols = st.columns(2)
        peca_sel = cols[0].selectbox("Peça", estoque["Peça"].tolist())
        fornecedor = cols[1].text_input("Fornecedor", placeholder="AutoPeças São Paulo")

        cols2 = st.columns(3)
        qtd = cols2[0].number_input("Quantidade", min_value=1, value=10)
        peca_info = estoque[estoque["Peça"] == peca_sel].iloc[0]
        preco = cols2[1].number_input("Preço Unitário", value=float(peca_info["Preço Custo"]), format="%.2f")
        nf = cols2[2].text_input("Nota Fiscal", placeholder="NF-12345")

        total = round(qtd * preco, 2)
        st.info(f"💰 **Total da compra: R$ {total:,.2f}**")

        if st.form_submit_button("✅ Registrar Compra", type="primary"):
            agora = datetime.now()
            # Salvar na planilha de compras
            if _existe(COMPRAS_PATH):
                df_compras = _ler(COMPRAS_PATH)
                novo_id = len(df_compras) + 1
            else:
                novo_id = 1

            from utils.escrita import adicionar_linha
            if not _existe(COMPRAS_PATH):
                from utils.escrita import criar_planilha_de_dataframe
                cols_compra = ["ID", "Data", "Hora", "Peça", "Código", "Categoria",
                               "Fornecedor", "Quantidade", "Preço Unitário", "Total", "Nota Fiscal"]
                criar_planilha_de_dataframe(pd.DataFrame(columns=cols_compra), COMPRAS_PATH, "Compras")

            adicionar_linha(COMPRAS_PATH, [
                novo_id, agora.strftime("%d/%m/%Y"), agora.strftime("%H:%M"),
                peca_sel, peca_info["Código"], peca_info["Categoria"],
                fornecedor, qtd, preco, total, nf
            ])

            # Atualizar estoque (+quantidade)
            from utils.escrita import atualizar_celula
            linha_estoque = estoque[estoque["Peça"] == peca_sel].index[0] + 2
            novo_estoque = int(peca_info["Estoque Atual"]) + qtd
            atualizar_celula(ESTOQUE_PATH, linha_estoque, 10, novo_estoque)

            # Espelha a compra no MySQL (API Java)
            _salvar_compra_api(peca_sel, fornecedor, qtd, preco, total, nf)
            _atualizar_estoque_api(peca_sel, novo_estoque)
            _salvar_log_api("REGISTRO_COMPRA", "Usuário")

            st.success(f"✅ Compra registrada (Excel + MySQL)! Estoque de '{peca_sel}' atualizado: {novo_estoque} unidades")
            st.toast("Compra registrada com sucesso!", icon="💳")

    # Últimas compras
    if _existe(COMPRAS_PATH):
        st.subheader("📋 Últimas Compras")
        st.dataframe(_ler(COMPRAS_PATH).tail(10), use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════════════════════════
# REGISTRAR VENDA
# ═══════════════════════════════════════════════════════════════════════════
def pagina_venda():
    st.header("💰 Registrar Venda")
    if not _existe(ESTOQUE_PATH):
        _aviso(); return

    estoque = _ler(ESTOQUE_PATH)
    disponiveis = estoque[estoque["Estoque Atual"] > 0]

    with st.form("form_venda"):
        cols = st.columns(2)
        peca_sel = cols[0].selectbox("Peça", disponiveis["Peça"].tolist())
        peca_info = disponiveis[disponiveis["Peça"] == peca_sel].iloc[0]
        cols[1].info(f"Em estoque: **{int(peca_info['Estoque Atual'])}** | Preço: **R$ {peca_info['Preço Venda']:,.2f}**")

        cols2 = st.columns(3)
        cliente = cols2[0].text_input("Cliente", placeholder="João Silva")
        veiculo = cols2[1].text_input("Veículo", placeholder="Gol G5 2018")
        placa = cols2[2].text_input("Placa", placeholder="ABC-1234")

        cols3 = st.columns(3)
        qtd = cols3[0].number_input("Quantidade", min_value=1, max_value=int(peca_info["Estoque Atual"]), value=1)
        pagamento = cols3[1].selectbox("Pagamento", ["PIX", "Cartão Crédito", "Cartão Débito", "Dinheiro", "Fiado"])
        vendedor = cols3[2].text_input("Vendedor", placeholder="Carlos")

        total = round(qtd * float(peca_info["Preço Venda"]), 2)
        st.success(f"💰 **Total da venda: R$ {total:,.2f}**")

        if st.form_submit_button("✅ Registrar Venda", type="primary"):
            agora = datetime.now()
            if _existe(VENDAS_PATH):
                df_vendas = _ler(VENDAS_PATH)
                novo_id = len(df_vendas) + 1
            else:
                novo_id = 1

            from utils.escrita import adicionar_linha
            if not _existe(VENDAS_PATH):
                from utils.escrita import criar_planilha_de_dataframe
                cols_venda = ["ID", "Data", "Hora", "Peça", "Código", "Categoria",
                              "Cliente", "Veículo", "Placa", "Quantidade",
                              "Preço Unitário", "Total", "Forma Pagamento", "Vendedor", "Status"]
                criar_planilha_de_dataframe(pd.DataFrame(columns=cols_venda), VENDAS_PATH, "Vendas")

            adicionar_linha(VENDAS_PATH, [
                novo_id, agora.strftime("%d/%m/%Y"), agora.strftime("%H:%M"),
                peca_sel, peca_info["Código"], peca_info["Categoria"],
                cliente, veiculo, placa, qtd,
                float(peca_info["Preço Venda"]), total, pagamento, vendedor, "Concluída"
            ])

            # Atualizar estoque (-quantidade)
            from utils.escrita import atualizar_celula
            linha_estoque = estoque[estoque["Peça"] == peca_sel].index[0] + 2
            novo_estoque = int(peca_info["Estoque Atual"]) - qtd
            atualizar_celula(ESTOQUE_PATH, linha_estoque, 10, novo_estoque)

            # Salva o log e espelha no MySQL (API Java)
            _salvar_log_api("REGISTRO_VENDA", vendedor)
            _salvar_venda_api(peca_sel, cliente, veiculo, placa, qtd, float(peca_info["Preço Venda"]), total, pagamento, vendedor)
            _atualizar_estoque_api(peca_sel, novo_estoque)

            nome_vend = vendedor if vendedor else "Usuário"
            st.success(f"✅ Venda registrada por {nome_vend} (Excel + MySQL)! Estoque de '{peca_sel}': {novo_estoque} unidades")
            st.toast("Venda finalizada com sucesso!", icon="💰")

    # Últimas vendas
    if _existe(VENDAS_PATH):
        st.subheader("📋 Últimas Vendas")
        st.dataframe(_ler(VENDAS_PATH).tail(10), use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════════════════════════
# RELATÓRIOS
# ═══════════════════════════════════════════════════════════════════════════
def pagina_relatorios():
    st.header("📈 Relatórios Financeiros")
    
    if not _existe(VENDAS_PATH):
        _aviso(); return

    vendas = _ler(VENDAS_PATH)
    vendas["Data"] = pd.to_datetime(vendas["Data"], format="%d/%m/%Y", dayfirst=True)
    vendas_concluidas = vendas[vendas["Status"] == "Concluída"]
    
    compras = pd.DataFrame()
    if _existe(COMPRAS_PATH):
        compras = _ler(COMPRAS_PATH)
        compras["Data"] = pd.to_datetime(compras["Data"], format="%d/%m/%Y", dayfirst=True)

    tab1, tab2, tab3, tab4 = st.tabs(["📅 Diário", "📆 Mensal", "📊 Anual", "🏆 Ranking Peças"])

    with tab1:
        data_sel = st.date_input("Selecione o dia", value=datetime.now())
        dia_vendas = vendas_concluidas[vendas_concluidas["Data"].dt.date == data_sel]
        
        c1, c2, c3 = st.columns(3)
        total_vendas_dia = dia_vendas['Total'].sum()
        c1.metric("💰 Entradas (Vendas)", f"R$ {total_vendas_dia:,.2f}")
        
        total_compras_dia = 0
        if not compras.empty:
            dia_compras = compras[compras["Data"].dt.date == data_sel]
            total_compras_dia = dia_compras['Total'].sum()
            c2.metric("💳 Saídas (Compras)", f"R$ {total_compras_dia:,.2f}", delta=f"-R$ {total_compras_dia:,.2f}", delta_color="inverse")
            
        c3.metric("⚖️ Saldo do Dia", f"R$ {(total_vendas_dia - total_compras_dia):,.2f}")
        
        if not dia_vendas.empty:
            st.markdown("#### 💰 Vendas do Dia")
            st.dataframe(dia_vendas, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhuma venda neste dia.")

        st.markdown("---")
        
        if total_compras_dia > 0 and 'dia_compras' in locals() and not dia_compras.empty:
            st.markdown("#### 💳 Compras do Dia (Entrada de Peças)")
            st.dataframe(dia_compras, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhuma compra de peças (abastecimento de estoque) neste dia.")

    with tab2:
        vendas_c = vendas_concluidas.copy()
        vendas_c["Mes"] = vendas_c["Data"].dt.to_period("M").astype(str)
        mensal = vendas_c.groupby("Mes").agg(Receita=("Total", "sum"), Vendas=("ID", "count")).reset_index()
        
        if not compras.empty:
            compras_c = compras.copy()
            compras_c["Mes"] = compras_c["Data"].dt.to_period("M").astype(str)
            compras_mensal = compras_c.groupby("Mes").agg(Despesas=("Total", "sum")).reset_index()
            mensal = pd.merge(mensal, compras_mensal, on="Mes", how="outer").fillna(0)
            mensal["Lucro"] = mensal["Receita"] - mensal["Despesas"]
            
        st.dataframe(mensal, use_container_width=True, hide_index=True)
        
        # Gráfico
        fig = px.bar(mensal, x="Mes", y=["Receita", "Despesas"] if "Despesas" in mensal else "Receita", 
                     barmode="group", title="Receitas vs Despesas (Mensal)")
        fig.update_layout(template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        vendas_c2 = vendas_concluidas.copy()
        vendas_c2["Ano"] = vendas_c2["Data"].dt.year
        anual = vendas_c2.groupby("Ano").agg(Receita=("Total", "sum")).reset_index()
        
        if not compras.empty:
            compras_c2 = compras.copy()
            compras_c2["Ano"] = compras_c2["Data"].dt.year
            compras_anual = compras_c2.groupby("Ano").agg(Despesas=("Total", "sum")).reset_index()
            anual = pd.merge(anual, compras_anual, on="Ano", how="outer").fillna(0)
            anual["Lucro"] = anual["Receita"] - anual["Despesas"]

        st.dataframe(anual, use_container_width=True, hide_index=True)
        fig = px.bar(anual, x="Ano", y=["Receita", "Despesas"] if "Despesas" in anual else "Receita", 
                     barmode="group", title="Receitas vs Despesas (Anual)")
        fig.update_layout(template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    with tab4:
        ranking = vendas_concluidas.groupby("Peça").agg(
            Vendas=("ID", "count"), Receita=("Total", "sum"), Qtd_Total=("Quantidade", "sum")
        ).sort_values("Receita", ascending=False).reset_index()
        ranking.index = range(1, len(ranking) + 1)
        ranking.index.name = "Pos"
        st.dataframe(ranking, use_container_width=True)
        fig = px.bar(ranking.head(10), x="Peça", y="Receita", title="Top 10 Peças Mais Vendidas",
                     text_auto=",.0f", color="Peça")
        fig.update_layout(template="plotly_dark", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════
# GERAR DADOS EXEMPLO
# ═══════════════════════════════════════════════════════════════════════════
def pagina_gerar_dados():
    st.header("⚙️ Gerar Dados de Exemplo")
    st.markdown("Gera dados fictícios de peças, compras e vendas para testes do sistema.")
    
    st.warning("🔒 Área Restrita para Administradores")
    
    # Simples login no Streamlit
    if "logado" not in st.session_state:
        st.session_state["logado"] = False

    if not st.session_state["logado"]:
        with st.form("login_adm"):
            st.subheader("Login de Administrador")
            user = st.text_input("Usuário")
            senha = st.text_input("Senha", type="password")
            if st.form_submit_button("Entrar"):
                # Login fixo para teste: admin / admin
                if user == ADMIN_USER and senha == ADMIN_PASS:
                    st.session_state["logado"] = True
                    st.success("Login aprovado! Pode gerar os dados.")
                    st.rerun()
                else:
                    st.error("Usuário ou senha incorretos.")
        return

    # Se estiver logado, mostra as opções administrativas
    if st.button("🚪 Sair do Modo Admin"):
        st.session_state["logado"] = False
        st.rerun()
        
    st.markdown("---")
    tab1, tab2 = st.tabs(["📤 Importar Suas Planilhas", "📥 Ver e Exportar Dados Reais"])

    with tab1:
        st.markdown("Faça o upload de planilhas reais. **ATENÇÃO:** O arquivo deve seguir RIGOROSAMENTE o padrão de colunas do sistema.")
        
        col_up1, col_up2, col_up3 = st.columns(3)
        
        with col_up1:
            arq_estoque = st.file_uploader("Upload Estoque", type=["xlsx"], key="up_est")
            if arq_estoque and st.button("Salvar Estoque"):
                with open(ESTOQUE_PATH, "wb") as f:
                    f.write(arq_estoque.getbuffer())
                _salvar_log_api("IMPORTACAO_ESTOQUE", "admin")
                st.success("Estoque atualizado!")
                
        with col_up2:
            arq_compras = st.file_uploader("Upload Compras", type=["xlsx"], key="up_comp")
            if arq_compras and st.button("Salvar Compras"):
                with open(COMPRAS_PATH, "wb") as f:
                    f.write(arq_compras.getbuffer())
                _salvar_log_api("IMPORTACAO_COMPRAS", "admin")
                st.success("Compras atualizadas!")
                
        with col_up3:
            arq_vendas = st.file_uploader("Upload Vendas", type=["xlsx"], key="up_vend")
            if arq_vendas and st.button("Salvar Vendas"):
                with open(VENDAS_PATH, "wb") as f:
                    f.write(arq_vendas.getbuffer())
                _salvar_log_api("IMPORTACAO_VENDAS", "admin")
                st.success("Vendas atualizadas!")

    with tab2:
        st.markdown("Veja os dados atuais do sistema em tempo real e faça o download da planilha.")
        
        opcao_ver = st.selectbox("Selecione a Planilha", ["Estoque de Peças", "Compras", "Vendas"])
        hoje_str = datetime.now().strftime("%d-%m-%Y")
        
        caminho_alvo = None
        nome_arq = None
        
        if opcao_ver == "Estoque de Peças" and _existe(ESTOQUE_PATH):
            caminho_alvo = ESTOQUE_PATH
            nome_arq = f"estoque_pecas_{hoje_str}.xlsx"
        elif opcao_ver == "Compras" and _existe(COMPRAS_PATH):
            caminho_alvo = COMPRAS_PATH
            nome_arq = f"compras_{hoje_str}.xlsx"
        elif opcao_ver == "Vendas" and _existe(VENDAS_PATH):
            caminho_alvo = VENDAS_PATH
            nome_arq = f"vendas_{hoje_str}.xlsx"
            
        
        if caminho_alvo:
            # Mostra a planilha em tempo real
            st.dataframe(_ler(caminho_alvo), use_container_width=True, hide_index=True)
            
            st.markdown("---")
            nome_download = st.text_input("Seu Nome (Obrigatório para baixar)")
            
            if nome_download.strip():
                # Botão de download
                with open(caminho_alvo, "rb") as f:
                    st.download_button(
                        label=f"⬇️ Baixar Planilha de {opcao_ver}",
                        data=f,
                        file_name=nome_arq,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        type="primary",
                        on_click=_salvar_log_api,
                        args=("EXPORTACAO_PLANILHA", nome_download)
                    )
            else:
                st.warning("⚠️ Digite seu nome para liberar o download.")
        else:
            st.info("A planilha selecionada ainda não existe no sistema.")

# ═══════════════════════════════════════════════════════════════════════════
# HISTÓRICO DE LOGS (Auditoria)
# ═══════════════════════════════════════════════════════════════════════════
def pagina_historico_logs():
    st.header("📜 Histórico do Sistema (Logs e Auditoria)")
    st.markdown("Veja quem acessou o sistema e quais operações foram realizadas.")
    
    # Login igual ao do Admin
    if "logado" not in st.session_state:
        st.session_state["logado"] = False

    if not st.session_state["logado"]:
        st.warning("🔒 Área Restrita para Administradores")
        with st.form("login_logs"):
            user = st.text_input("Usuário Administrador")
            senha = st.text_input("Senha", type="password")
            if st.form_submit_button("Entrar"):
                if user == ADMIN_USER and senha == ADMIN_PASS:
                    st.session_state["logado"] = True
                    st.rerun()
                else:
                    st.error("Credenciais inválidas.")
        return
        
    if st.button("🚪 Sair do Modo Admin"):
        st.session_state["logado"] = False
        st.rerun()
        
    st.markdown("---")
    try:
        response = requests.get(f"{API_URL}/logs", timeout=3)
        if response.status_code == 200:
            logs = response.json()
            if logs:
                df = pd.DataFrame(logs)
                df["dataHora"] = pd.to_datetime(df["dataHora"]).dt.strftime("%d/%m/%Y %H:%M:%S")
                df = df[["id", "dataHora", "usuario", "tipoOperacao", "resumoDados"]]
                df = df.sort_values(by="id", ascending=False)
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("Nenhum log registrado ainda.")
        else:
            st.error("Erro na API ao carregar os logs.")
    except Exception as e:
        st.error(f"Erro ao conectar com o Banco de Dados (API Java): {e}")
