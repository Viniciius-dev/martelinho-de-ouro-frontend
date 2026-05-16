"""
╔══════════════════════════════════════════════════════════════════╗
║          🐍 AUTOMAÇÃO DE PLANILHAS COM PYTHON 🐍               ║
║                                                                  ║
║  Sistema completo para manipulação de planilhas Excel            ║
║  - Gerar dados de exemplo                                        ║
║  - Ler e inspecionar planilhas                                   ║
║  - Analisar dados (filtros, agrupamentos, rankings)              ║
║  - Gerar gráficos profissionais                                  ║
║  - Mesclar e dividir planilhas                                   ║
║  - Gerar relatórios executivos                                   ║
╚══════════════════════════════════════════════════════════════════╝
"""

import os
import sys

# Forçar encoding UTF-8 no console do Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# Diretórios do projeto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DADOS_DIR = os.path.join(BASE_DIR, "dados")
GRAFICOS_DIR = os.path.join(BASE_DIR, "graficos")
RELATORIOS_DIR = os.path.join(BASE_DIR, "relatorios")

VENDAS_PATH = os.path.join(DADOS_DIR, "vendas.xlsx")
PRODUTOS_PATH = os.path.join(DADOS_DIR, "produtos.xlsx")
VENDEDORES_PATH = os.path.join(DADOS_DIR, "vendedores.xlsx")


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    input("\n  ⏎ Pressione ENTER para continuar...")


def banner():
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║       🐍  AUTOMAÇÃO DE PLANILHAS COM PYTHON  🐍            ║
    ╚══════════════════════════════════════════════════════════════╝
    """)


def menu_principal():
    print("""
    ┌──────────────────────────────────────────┐
    │            📋 MENU PRINCIPAL             │
    ├──────────────────────────────────────────┤
    │  1. 📦 Gerar planilhas de exemplo        │
    │  2. 🔍 Ler e inspecionar planilha        │
    │  3. 📊 Análise de dados                  │
    │  4. 🎨 Gerar gráficos                    │
    │  5. 🔗 Mesclar / Dividir planilhas       │
    │  6. 📄 Gerar relatório completo          │
    │  7. ✏️  Editar planilha                   │
    │  0. 🚪 Sair                              │
    └──────────────────────────────────────────┘
    """)


def verificar_dados():
    """Verifica se as planilhas de exemplo existem."""
    if not os.path.exists(VENDAS_PATH):
        print("  ⚠️  Planilhas de exemplo não encontradas!")
        print("  💡 Use a opção 1 para gerar os dados primeiro.\n")
        return False
    return True


# ═══════════════════════════════════════════════════════════════════
# OPÇÃO 1: GERAR DADOS
# ═══════════════════════════════════════════════════════════════════
def opcao_gerar_dados():
    from utils.gerar_dados import gerar_todas_planilhas

    print("\n  📦 GERAR PLANILHAS DE EXEMPLO")
    print("  " + "─" * 40)

    qtd = input("  Quantos registros de vendas? (padrão: 200): ").strip()
    qtd = int(qtd) if qtd.isdigit() else 200

    print(f"\n  ⏳ Gerando {qtd} registros de vendas...")

    # Re-import to pass quantity
    from utils.gerar_dados import (
        gerar_planilha_vendas, gerar_planilha_produtos, gerar_planilha_vendedores
    )
    os.makedirs(DADOS_DIR, exist_ok=True)
    gerar_planilha_vendas(DADOS_DIR, qtd)
    gerar_planilha_produtos(DADOS_DIR)
    gerar_planilha_vendedores(DADOS_DIR)

    print(f"\n  ✅ Planilhas geradas na pasta: {DADOS_DIR}")
    print(f"     📄 vendas.xlsx ({qtd} registros)")
    print(f"     📄 produtos.xlsx (15 produtos)")
    print(f"     📄 vendedores.xlsx (8 vendedores)")


# ═══════════════════════════════════════════════════════════════════
# OPÇÃO 2: LER / INSPECIONAR
# ═══════════════════════════════════════════════════════════════════
def opcao_ler_planilha():
    from utils.leitura import resumo_planilha, buscar_registros, listar_abas

    if not verificar_dados():
        return

    print("\n  🔍 LER E INSPECIONAR PLANILHA")
    print("  " + "─" * 40)
    print("  1. Vendas")
    print("  2. Produtos")
    print("  3. Vendedores")
    print("  4. Outro arquivo (digitar caminho)")

    escolha = input("\n  Escolha: ").strip()

    caminhos = {"1": VENDAS_PATH, "2": PRODUTOS_PATH, "3": VENDEDORES_PATH}

    if escolha in caminhos:
        caminho = caminhos[escolha]
    elif escolha == "4":
        caminho = input("  Caminho do arquivo: ").strip()
    else:
        print("  ❌ Opção inválida.")
        return

    if not os.path.exists(caminho):
        print(f"  ❌ Arquivo não encontrado: {caminho}")
        return

    print("\n  a) Resumo completo")
    print("  b) Buscar registro")

    sub = input("\n  Escolha: ").strip().lower()

    if sub == "a":
        resumo_planilha(caminho)
    elif sub == "b":
        col = input("  Nome da coluna: ").strip()
        val = input("  Valor a buscar: ").strip()
        buscar_registros(caminho, col, val)


# ═══════════════════════════════════════════════════════════════════
# OPÇÃO 3: ANÁLISE
# ═══════════════════════════════════════════════════════════════════
def opcao_analise():
    from utils.analise import (
        ranking_vendedores, analise_por_categoria,
        analise_por_regiao, analise_mensal,
        agrupar_e_somar, filtrar_por_periodo
    )

    if not verificar_dados():
        return

    print("\n  📊 ANÁLISE DE DADOS")
    print("  " + "─" * 40)
    print("  1. 🏆 Ranking de vendedores")
    print("  2. 📦 Análise por categoria")
    print("  3. 🗺️  Análise por região")
    print("  4. 📅 Análise mensal")
    print("  5. 📊 Agrupar e somar (personalizado)")
    print("  6. 📅 Filtrar por período")
    print("  7. 🔄 Todas as análises")

    escolha = input("\n  Escolha: ").strip()

    if escolha == "1":
        ranking_vendedores(VENDAS_PATH)
    elif escolha == "2":
        analise_por_categoria(VENDAS_PATH)
    elif escolha == "3":
        analise_por_regiao(VENDAS_PATH)
    elif escolha == "4":
        analise_mensal(VENDAS_PATH)
    elif escolha == "5":
        col_grupo = input("  Coluna para agrupar: ").strip()
        col_valor = input("  Coluna numérica: ").strip()
        agrupar_e_somar(VENDAS_PATH, col_grupo, col_valor)
    elif escolha == "6":
        inicio = input("  Data início (dd/mm/yyyy): ").strip()
        fim = input("  Data fim (dd/mm/yyyy): ").strip()
        resultado = filtrar_por_periodo(VENDAS_PATH, "Data", inicio, fim)
        if not resultado.empty:
            print(resultado.head(20).to_string(index=False))
    elif escolha == "7":
        ranking_vendedores(VENDAS_PATH)
        analise_por_categoria(VENDAS_PATH)
        analise_por_regiao(VENDAS_PATH)
        analise_mensal(VENDAS_PATH)
    else:
        print("  ❌ Opção inválida.")


# ═══════════════════════════════════════════════════════════════════
# OPÇÃO 4: GRÁFICOS
# ═══════════════════════════════════════════════════════════════════
def opcao_graficos():
    from utils.graficos import (
        grafico_vendas_por_categoria, grafico_vendas_mensal,
        grafico_ranking_vendedores, grafico_pizza_regiao,
        grafico_status_vendas, grafico_forma_pagamento,
        gerar_todos_graficos
    )

    if not verificar_dados():
        return

    print("\n  🎨 GERAR GRÁFICOS")
    print("  " + "─" * 40)
    print("  1. 📊 Vendas por categoria")
    print("  2. 📈 Evolução mensal")
    print("  3. 🏆 Ranking vendedores")
    print("  4. 🗺️  Pizza por região")
    print("  5. 📋 Status das vendas")
    print("  6. 💳 Formas de pagamento")
    print("  7. 🎉 TODOS os gráficos")

    escolha = input("\n  Escolha: ").strip()

    funcoes = {
        "1": grafico_vendas_por_categoria,
        "2": grafico_vendas_mensal,
        "3": grafico_ranking_vendedores,
        "4": grafico_pizza_regiao,
        "5": grafico_status_vendas,
        "6": grafico_forma_pagamento,
    }

    if escolha in funcoes:
        funcoes[escolha](VENDAS_PATH, GRAFICOS_DIR)
    elif escolha == "7":
        gerar_todos_graficos(VENDAS_PATH, GRAFICOS_DIR)
    else:
        print("  ❌ Opção inválida.")


# ═══════════════════════════════════════════════════════════════════
# OPÇÃO 5: MESCLAR / DIVIDIR
# ═══════════════════════════════════════════════════════════════════
def opcao_mesclar():
    from utils.mesclar import (
        mesclar_com_lookup, dividir_planilha_por_coluna, consolidar_em_abas
    )

    if not verificar_dados():
        return

    print("\n  🔗 MESCLAR / DIVIDIR PLANILHAS")
    print("  " + "─" * 40)
    print("  1. 🔗 PROCV - Trazer dados de outra planilha")
    print("  2. ✂️  Dividir planilha por coluna")
    print("  3. 📚 Consolidar arquivos em abas")

    escolha = input("\n  Escolha: ").strip()

    if escolha == "1":
        saida = os.path.join(DADOS_DIR, "vendas_com_meta.xlsx")
        mesclar_com_lookup(
            VENDAS_PATH, VENDEDORES_PATH,
            "Vendedor", "Nome",
            ["Meta Mensal", "Comissao %"],
            saida
        )
        print(f"\n  ✅ Resultado: {saida}")

    elif escolha == "2":
        col = input("  Coluna para dividir (ex: Região, Categoria): ").strip()
        pasta = os.path.join(DADOS_DIR, f"dividido_por_{col.lower()}")
        dividir_planilha_por_coluna(VENDAS_PATH, col, pasta)

    elif escolha == "3":
        saida = os.path.join(DADOS_DIR, "consolidado.xlsx")
        consolidar_em_abas(
            [VENDAS_PATH, PRODUTOS_PATH, VENDEDORES_PATH],
            saida
        )
    else:
        print("  ❌ Opção inválida.")


# ═══════════════════════════════════════════════════════════════════
# OPÇÃO 6: RELATÓRIO
# ═══════════════════════════════════════════════════════════════════
def opcao_relatorio():
    from utils.relatorios import gerar_relatorio_completo

    if not verificar_dados():
        return

    print("\n  📄 GERAR RELATÓRIO COMPLETO")
    print("  " + "─" * 40)
    print("  Gerando relatório executivo com gráficos embutidos...\n")

    gerar_relatorio_completo(VENDAS_PATH, RELATORIOS_DIR)


# ═══════════════════════════════════════════════════════════════════
# OPÇÃO 7: EDITAR
# ═══════════════════════════════════════════════════════════════════
def opcao_editar():
    from utils.escrita import adicionar_linha, atualizar_celula
    from utils.leitura import resumo_planilha

    if not verificar_dados():
        return

    print("\n  ✏️  EDITAR PLANILHA")
    print("  " + "─" * 40)
    print("  1. Adicionar linha")
    print("  2. Atualizar célula")

    escolha = input("\n  Escolha: ").strip()

    if escolha == "1":
        print("\n  Colunas de vendas: ID, Data, Produto, Categoria, Quantidade,")
        print("  Preço Unitário, Total, Vendedor, Região, Forma Pagamento, Status\n")

        dados = input("  Digite os valores separados por vírgula:\n  > ").strip()
        valores = [v.strip() for v in dados.split(",")]

        # Converter numéricos
        for i in [0, 4]:
            if i < len(valores):
                try:
                    valores[i] = int(valores[i])
                except ValueError:
                    pass
        for i in [5, 6]:
            if i < len(valores):
                try:
                    valores[i] = float(valores[i])
                except ValueError:
                    pass

        adicionar_linha(VENDAS_PATH, valores)
        print("  ✅ Linha adicionada com sucesso!")

    elif escolha == "2":
        linha = int(input("  Número da linha: ").strip())
        coluna = int(input("  Número da coluna: ").strip())
        valor = input("  Novo valor: ").strip()

        try:
            valor = float(valor)
        except ValueError:
            pass

        atualizar_celula(VENDAS_PATH, linha, coluna, valor)
        print(f"  ✅ Célula ({linha}, {coluna}) atualizada!")

    else:
        print("  ❌ Opção inválida.")


# ═══════════════════════════════════════════════════════════════════
# LOOP PRINCIPAL
# ═══════════════════════════════════════════════════════════════════
def main():
    while True:
        limpar_tela()
        banner()
        menu_principal()

        opcao = input("  👉 Escolha uma opção: ").strip()

        if opcao == "1":
            opcao_gerar_dados()
        elif opcao == "2":
            opcao_ler_planilha()
        elif opcao == "3":
            opcao_analise()
        elif opcao == "4":
            opcao_graficos()
        elif opcao == "5":
            opcao_mesclar()
        elif opcao == "6":
            opcao_relatorio()
        elif opcao == "7":
            opcao_editar()
        elif opcao == "0":
            print("\n  👋 Até logo! Bom trabalho com as planilhas!\n")
            sys.exit(0)
        else:
            print("  ❌ Opção inválida. Tente novamente.")

        pausar()


if __name__ == "__main__":
    main()
