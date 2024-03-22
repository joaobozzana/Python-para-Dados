import pandas as pd

df = pd.read_csv('credito.csv', na_values='na') # Posso por uma lista = na_values=['na', '', None]

# Analisando a estrutura 
qtd_total = df.shape[0]
print(qtd_total) 

qtd_adimplentes = df[df['default'] == 0].shape[0] # Sabendo a quantidade de adimplentes
print(qtd_adimplentes)
qtd_inadimplentes = df[df['default'] == 1].shape[0] # Sabendo a quantidade de inadimplentes 
print(qtd_inadimplentes)

print(f"A proporção de clientes adimplentes é de {round(100 * qtd_adimplentes / qtd_total, 2)}%")
print(f"A proporção de clientes inadimplentes é de {round(100 * qtd_inadimplentes / qtd_total, 2)}%")


print("-----------------------------------------------------------------------------------------------", end='\n\n')

# Analisando o Schema
analise_colunas = df.dtypes # Analisa o tipo de cada coluna
print(analise_colunas, end='\n\n')

atributos_categoricos = df.select_dtypes('object').describe().transpose()
print(atributos_categoricos, end='\n\n')

atributos_numericos = df.drop('id', axis=1).select_dtypes('number').describe().transpose()
print(atributos_numericos)


print("-----------------------------------------------------------------------------------------------", end='\n\n')

# Analisando os dados faltantes

print(df.isna().any(), end='\n\n')

def stas_dados_faltantes(df: pd.DataFrame) -> None:

    stas_dados_faltantes = []
    for col in df.columns:
        if df[col].isna().any():
            qtd = df[df[col].isna()].shape[0]
            total = df.shape[0]
            dict_dados_faltantes = {col: {'quantidade': qtd, 'porcentagem': round(100 * qtd / total, 2)}}
            stas_dados_faltantes.append(dict_dados_faltantes)
    
    for stat in stas_dados_faltantes:
        print(stat)

stas_dados_faltantes(df=df) #total
print("")
stas_dados_faltantes(df = df[df['default'] == 0]) # adimplentes
print("")
stas_dados_faltantes(df = df[df['default'] == 1]) # inadimplentes

print("-----------------------------------------------------------------------------------------------", end='\n\n')

# Transformação e limpeza dos dados

func = lambda valor: float(valor.replace(".", "").replace(",", "."))
df['valor_transacoes_12m'] = df['valor_transacoes_12m'].apply(func)
df['limite_credito'] = df['limite_credito'].apply(func)

print(df.select_dtypes('object').describe().transpose(), end='\n\n')
print(df.drop('id', axis=1).select_dtypes('number').describe().transpose(), end='\n\n')

df.dropna(inplace=True)

print(df.shape)
print(df[df['default'] == 0].shape)
print(df[df['default'] == 1].shape, end='\n\n')

# Comparando as proporções

qtd_total_atualizado = df.shape[0]
qtd_adimplentes_atualizado = df[df['default'] == 0].shape[0] # Sabendo a quantidade de adimplentes
qtd_inadimplentes_atualizado = df[df['default'] == 1].shape[0] # Sabendo a quantidade de inadimplentes 

print(f"A proporção de clientes adimplentes é de {round(100 * qtd_adimplentes / qtd_total, 2)}%")
print(f"A nova proporção de clientes inadimplentes é de {round(100 * qtd_adimplentes_atualizado / qtd_total_atualizado, 2)}%")
print("")
print(f"A proporção de clientes adimplentes é de {round(100 * qtd_inadimplentes / qtd_total, 2)}%")
print(f"A nova proporção de clientes inadimplentes é de {round(100 * qtd_inadimplentes_atualizado / qtd_total_atualizado, 2)}%")


print("-----------------------------------------------------------------------------------------------", end='\n\n')

# Visualização de dados

import seaborn as sns
import matplotlib.pyplot as plt

sns.set_style("whitegrid")

df_adimplente = df[df['default'] == 0]
df_inadimplente = df[df['default'] == 1]

#print(df.select_dtypes('object').head(n=5))

def gerador_de_grafico_categoricas(df, df_adimplente, df_inadimplente, coluna, titulos):
    figura, eixos = plt.subplots(1, 3, figsize=(15, 9), sharex=True)

    max_y = 0

    for eixo, dataframe in enumerate([df, df_adimplente, df_inadimplente]):
        df_to_plot = dataframe[coluna].value_counts().to_frame()
        df_to_plot[coluna] = df_to_plot.index
        df_to_plot.reset_index(drop=True, inplace=True)
        df_to_plot.sort_values(by=[coluna], inplace=True)

        f = sns.barplot(x=df_to_plot[coluna], y=df_to_plot["count"], ax=eixos[eixo])
        f.set(title=titulos[eixo], xlabel=coluna.capitalize(), ylabel='Quantidade de Clientes')
        
        # Define as posições dos ticks no eixo x
        f.set_xticks(range(len(df_to_plot[coluna])))
        f.set_xticklabels(labels=df_to_plot[coluna], rotation=90)

        _, max_y_f = f.get_ylim()
        max_y = max_y_f if max_y_f > max_y else max_y
        f.set(ylim=(0, max_y))

    figura.show()
    plt.show()


# Analisando algumas variaveis categóricas

'''
coluna = 'escolaridade'
titulos = [
    'Escolaridade dos Clientes',
    'Escolaridade dos Clientes Adimplentes',
    'Escolaridade dos Clientes Inadimplentes'
]

coluna = 'salario_anual'
titulos = [
    'Salario Anual dos Clientes',
    'Salario Anual dos Clientes Adimplentes',
    'Salario Anual dos Clientes Inadimplentes'
]

gerador_de_grafico_categoricas(df, df_adimplente, df_inadimplente, coluna, titulos)
'''

# print(df.drop(['id', 'default'], axis=1).select_dtypes('number').head(n=5))

def gerador_de_grafico_numericas(df, df_adimplente, df_inadimplente, coluna, titulos):
    figura, eixos = plt.subplots(1, 3, figsize=(15, 9), sharex=True)

    max_y = 0

    for eixo, dataframe in enumerate([df, df_adimplente, df_inadimplente]):

        f = sns.histplot(x=coluna, data=dataframe, stat='count', ax=eixos[eixo])
        f.set(
            title=titulos[eixo],
            xlabel=coluna.capitalize(),
            ylabel='Quantidade de Clientes'
        )

        _, max_y_f = f.get_ylim()
        max_y = max_y_f if max_y_f > max_y else max_y
        f.set(ylim=(0, max_y))

    figura.show()
    plt.show()

'''
coluna = 'qtd_transacoes_12m'
titulos = [
    'Qtd. de Transações no Último Ano',
    'Qtd. de Transações no Último Ano de Adimplentes',
    'Qtd. de Transações no Último Ano de Inadimplentes'
]


coluna = 'valor_transacoes_12m'
titulos = [
    'Valor das Transações no Último Ano',
    'Valor das Transações no Último Ano de Adimplentes',
    'Valor das Transações no Último Ano de Inadimplentes'
]

gerador_de_grafico_numericas(df, df_adimplente, df_inadimplente, coluna, titulos)
'''

f = sns.relplot(x='valor_transacoes_12m',y='qtd_transacoes_12m', data=df, hue='default')
_ = f.set(
    title='Relação entre Valor e Quantidade de Transações no Último Ano',
    xlabel='Valor das Transações no Último Ano',
    ylabel='Quantidade das Transações no Último Ano'
)

plt.show()
