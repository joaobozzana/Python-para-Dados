# Storytelling

## Introdução

Essa é uma análise que eu fiz para explorar um pouco as bibliotecas **seaborn** e **matplotlib.pyplot** de Python, que são utilizadas para a visualização de dados. Por conta disso, não levei os dados a nenhuma ferramenta de visualização. Além disso, preferi usar o VSCode em vez de construir no Jupyter Notebook. Queria ver o comportamento e como seria trabalhar isso no prompt.

## Base de Dados e bibliotecas

A base de dados em questão é de crédito e contém informações sobre os clientes de uma instituição financeira. Em particular, meu interesse reside na segunda coluna, denominada default, que indica se um cliente é adimplente (**default = 0**) ou inadimplente (**default = 1**). Meu objetivo é compreender melhor os fatores que levam um cliente a não pagar suas dívidas, visando insights relevantes para o contexto financeiro.

A [Base de dados](/Dados-de-Credito/credito.csv), o [código](/Dados-de-Credito/script.py) e as bibliotecas necessarias:

- `import pandas as pd`
- `import seaborn as sns`
- `import matplotlib.pyplot as plt`

## Etapa de exploração

Fiz algumas observações para entender melhor a base de dados e identificar possíveis problemas que podem requerer tratamento posterior. Essas observações incluem:

- Verificar a representatividade de inadimplentes e adimplentes na base de dados.
- Conferir os tipos de dados presentes na base.
- Avaliar a consistência dos dados para garantir sua integridade e confiabilidade.

Isso me proporcionou uma boa visão e observei alguns problemas, como no caso das colunas **limite_credito** e **valor_transacoes_12m**, que estavam classificadas como tipo object em vez de float. Percebi que isso se deve ao fato de os valores estarem formatados com pontos e vírgulas, seguindo o padrão contábil brasileiro, enquanto o Python reconhece o formato americano. Além disso, observei a presença de dados faltantes nas colunas escolaridade, estado_civil e salario_anual, o que compromete a consistência dos dados. Sendo problemas que eu eventualmente precissarei tratar.

## Etapa de limpeza e tranformação

Após uma análise mais aprofundada da natureza dos dados, procedi com a limpeza e transformação dos mesmos. Em particular, realizei as seguintes ações:

- Correção do esquema das colunas, transformando os dados em float. Utilizei uma função lambda simples para esse propósito.

    - `func = lambda valor: float(valor.replace(".", "").replace(",", "."))`
    - `df['valor_transacoes_12m'] = df['valor_transacoes_12m'].apply(func)`
    - `df['limite_credito'] = df['limite_credito'].apply(func)`


- Remoção dos dados faltantes, decisão tomada após analisar que a remoção não teria um impacto significativo em uma das duas categorias (adimplentes e inadimplentes).
    
    ![Proporção](/Dados-de-Credito/imgs/proporcao.png)

Considerei essas correções necessárias para garantir a consistência e a qualidade dos dados, elementos essenciais para conduzir uma análise precisa e confiável.

## Etapa de análise (com visualizações)

Além de focar nas colunas com valores numéricos para obter insights, também fiz observações nas colunas com valores categóricos. Para explorar a extensão das bibliotecas e testar diferentes tipos de gráficos, gerei alguns exemplos, incluindo:
![Fig1](/Dados-de-Credito/imgs/Fig1.png)
![Fig2](/Dados-de-Credito/imgs/Fig2.png)
![Fig3](/Dados-de-Credito/imgs/Fig3.png)


## Resumo dos insights gerados.

Ao realizar a análise gráfica, não obtive muitos insights significativos. No entanto, uma observação interessante que destaco é a correlação entre clientes inadimplentes e baixos valores de transações, assim como uma menor frequência de transações nos últimos 12 meses. O gráfico abaixo exemplifica essa tendência:

- default 0 = adimplentes
- default 1 = inadimplentes

![Fig4](/Dados-de-Credito/imgs/Fig4.png)

Essa observação sugere que o comportamento de gastos dos clientes pode estar relacionado à probabilidade de inadimplência, o que pode ser uma pista importante para análises futuras.