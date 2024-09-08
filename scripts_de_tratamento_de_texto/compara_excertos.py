import scripts_auxiliares.aux as aux
import scripts_auxiliares.acessa_api as api
import concurrent.futures as cf
import asyncio
from nltk.metrics.distance import jaro_winkler_similarity
from datetime import datetime

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

def verifica_proximidade(dados, caminho, nome_arquivo):
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


def executa(caminho, nome_arquivo): 
    dados = aux.read_data("./dados/1-resultados", f"{nome_arquivo}_filtros")
    dados = recorta_trechos(dados)

    dados = verifica_repeticoes(dados)
    save_csv_from_list(dados, f"{nome_arquivo}_repeticoes")

    dados = verifica_proximidade(dados, caminho, nome_arquivo)
    save_csv_from_list(dados, f"{nome_arquivo}_proximidade")

