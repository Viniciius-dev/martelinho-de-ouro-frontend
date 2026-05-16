"""
Módulo de geração de gráficos a partir de planilhas.
Cria gráficos profissionais com matplotlib.
"""

import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # Backend não-interativo
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

from utils.leitura import ler_planilha

# ── Configuração global de estilo ────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor": "#1a1a2e",
    "axes.facecolor": "#16213e",
    "axes.edgecolor": "#e0e0e0",
    "axes.labelcolor": "#e0e0e0",
    "text.color": "#e0e0e0",
    "xtick.color": "#e0e0e0",
    "ytick.color": "#e0e0e0",
    "font.family": "sans-serif",
    "font.size": 11,
    "axes.grid": True,
    "grid.alpha": 0.15,
    "grid.color": "#ffffff",
})

PALETA = ["#e94560", "#0f3460", "#533483", "#48c9b0", "#f39c12",
          "#3498db", "#e74c3c", "#2ecc71", "#9b59b6", "#1abc9c"]


def _salvar_grafico(fig, pasta, nome):
    """Salva o gráfico e exibe confirmação."""
    os.makedirs(pasta, exist_ok=True)
    caminho = os.path.join(pasta, f"{nome}.png")
    fig.savefig(caminho, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  ✅ Gráfico salvo: {caminho}")
    return caminho


def grafico_vendas_por_categoria(caminho_dados: str, pasta_saida: str) -> str:
    """Gera gráfico de barras horizontais de vendas por categoria."""
    df = ler_planilha(caminho_dados)
    vendas = df[df["Status"] == "Concluida"]
    dados = vendas.groupby("Categoria")["Total"].sum().sort_values()

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.barh(dados.index, dados.values, color=PALETA[:len(dados)],
                   edgecolor="white", linewidth=0.5, height=0.6)

    # Valores nas barras
    for bar, valor in zip(bars, dados.values):
        ax.text(bar.get_width() + dados.max() * 0.01, bar.get_y() + bar.get_height() / 2,
                f"R$ {valor:,.0f}", va="center", fontsize=10, color="#e0e0e0")

    ax.set_title("💰 Vendas por Categoria", fontsize=16, fontweight="bold", pad=20)
    ax.set_xlabel("Receita Total (R$)")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"R$ {x:,.0f}"))

    return _salvar_grafico(fig, pasta_saida, "vendas_por_categoria")


def grafico_vendas_mensal(caminho_dados: str, pasta_saida: str) -> str:
    """Gera gráfico de linha de vendas mensais com área preenchida."""
    df = ler_planilha(caminho_dados)
    vendas = df[df["Status"] == "Concluida"].copy()
    vendas["Data"] = pd.to_datetime(vendas["Data"], format="%d/%m/%Y", dayfirst=True)
    vendas["Mês"] = vendas["Data"].dt.to_period("M")

    mensal = vendas.groupby("Mês")["Total"].sum()

    fig, ax = plt.subplots(figsize=(14, 6))

    x = range(len(mensal))
    ax.fill_between(x, mensal.values, alpha=0.3, color=PALETA[0])
    ax.plot(x, mensal.values, color=PALETA[0], linewidth=2.5, marker="o",
            markersize=8, markerfacecolor="white", markeredgecolor=PALETA[0], markeredgewidth=2)

    ax.set_xticks(x)
    ax.set_xticklabels([str(m) for m in mensal.index], rotation=45, ha="right")
    ax.set_title("📈 Evolução Mensal de Vendas", fontsize=16, fontweight="bold", pad=20)
    ax.set_ylabel("Receita (R$)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"R$ {x:,.0f}"))

    return _salvar_grafico(fig, pasta_saida, "vendas_mensal")


def grafico_ranking_vendedores(caminho_dados: str, pasta_saida: str) -> str:
    """Gera gráfico de barras do ranking de vendedores."""
    df = ler_planilha(caminho_dados)
    vendas = df[df["Status"] == "Concluida"]
    ranking = vendas.groupby("Vendedor")["Total"].sum().sort_values(ascending=True)

    fig, ax = plt.subplots(figsize=(12, 6))

    cores = [PALETA[i % len(PALETA)] for i in range(len(ranking))]
    bars = ax.barh(ranking.index, ranking.values, color=cores,
                   edgecolor="white", linewidth=0.5, height=0.6)

    for bar, valor in zip(bars, ranking.values):
        ax.text(bar.get_width() + ranking.max() * 0.01, bar.get_y() + bar.get_height() / 2,
                f"R$ {valor:,.0f}", va="center", fontsize=10, color="#e0e0e0")

    ax.set_title("🏆 Ranking de Vendedores", fontsize=16, fontweight="bold", pad=20)
    ax.set_xlabel("Receita Total (R$)")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"R$ {x:,.0f}"))

    return _salvar_grafico(fig, pasta_saida, "ranking_vendedores")


def grafico_pizza_regiao(caminho_dados: str, pasta_saida: str) -> str:
    """Gera gráfico de pizza de vendas por região."""
    df = ler_planilha(caminho_dados)
    vendas = df[df["Status"] == "Concluida"]
    dados = vendas.groupby("Regiao")["Total"].sum()

    fig, ax = plt.subplots(figsize=(10, 8))

    wedges, texts, autotexts = ax.pie(
        dados.values,
        labels=dados.index,
        autopct="%1.1f%%",
        colors=PALETA[:len(dados)],
        startangle=140,
        pctdistance=0.8,
        wedgeprops=dict(width=0.5, edgecolor="white", linewidth=2),
    )

    for text in autotexts:
        text.set_fontsize(11)
        text.set_fontweight("bold")

    ax.set_title("🗺️ Distribuição de Vendas por Região",
                 fontsize=16, fontweight="bold", pad=20)

    return _salvar_grafico(fig, pasta_saida, "vendas_por_regiao")


def grafico_status_vendas(caminho_dados: str, pasta_saida: str) -> str:
    """Gera gráfico de barras com o status das vendas."""
    df = ler_planilha(caminho_dados)
    dados = df["Status"].value_counts()

    cores_status = {"Concluida": "#2ecc71", "Pendente": "#f39c12", "Cancelada": "#e74c3c"}
    cores = [cores_status.get(s, PALETA[0]) for s in dados.index]

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(dados.index, dados.values, color=cores,
                  edgecolor="white", linewidth=1, width=0.5)

    for bar, valor in zip(bars, dados.values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                str(valor), ha="center", va="bottom", fontsize=14, fontweight="bold")

    ax.set_title("📊 Status das Vendas", fontsize=16, fontweight="bold", pad=20)
    ax.set_ylabel("Quantidade")

    return _salvar_grafico(fig, pasta_saida, "status_vendas")


def grafico_forma_pagamento(caminho_dados: str, pasta_saida: str) -> str:
    """Gera gráfico de barras por forma de pagamento."""
    df = ler_planilha(caminho_dados)
    vendas = df[df["Status"] == "Concluida"]
    dados = vendas.groupby("Forma Pagamento")["Total"].sum().sort_values(ascending=True)

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.barh(dados.index, dados.values, color=PALETA[:len(dados)],
                   edgecolor="white", linewidth=0.5, height=0.5)

    for bar, valor in zip(bars, dados.values):
        ax.text(bar.get_width() + dados.max() * 0.01, bar.get_y() + bar.get_height() / 2,
                f"R$ {valor:,.0f}", va="center", fontsize=10, color="#e0e0e0")

    ax.set_title("💳 Vendas por Forma de Pagamento", fontsize=16, fontweight="bold", pad=20)
    ax.set_xlabel("Receita Total (R$)")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"R$ {x:,.0f}"))

    return _salvar_grafico(fig, pasta_saida, "vendas_por_pagamento")


def gerar_todos_graficos(caminho_dados: str, pasta_saida: str) -> list:
    """Gera todos os gráficos disponíveis."""
    print("\n  🎨 Gerando todos os gráficos...\n")
    graficos = [
        grafico_vendas_por_categoria(caminho_dados, pasta_saida),
        grafico_vendas_mensal(caminho_dados, pasta_saida),
        grafico_ranking_vendedores(caminho_dados, pasta_saida),
        grafico_pizza_regiao(caminho_dados, pasta_saida),
        grafico_status_vendas(caminho_dados, pasta_saida),
        grafico_forma_pagamento(caminho_dados, pasta_saida),
    ]
    print(f"\n  🎉 {len(graficos)} gráficos gerados com sucesso!")
    return graficos
