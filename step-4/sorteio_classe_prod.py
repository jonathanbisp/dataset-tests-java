# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 20:25:09 2020

@author: JJSS
"""

import pandas as pd
import json
import random

from math import ceil

import credentials, request_manager

git_username, git_access_token = credentials.load("tokens.txt")
base_url = "https://api.github.com/repos/{}/git/trees/{}?recursive=1"

switch_account = 0

with open("../step-2/paths.json", 'r+') as paths_file:
    try:
        paths = json.load(paths_file)
    except:
        paths = {}
del paths_file

df = pd.read_csv("../step-3/results.csv")

paths_sorteio = {}
for projeto in df['full_name']:
    paths_sorteio.update({projeto: paths[projeto]})

projeto_path = []
for k, v in paths_sorteio.items():
    for caminho in v:
        projeto_path.append([k, caminho])
del k, v, caminho


sorteados = []
while len(sorteados)!= ceil(len(projeto_path)*0.05)+1:
    random.shuffle(projeto_path)
    num = random.randint(0,len(projeto_path))
    candidato = projeto_path.pop(num)
    
    candidato_file_name = "/" + candidato[1].split('/')[-1].replace('Test', '')
    
    candidato_data = df.loc[df['full_name'] == candidato[0], ['full_name','last_commit_sha']].to_dict('records')
    
    tree_files_commit_url = "https://api.github.com/repos/{}/git/trees/{}?recursive=1".format(candidato_data[0]['full_name'], candidato_data[0]['last_commit_sha'])
    tree_files_commit, switch_account = request_manager.request(tree_files_commit_url, git_username, git_access_token, switch_account)
    
    possibilidades = []
    for file in tree_files_commit['tree']:
        if file['path'].endswith(candidato_file_name):
            possibilidades.append(file['path'])
    
    if possibilidades:
        candidato.append(possibilidades)
        sorteados.append(candidato)
del projeto_path, num

for elemento in sorteados:
    sha = df.loc[df['full_name'] == elemento[0], ['last_commit_sha']].to_string(header=False, index=False).strip()
    elemento.append(sha)
del sha, elemento

with open("sorteados.json", 'r+') as results:
    json.dump(sorteados, results)