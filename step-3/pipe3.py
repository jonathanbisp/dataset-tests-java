# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 18:43:00 2020

@author: JJSS
"""

import pandas as pd

from math import ceil

#remove os repositorios que não foram encontrados
with open("../step-2/data_result.csv", "r+",encoding='utf8') as data_source:
    content = ""
    for line in data_source:
        if(not line.endswith(",,,\n")):
            content += line
    data_source.truncate(0)
    data_source.seek(0)
    data_source.write(content)
del content, data_source, line

#carrega o dataframe para a memoria
df = pd.read_csv('../step-2/data_result.csv', index_col='repo_id')

#remove o indice que usamos durante a mineração
df = df.drop(columns=['index'])

#deleta eventuais duplicatas
df = df.drop_duplicates(subset=['full_name'])

#deixa apenas os projetos que são Java
df = df.loc[lambda x: x.language == "Java"]

#função normalizadora, coloca os valores da coluna passada entre 0 e 1 em uma nova coluna
def normalize(df, colName, colNameN):
    result = df.copy()
    max_value = df[colName].max()
    min_value = df[colName].min()
    result[colNameN] = (df[colName] - min_value) / (max_value - min_value)
    return result

#normaliza os valores
df = normalize(df, 'forks_count', 'forks_count_normalized')
df = normalize(df, 'stargazers', 'stargazers_normalized')

#cria uma coluna de classificação, somando os valores normalizados
df['classification'] = df['forks_count_normalized'] + df['stargazers_normalized']

#deleta as colunas que foram criadas para gerar a classificação
df = df.drop(columns=['forks_count_normalized','stargazers_normalized'])

#ordena as linhas pela sua classificação
df = df.sort_values(by=['classification'], ascending=False)

#salva o dataframe com todas as linhas e colunas e suas classificações
df.to_csv('dataset.csv', encoding='utf-8', index=True)

#5% do dataset
df = df.iloc[:ceil(df.shape[0] * 0.05),:]

#salva os melhores 5% resultado no results.csv
df.to_csv('results.csv', encoding='utf-8', index=True)
