import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def carrega_dados(caminho):
    dados = pd.read_csv(caminho)
    return dados


def grafico_comparativo(dados_2019, dados_2020, causa, estado = 'BRASIL'):

    if estado == 'BRASIL':
        total_2019 = dados_2019.groupby(['tipo_doenca'])['total'].sum()
        total_2020 = dados_2020.groupby(['tipo_doenca'])['total'].sum()

        if causa != 'COVID':
            lista = [total_2019.loc[causa], total_2020.loc[causa]]
        else:
            lista = [0, total_2020.loc[causa]]

    else:
        total_uf_2019 = dados_2019.groupby(['uf', 'tipo_doenca'])['total'].sum()
        total_uf_2020 = dados_2020.groupby(['uf', 'tipo_doenca'])['total'].sum()

        if causa != 'COVID':
            lista = [total_uf_2019.loc[estado, causa], total_uf_2020.loc[estado, causa]]
        else:
            lista = [0, total_uf_2020.loc[estado, causa]]

    dados = pd.DataFrame({'Total' : lista,
                          'Ano' : [2019, 2020]})
    fig, ax = plt.subplots()
    ax = sns.barplot(x='Ano', y='Total', data=dados)
    ax.set_title(f'Número de óbitos por {causa} - {estado}')

    return fig

def main():

    obitos_2019 = carrega_dados('dados/obitos-2019.csv')
    obitos_2020 = carrega_dados('dados/obitos-2020.csv')

    tipo_doenca = obitos_2020['tipo_doenca'].unique()
    local = np.append(obitos_2020['uf'].unique(), 'BRASIL')

    st.title('Análise de Óbitos 2019-2020')
    st.markdown('Este trabanho analisa dados dos **óbitos 2019-2020**')

    opcao_1 = st.sidebar.selectbox('Selecione o tipo de doença', tipo_doenca)
    opcao_2 = st.sidebar.selectbox('Selecione o local', local)

    figura = grafico_comparativo(obitos_2019, obitos_2020, opcao_1, opcao_2)
    st.pyplot(figura)

    opcao_ano_df = st.sidebar.selectbox('Para visualizar determinada tabela, selecione o ano:', 
                                        ['Não visualizar', '2019', '2020'])
    if opcao_ano_df == '2019':
        st.dataframe(obitos_2019)
    elif opcao_ano_df == '2020':
        st.dataframe(obitos_2020)
    else:
        pass
    

if __name__ == '__main__':
    main()
