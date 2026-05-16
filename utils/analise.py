"""
Módulo de análise de dados de planilhas.
Filtros, agrupamentos, cálculos e rankings.
"""

import pandas as pd
from utils.leitura import ler_planilha


def filtrar_por_periodo(caminho: str, coluna_data: str,
                        data_inicio: str, data_fim: str) -> pd.DataFrame:
    """
    Filtra registros por período de datas.

    Args:
        caminho: Caminho do arquivo.
        coluna_data: Nome da coluna de data.
        data_inicio: Data inicial (dd/mm/yyyy).
        data_fim: Data final (dd/mm/yyyy).

    Returns:
        DataFrame filtrado.
    """
    df = ler_planilha(caminho)
    df[coluna_data] = pd.to_datetime(df[coluna_data], format="%d/%m/%Y", dayfirst=True)
    inicio = pd.to_datetime(data_inicio, format="%d/%m/%Y", dayfirst=True)
    fim = pd.to_datetime(data_fim, format="%d/%m/%Y", dayfirst=True)

    filtrado = df[(df[coluna_data] >= inicio) & (df[coluna_data] <= fim)]

    print(f"\n  📅 Período: {data_inicio} a {data_fim}")
    print(f"  📊 {len(filtrado)} registros encontrados de {len(df)} totais")

    return filtrado


def filtrar_por_valor(caminho: str, coluna: str, operador: str, valor) -> pd.DataFrame:
    """
    Filtra registros por valor numérico.

    Args:
        coluna: Nome da coluna.
        operador: '>', '<', '>=', '<=', '==', '!='
        valor: Valor para comparação.

    Returns:
        DataFrame filtrado.
    """
    df = ler_planilha(caminho)

    operadores = {
        ">": df[coluna] > valor,
        "<": df[coluna] < valor,
        ">=": df[coluna] >= valor,
        "<=": df[coluna] <= valor,
        "==": df[coluna] == valor,
        "!=": df[coluna] != valor,
    }

    if operador not in operadores:
        print(f"  ❌ Operador inválido: {operador}")
        return pd.DataFrame()

    filtrado = df[operadores[operador]]
    print(f"\n  🔎 Filtro: {coluna} {operador} {valor}")
    print(f"  📊 {len(filtrado)} registros encontrados")

    return filtrado


def agrupar_e_somar(caminho: str, coluna_grupo: str, coluna_valor: str) -> pd.DataFrame:
    """
    Agrupa dados e calcula soma, média, contagem, mín e máx.

    Args:
        coluna_grupo: Coluna para agrupar.
        coluna_valor: Coluna numérica para calcular.

    Returns:
        DataFrame com os agrupamentos.
    """
    df = ler_planilha(caminho)

    agrupado = df.groupby(coluna_grupo)[coluna_valor].agg(
        Total="sum",
        Media="mean",
        Contagem="count",
        Minimo="min",
        Maximo="max"
    ).round(2)

    agrupado = agrupado.sort_values("Total", ascending=False)

    print(f"\n  📊 Agrupamento por: {coluna_grupo} | Valor: {coluna_valor}")
    print("=" * 70)
    print(agrupado.to_string())
    print("=" * 70)

    return agrupado.reset_index()


def ranking_vendedores(caminho: str) -> pd.DataFrame:
    """Gera ranking dos vendedores por total de vendas."""
    df = ler_planilha(caminho)

    # Só vendas concluídas
    vendas = df[df["Status"] == "Concluida"]

    ranking = vendas.groupby("Vendedor").agg(
        Total_Vendas=("Total", "sum"),
        Qtd_Vendas=("ID", "count"),
        Ticket_Medio=("Total", "mean"),
    ).round(2)

    ranking = ranking.sort_values("Total_Vendas", ascending=False)
    ranking["Posicao"] = range(1, len(ranking) + 1)

    print("\n  🏆 RANKING DE VENDEDORES")
    print("=" * 70)
    for _, row in ranking.iterrows():
        pos = int(row["Posicao"])
        medalha = {1: "1.", 2: "2.", 3: "3."}.get(pos, f" {pos}.")
        print(f"  {medalha} {row.name:<20s} | R$ {row['Total_Vendas']:>12,.2f} | "
              f"{int(row['Qtd_Vendas']):>4d} vendas | Ticket: R$ {row['Ticket_Medio']:>10,.2f}")
    print("=" * 70)

    return ranking.reset_index()


def analise_por_categoria(caminho: str) -> pd.DataFrame:
    """Analisa vendas por categoria de produto."""
    df = ler_planilha(caminho)
    vendas = df[df["Status"] == "Concluida"]

    analise = vendas.groupby("Categoria").agg(
        Receita=("Total", "sum"),
        Quantidade=("Quantidade", "sum"),
        Num_Vendas=("ID", "count"),
        Ticket_Medio=("Total", "mean"),
    ).round(2)

    analise["% Receita"] = (analise["Receita"] / analise["Receita"].sum() * 100).round(1)
    analise = analise.sort_values("Receita", ascending=False)

    print("\n  📦 ANÁLISE POR CATEGORIA")
    print("=" * 80)
    for _, row in analise.iterrows():
        barra = "█" * int(row["% Receita"] / 2)
        print(f"  {row.name:<18s} | R$ {row['Receita']:>12,.2f} | "
              f"{row['% Receita']:>5.1f}% {barra}")
    print("=" * 80)

    return analise.reset_index()


def analise_por_regiao(caminho: str) -> pd.DataFrame:
    """Analisa vendas por região."""
    df = ler_planilha(caminho)
    vendas = df[df["Status"] == "Concluida"]

    analise = vendas.groupby("Regiao").agg(
        Receita=("Total", "sum"),
        Quantidade=("Quantidade", "sum"),
        Num_Vendas=("ID", "count"),
    ).round(2)

    analise["% Receita"] = (analise["Receita"] / analise["Receita"].sum() * 100).round(1)
    analise = analise.sort_values("Receita", ascending=False)

    print("\n  🗺️  ANÁLISE POR REGIÃO")
    print("=" * 70)
    for _, row in analise.iterrows():
        barra = "█" * int(row["% Receita"] / 2)
        print(f"  {row.name:<15s} | R$ {row['Receita']:>12,.2f} | "
              f"{row['% Receita']:>5.1f}% {barra}")
    print("=" * 70)

    return analise.reset_index()


def analise_mensal(caminho: str) -> pd.DataFrame:
    """Analisa vendas mês a mês com tendência."""
    df = ler_planilha(caminho)
    vendas = df[df["Status"] == "Concluida"].copy()
    vendas["Data"] = pd.to_datetime(vendas["Data"], format="%d/%m/%Y", dayfirst=True)
    vendas["Mes/Ano"] = vendas["Data"].dt.to_period("M")

    mensal = vendas.groupby("Mes/Ano").agg(
        Receita=("Total", "sum"),
        Num_Vendas=("ID", "count"),
    ).round(2)

    mensal["Ticket_Medio"] = (mensal["Receita"] / mensal["Num_Vendas"]).round(2)

    print("\n  📅 ANÁLISE MENSAL DE VENDAS")
    print("=" * 70)
    receita_anterior = None
    for periodo, row in mensal.iterrows():
        if receita_anterior is not None:
            variacao = ((row["Receita"] - receita_anterior) / receita_anterior * 100)
            seta = "📈" if variacao > 0 else "📉"
            var_str = f" {seta} {variacao:+.1f}%"
        else:
            var_str = ""
        print(f"  {str(periodo):<10s} | R$ {row['Receita']:>12,.2f} | "
              f"{int(row['Num_Vendas']):>4d} vendas{var_str}")
        receita_anterior = row["Receita"]
    print("=" * 70)

    return mensal.reset_index()
