import requests
from unidecode import unidecode
import json
from dateutil.rrule import YEARLY, rrule
from datetime import date, datetime
import pandas as pd
from collections import deque
from itertools import islice


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

gazettes_endpoint = "https://queridodiario.ok.org.br/api/gazettes?"

def query_gazettes(params):
    url = gazettes_endpoint
    for key in params.keys():
        if params[key] is None or params[key] == "":
            continue
        else:
            url += f"{key}={params[key]}&"
    url = url[:-1]  

    # print(f"{datetime.now().strftime('%Y/%m/%d %H:%M')} | Requisitando {url}\n")
    response = requests.get(url)
    return json.loads(response.text)

def save_csv_from_list(resultados, arquivo):
    df_resultados = pd.DataFrame(resultados)
    df_resultados.to_csv(f'./dados/1-resultados/{arquivo}.csv', encoding = 'utf-8')

def separates_excerpts(resultados):
    print("\nOrganizando resultados obtidos")
    print(f"ANTES  | Quantidade de resultados: {len(resultados)}")

    resultados_unicos = []
    for resultado in resultados:
        for excerto in resultado['excerpts']:
            excerto_unico = resultado.copy()
            excerto_unico['excerpts'] = sanitiza(excerto)
            excerto_unico['no_blankspaces'] = excerto_unico['excerpts'].replace(" ", "")
            resultados_unicos.append(excerto_unico)
    print(f"DEPOIS | Quantidade de resultados: {len(resultados_unicos)}\n")

    return resultados_unicos

def get_qnt_resultados(params):
    params["size"] = 1
    response = query_gazettes(params)
    return response["total_gazettes"]

def get_oldest_result_date(params):
    params["size"] = 1
    response = query_gazettes(params)
    return response["gazettes"][0]["date"]

def _sliding_window(oldest_date, n=2):
    dates_of_interest = [
        dt for dt in rrule(freq=YEARLY, dtstart=oldest_date, until=date.today(), interval=2)
    ]
       
    if date.today() not in dates_of_interest:
        dates_of_interest.append(date.today()) 

    it = iter(dates_of_interest)
    window = deque(islice(it, n - 1), maxlen=n)
    for x in it:
        window.append(x)
        yield tuple(window)

def collect_results(params):
    lista_de_resultados = []
    oldest_date = datetime.strptime(get_oldest_result_date(params.copy()), '%Y-%m-%d').date()

    for start, end in _sliding_window(oldest_date):
        start = start.strftime('%Y-%m-%d')
        end = end.strftime('%Y-%m-%d') 
        params["published_since"] = start
        params["published_until"] = end 

        qnt_resultados = get_qnt_resultados(params.copy())

        for offset in range(0, qnt_resultados, params["size"]):
            params["offset"] = offset
            
            print(f"{datetime.now().strftime('%y/%m/%d %H:%M')} | Obtendo resultados do intervalo {start} a {end} | {offset}/{qnt_resultados}")
            response = query_gazettes(params)
            lista_de_resultados.extend(response['gazettes'])
    
    for i in range(len(lista_de_resultados)):
        lista_de_resultados[i]["busca"] = params["querystring"]

    return separates_excerpts(lista_de_resultados)

def sanitiza(texto):
    texto = unidecode(texto.lower())

    # remove "-\n"
    texto = texto.replace("-\n", "")

    # substitui "\n" por blankspace
    texto = texto.replace("\n", " ")

    while "  " in texto:
        texto = texto.replace("  ", " ")

    return texto

def buscas(lista_de_pesquisas, filtro_intervalo, inicio, fim, nome_arquivo_geral):  
    total_resultados = []

    if filtro_intervalo:
        fixed_params["published_since"] = inicio
        fixed_params["published_until"] = fim

    for item in lista_de_pesquisas:
        for search_key in item[1]:
            print(f"Iniciando pesquisas para tema {search_key}")
            fixed_params["querystring"] = search_key
            resultados = collect_results(fixed_params.copy())
            total_resultados.extend(resultados)
    
    save_csv_from_list(total_resultados, f"{nome_arquivo_geral}_bruto")