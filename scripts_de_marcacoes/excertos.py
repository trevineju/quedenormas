import scripts_auxiliares.aux as aux
import scripts_auxiliares.acessa_api as api

def recorta_trechos(dados):
    c = int(api.part)
    for i in range(len(dados)):
        dados[i]["recorte"] = dados[i]["no_whitespaces"][c:c*3]
    return dados

def add_colunas_para_comparacao(dados):
    for i in range(len(dados)):
        dados[i]["txt_mun_data"] = -1
        dados[i]["txt_mun"] = -1
        dados[i]["txt"] = -1
    return dados

def marca_casos_repetidos(dados):
    dados = add_colunas_para_comparacao(dados)
    for i in range(len(dados)-1):
        print(f"Verificando repetições | {i} de {len(dados)}")

        excerpt = dados[i]['no_whitespaces']
        i_city = dados[i]["territory_id"]
        i_date = dados[i]["date"]

        for y in range(i+1, len(dados)):
            cutted_excerpt = dados[y]['recorte']
            y_city = dados[y]["territory_id"]
            y_date = dados[y]["date"]

            if cutted_excerpt in excerpt:                
                if i_city == y_city: # mesmo municipio
                    if i_date == y_date: # mesma data
                        dados = inclui_marcacao('txt_mun_data', dados, i, y)
                    else: # datas diferentes
                        dados = inclui_marcacao('txt_mun', dados, i, y)
                else: # municipios diferentes
                    dados = inclui_marcacao('txt', dados, i, y)

    return dados

def inclui_marcacao(coluna, dados, i, y):
    id = min(dados[i][coluna], dados[y][coluna])
    if id == -1: id = i

    dados[i][coluna] = id
    dados[y][coluna] = id

    return dados

def aplica_criterios(dados, criterios, mensagem):
    for i in range(len(dados)):
        if "status" not in list(dados[i].keys()): dados[i]["status"] = ""

        for config in criterios:
            if deve_ser_marcado(dados[i], config):
                dados[i]["status"] = mensagem

    return dados

def deve_ser_marcado(caso, config):
    descarte = True    
    for criterio in config:
        descarte = descarte and criterio[0] == caso[criterio[1]]
    return descarte

def marca_urls_iguais(dados):
    for i in range(len(dados)-1):
        if "url_repetida" not in list(dados[i].keys()): dados[i]["url_repetida"] = ""

        i_url = dados[i]["txt_url"]
        for y in range(i+1, len(dados)):
            y_url = dados[y]["txt_url"]

            if i_url == y_url:
                print(dados[i]["clear_excerpt"])
                print()
                print(dados[y]["clear_excerpt"])
                breakpoint()
    
    return dados

def compara(caminho, arq_entrada, arq_saida, descartes, interesses): 
    dados = aux.read_data(caminho, arq_entrada)
    dados = recorta_trechos(dados)
    dados = marca_casos_repetidos(dados)    

    dados = aplica_criterios(dados, interesses, "aderente_automatizado")    
    dados = aplica_criterios(dados, descartes, "descarte_automatizado")

    dados = marca_urls_iguais(dados)

    aux.save_data(dados, caminho, arq_saida)

