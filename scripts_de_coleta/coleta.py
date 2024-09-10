
from dateutil.rrule import YEARLY, rrule
from datetime import date, datetime
from collections import deque
from itertools import islice
import scripts_auxiliares.aux as aux
import scripts_auxiliares.acessa_api as api

def separates_excerpts(resultados, params):
    print("\nOrganizando resultados obtidos")
    print(f"ANTES  | Quantidade de resultados: {len(resultados)}")

    resultados_unicos = []
    for resultado in resultados:
        resultado["chave-busca"] = params["querystring"]
        for excerto in resultado['excerpts']:
            excerto_unico = resultado.copy()
            excerto_unico['excerpts'] = excerto
            resultados_unicos.append(excerto_unico)
    print(f"DEPOIS | Quantidade de resultados: {len(resultados_unicos)}\n")

    return resultados_unicos

def get_qnt_resultados(params):
    params["size"] = 1
    return api.get_response(api.request_url(params))["total_gazettes"]

def get_oldest_result_date(params):
    params["size"] = 1
    return api.get_response(api.request_url(params))["gazettes"][0]["date"]

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

        for offset in range(0, get_qnt_resultados(params.copy()), params["size"]):
            params["offset"] = offset
            
            print(f"{datetime.now().strftime('%y/%m/%d %H:%M')} | Obtendo resultados do intervalo {start} a {end} | {offset}")
            response = api.get_response(api.request_url(params))
            lista_de_resultados.extend(response['gazettes'])

    return separates_excerpts(lista_de_resultados, params)

def resultados(search_key, inicio, fim, caminho, nome_arquivo):  
    api_params = api.params
    api_params["published_since"] = inicio
    api_params["published_until"] = fim
    api_params["querystring"] = search_key

    print(f"Iniciando pesquisa para tema {search_key}")
    resultados = collect_results(api_params.copy())
    
    aux.save_data(resultados, caminho, nome_arquivo)
