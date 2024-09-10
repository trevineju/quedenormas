from datetime import datetime
import scripts_auxiliares.aux as aux
import scripts_auxiliares.acessa_api as api

def available_cities():
    dados = api.get_response(api.available_cities)

    cities_list = []
    for i in range(len(dados["cities"])):
        cities_list.append(dados["cities"][i]["territory_id"])
    
    return cities_list

def seleciona_municipios(dados):
    conjunto_ids = set()
    for i in range(len(dados)):
        conjunto_ids.add(dados[i]['territory_id'])
    return list(conjunto_ids)

def intervalo_cobertura(codeslist):
    dados = []
    params = api.params 
    params["number_of_excerpts"] = 1
    params["size"] = 1
    
    i=1
    for ibgecode in codeslist:
        print(f"{datetime.now().strftime('%Y/%m/%d %H:%M')} | {i}/{len(codeslist)}")
        i+=1

        params["territory_ids"] = ibgecode

        # primeira edicao
        params["sort_by"] = "ascending_date" 
        edicao_1 = api.get_response(api.request_url(params))
        # ultima edicao 
        params["sort_by"] = "descending_date"
        edicao_n = api.get_response(api.request_url(params))

        dados.append({
            "ibgecode": ibgecode,
            "nome": edicao_n["gazettes"][0]["territory_name"],
            "uf": edicao_n["gazettes"][0]["state_code"],
            "data_inicial": edicao_1["gazettes"][0]["date"],
            "data_final": edicao_n["gazettes"][0]["date"],
            "total": edicao_n["total_gazettes"],
            "coleta_mais_antiga": edicao_1["gazettes"][0]["scraped_at"]
        })

    return dados

def completa(caminho, nome_arquivo):
    cities_list = available_cities() 
    cobertura = intervalo_cobertura(cities_list)
    aux.save_data(cobertura, caminho, f"{nome_arquivo}_cobertura-completa")

def municipios_com_resultados(caminho, arquivo_entrada, arquivo_saida):
    dados = aux.read_data(caminho, arquivo_entrada)
    cobertura = intervalo_cobertura(seleciona_municipios(dados))
    aux.save_data(cobertura, caminho, arquivo_saida)
