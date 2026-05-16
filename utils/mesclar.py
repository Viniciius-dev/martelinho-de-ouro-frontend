"""
Módulo para mesclar e combinar planilhas Excel.
"""

import os
import pandas as pd
from utils.leitura import ler_planilha
from utils.escrita import criar_planilha_de_dataframe, adicionar_aba


def mesclar_planilhas_verticalmente(caminhos: list, caminho_saida: str,
                                      nome_aba: str = "Dados Mesclados") -> str:
    """Mescla várias planilhas empilhando os dados."""
    dfs = []
    for cam in caminhos:
        df = ler_planilha(cam)
        df["_Origem"] = os.path.basename(cam)
        dfs.append(df)
        print(f"  📄 {os.path.basename(cam)}: {len(df)} linhas")

    resultado = pd.concat(dfs, ignore_index=True)
    print(f"\n  📊 Total mesclado: {len(resultado)} linhas")
    criar_planilha_de_dataframe(resultado, caminho_saida, nome_aba)
    print(f"  ✅ Salvo em: {caminho_saida}")
    return caminho_saida


def mesclar_com_lookup(caminho_principal: str, caminho_referencia: str,
                        coluna_chave_principal: str, coluna_chave_referencia: str,
                        colunas_trazer: list, caminho_saida: str) -> str:
    """Faz um VLOOKUP/PROCV entre duas planilhas."""
    df_principal = ler_planilha(caminho_principal)
    df_referencia = ler_planilha(caminho_referencia)

    colunas_ref = [coluna_chave_referencia] + colunas_trazer
    df_ref_filtrado = df_referencia[colunas_ref]

    resultado = df_principal.merge(
        df_ref_filtrado, left_on=coluna_chave_principal,
        right_on=coluna_chave_referencia, how="left"
    )
    if coluna_chave_principal != coluna_chave_referencia:
        resultado = resultado.drop(columns=[coluna_chave_referencia])

    print(f"\n  🔗 Merge: {len(df_principal)} → {len(resultado)} linhas")
    print(f"     Colunas adicionadas: {', '.join(colunas_trazer)}")
    criar_planilha_de_dataframe(resultado, caminho_saida, "Dados Mesclados")
    return caminho_saida


def dividir_planilha_por_coluna(caminho: str, coluna: str, pasta_saida: str) -> list:
    """Divide uma planilha em vários arquivos por valores de uma coluna."""
    df = ler_planilha(caminho)
    os.makedirs(pasta_saida, exist_ok=True)
    valores = df[coluna].unique()
    arquivos = []

    print(f"\n  ✂️ Dividindo por '{coluna}' ({len(valores)} grupos):")
    for valor in sorted(valores):
        df_filtrado = df[df[coluna] == valor]
        nome_arquivo = f"{valor.replace(' ', '_').lower()}.xlsx"
        caminho_saida_arq = os.path.join(pasta_saida, nome_arquivo)
        criar_planilha_de_dataframe(df_filtrado, caminho_saida_arq, str(valor))
        arquivos.append(caminho_saida_arq)
        print(f"     📄 {nome_arquivo}: {len(df_filtrado)} linhas")

    print(f"\n  ✅ {len(arquivos)} arquivos gerados")
    return arquivos


def consolidar_em_abas(caminhos: list, caminho_saida: str) -> str:
    """Consolida vários arquivos em um único com múltiplas abas."""
    print(f"\n  📚 Consolidando {len(caminhos)} arquivo(s)...")
    primeiro = True
    for cam in caminhos:
        df = ler_planilha(cam)
        nome_aba = os.path.splitext(os.path.basename(cam))[0].capitalize()[:31]
        if primeiro:
            criar_planilha_de_dataframe(df, caminho_saida, nome_aba)
            primeiro = False
        else:
            adicionar_aba(caminho_saida, df, nome_aba)
        print(f"     📑 Aba '{nome_aba}': {len(df)} linhas")

    print(f"\n  ✅ Consolidado em: {caminho_saida}")
    return caminho_saida
