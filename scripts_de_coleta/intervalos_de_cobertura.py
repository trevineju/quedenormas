import requests
import json
from datetime import datetime
import pandas as pd

gazettes_endpoint = "https://queridodiario.ok.org.br/api/gazettes?"

fixed_params = {
    "territory_ids": None,            
    "published_since" : None,
    "published_until" : None,
    "querystring": None,            # string
    "excerpt_size": 1000,            # int
    "number_of_excerpts": 50,        
    "pre_tags": "",            
    "post_tags": "",           
    "size": 200,
    "offset": None,
    "sort_by": "ascending_date"
}

def available_cities():
    link = f"https://queridodiario.ok.org.br/api/cities?levels=3"
    response = requests.get(link)
    response = json.loads(response.text)

    cities_list = []
    for i in range(len(response["cities"])):
        cities_list.append(response["cities"][i]["territory_id"])
    
    return cities_list

def query_gazettes(params):
    url = gazettes_endpoint
    for key in params.keys():
        if params[key] is None:
            continue
        elif params[key] == "":
            continue
        else:
            url += f"{key}={params[key]}&"
    url = url[:-1]  

    # print(f"{datetime.now().strftime('%Y/%m/%d %H:%M')} | Requisitando {url}\n")
    response = requests.get(url)
    return json.loads(response.text)

def intervalo_cobertura(codeslist):
    dados = []
    params = {
        "territory_ids": None,
        "excerpt_size": 50,             
        "number_of_excerpts": 1,        
        "size": 1,
        "sort_by": None
    }

    for ibgecode in codeslist:
        print(f"{datetime.now().strftime('%Y/%m/%d %H:%M')} | Consultando API para município de código {ibgecode}")
        params["territory_ids"] = ibgecode

        # primeira edicao
        params["sort_by"] = "ascending_date" 
        edicao_1 = query_gazettes(params)
        # ultima edicao 
        params["sort_by"] = "descending_date"
        edicao_n = query_gazettes(params)
        
        dados.append({
            "ibgecode": ibgecode,
            "nome": edicao_n["gazettes"][0]["territory_name"],
            "uf": edicao_n["gazettes"][0]["state_code"],
            "data_inicial": edicao_1["gazettes"][0]["date"],
            "data_final": edicao_n["gazettes"][0]["date"],
            "total": edicao_n["total_gazettes"]
        })

    return dados

def save_csv_from_list(resultados, arquivo):
    df_resultados = pd.DataFrame(resultados)
    df_resultados.to_csv(f'./dados/{arquivo}.csv', encoding = 'utf-8')

def coleta(nome_arquivo):
    cities_list = available_cities() 
    cobertura = intervalo_cobertura(cities_list)
    save_csv_from_list(cobertura, f"{nome_arquivo}_cobertura")