import pandas as pd
import csv
import concurrent.futures as cf
import asyncio
from nltk.metrics.distance import jaro_winkler_similarity
from datetime import datetime


def save_csv_from_list(resultados, arquivo):
    df_resultados = pd.DataFrame(resultados)
    df_resultados.to_csv(f'./dados/1-resultados/{arquivo}.csv', encoding = 'utf-8')

def cria_colunas(dados, nome_colunas):
    for i in range(len(dados)):
        for nome_coluna in nome_colunas:
            dados[i][nome_coluna] = -1
    return dados

def verifica_repeticoes(dados):
    colunas = ["msm_municipio_msm_data", "msm_municipio", "municipios_diferentes"]
    dados = cria_colunas(dados,colunas)

    for i in range(len(dados)-1):
        ref = dados[i]['recorte']

        for y in range(i+1, len(dados)):
            compara = dados[y]['recorte']

            if ref == compara:
                # é do mesmo lugar
                if dados[i]["territory_id"] == dados[y]["territory_id"]:
                    # no mesmo dia
                    if dados[i]["date"] == dados[y]["date"]:
                        id = min(dados[i]['msm_municipio_msm_data'], dados[y]['msm_municipio_msm_data'])
                        if id == -1: id = i

                        dados[i]['msm_municipio_msm_data'] = id
                        dados[y]['msm_municipio_msm_data'] = id
                    
                    # em dias diferentes
                    else:
                        id = min(dados[i]['msm_municipio'], dados[y]['msm_municipio'])
                        if id == -1: id = i

                        dados[i]['msm_municipio'] = id
                        dados[y]['msm_municipio'] = id
                
                # é de locais diferentes
                else:
                    id = min(dados[i]['municipios_diferentes'], dados[y]['municipios_diferentes'])
                    if id == -1: id = i

                    dados[i]['municipios_diferentes'] = id
                    dados[y]['municipios_diferentes'] = id

    return dados

def background(f):
    def wrapped(*args, **kwargs):
        return asyncio.get_event_loop().run_in_executor(None, f, *args, **kwargs)
    return wrapped

@background
def calcula_proximidade(dados, i, y, ref):
    compara = dados[y]['recorte']
    proximity = jaro_winkler_similarity(ref, compara)

    if compara != ref:

        if 0.975 < proximity <= 1:
            id = min(dados[i]["0.975 a 1"], dados[y]["0.975 a 1"])
            if id == -1: id = i

            dados[i]["0.975 a 1"] = id
            dados[y]["0.975 a 1"] = id

        elif 0.95 < proximity <= 0.975:
            id = min(dados[i]["0.95 a 0.975"], dados[y]["0.95 a 0.975"])
            if id == -1: id = i

            dados[i]["0.95 a 0.975"] = id
            dados[y]["0.95 a 0.975"] = id

        elif 0.925 < proximity <= 0.95:
            id = min(dados[i]["0.925 a 0.95"], dados[y]["0.925 a 0.95"])
            if id == -1: id = i

            dados[i]["0.925 a 0.95"] = id
            dados[y]["0.925 a 0.95"] = id

        elif 0.9 < proximity <= 0.925:
            id = min(dados[i]["0.9 a 0.925"], dados[y]["0.9 a 0.925"])
            if id == -1: id = i

            dados[i]["0.9 a 0.925"] = id
            dados[y]["0.9 a 0.925"] = id
        
        elif 0.875 < proximity <= 0.9:
            id = min(dados[i]["0.875 a 0.9"], dados[y]["0.875 a 0.9"])
            if id == -1: id = i
            
            dados[i]["0.875 a 0.9"] = id
            dados[y]["0.875 a 0.9"] = id
        
        elif 0.85 < proximity <= 0.875:
            id = min(dados[i]["0.85 a 0.875"], dados[y]["0.85 a 0.875"])
            if id == -1: id = i

            dados[i]["0.85 a 0.875"] = id
            dados[y]["0.85 a 0.875"] = id
        
        elif 0.825 < proximity <= 0.85:
            id = min(dados[i]["0.825 a 0.85"], dados[y]["0.825 a 0.85"])
            if id == -1: id = i

            dados[i]["0.825 a 0.85"] = id
            dados[y]["0.825 a 0.85"] = id
        
        elif 0.8 < proximity <= 0.825:
            id = min(dados[i]["0.8 a 0.825"], dados[y]["0.8 a 0.825"])
            if id == -1: id = i

            dados[i]["0.8 a 0.825"] = id
            dados[y]["0.8 a 0.825"] = id

    
    print(f"{datetime.now().strftime('%Y/%m/%d %H:%M')} | i = {i} | {y}/{len(dados)}")  

def verifica_proximidade(dados, nome_arquivo):
    colunas = ["0.8 a 0.825", "0.825 a 0.85", "0.85 a 0.875", "0.875 a 0.9", "0.9 a 0.925", "0.925 a 0.95", "0.95 a 0.975", "0.975 a 1"]
    dados = cria_colunas(dados, colunas)

    for i in range(len(dados)-1):
        ref = dados[i]['recorte']
        
        loop = asyncio.get_event_loop()
        loop.set_default_executor(cf.ThreadPoolExecutor(max_workers=40))                                      
        looper = asyncio.gather(*[calcula_proximidade(dados, i, y, ref) for y in range(i+1, len(dados))])
        results = loop.run_until_complete(looper)

        save_csv_from_list(dados, f"{nome_arquivo}_proximidade")

    return dados

def read(file_path):
    dados = []

    with open(f'./dados/1-resultados/{file_path}.csv', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            dados.append(row)

    return dados

def recorta_trecho(inicio, fim, dados):
    for i in range(len(dados)):
        dados[i]["recorte"] = dados[i]['no_blankspaces'][inicio:fim]
    return dados

def executa(nome_arquivo): 
    dados = read(f"{nome_arquivo}_filtro")
    dados = recorta_trecho(250, 750, dados)

    dados = verifica_repeticoes(dados)
    save_csv_from_list(dados, f"{nome_arquivo}_repeticoes")

    dados = verifica_proximidade(dados, nome_arquivo)
    save_csv_from_list(dados, f"{nome_arquivo}_proximidade")

