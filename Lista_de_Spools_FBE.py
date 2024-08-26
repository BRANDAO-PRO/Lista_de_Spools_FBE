from pathlib import Path

import streamlit as st
import pandas as pd

def formatar_porcentagem(val):
    return f"{val * 100:.2f}%"

# Atualizando o caminho para o arquivo
pasta_FBE = Path('C:/Users/tiago.francisco/Desktop/FBE/Lista_de_Spools_FBE')

# Adicionando um try-except para lidar com erros de arquivo não encontrado
try:
    df_Lista_de_Spools_FBE = pd.read_excel(pasta_FBE / 'Lista_de_Spools_FBE.xlsx')
except FileNotFoundError:
    st.error("Arquivo 'Lista_de_Spools_FBE.xlsx' não encontrado no diretório especificado.")
    st.stop()

# Formatar as colunas de porcentagem
colunas_para_formatar = ['% no EBR/ID', '% Teste/ID', '% Lavagem/ID']
df_Lista_de_Spools_FBE[colunas_para_formatar] = df_Lista_de_Spools_FBE[colunas_para_formatar].applymap(formatar_porcentagem)

# Converter a coluna 'Teste' para apenas a data
df_Lista_de_Spools_FBE['Teste'] = pd.to_datetime(df_Lista_de_Spools_FBE['Teste']).dt.date

# Formatar a coluna 'Tag' para ter quatro dígitos
df_Lista_de_Spools_FBE['Tag'] = df_Lista_de_Spools_FBE['Tag'].astype(str).str.zfill(4)

colunas = list(df_Lista_de_Spools_FBE.columns)
colunas_selecionadas = st.sidebar.multiselect('Selecione as colunas:', colunas, colunas)

# Organizando os filtros um abaixo do outro
col_filtro = st.sidebar.selectbox('Selecione a coluna', [c for c in colunas if c not in ['id_venda']])
valor_filtro = st.sidebar.selectbox('Selecione o valor', list(df_Lista_de_Spools_FBE[col_filtro].unique()))

# Adicionando filtro para 'Localização'
localizacao_filtro = st.sidebar.selectbox('Selecione a Localização', list(df_Lista_de_Spools_FBE['Localização'].unique()))

status_limpar = st.sidebar.button('Limpar')

if status_limpar:
    st.dataframe(df_Lista_de_Spools_FBE[colunas_selecionadas], height=1000)
else:
    df_filtrado = df_Lista_de_Spools_FBE.loc[(df_Lista_de_Spools_FBE[col_filtro] == valor_filtro) & 
                                              (df_Lista_de_Spools_FBE['Localização'] == localizacao_filtro), 
                                              colunas_selecionadas]
    st.dataframe(df_filtrado, height=1000)
    st.sidebar.text('Powered By Brandão')
