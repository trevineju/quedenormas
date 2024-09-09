import requests
import os
import re
import json
import scripts_auxiliares.aux as aux

status = "aderente"

nlei = "14.129"
marcacao_inicio = "d\s*e\s*c\s*r\s*e\s*t\s*o"
# tem casos que não é decreto, e sim "resolução"
marcacao_fim = "e\s*n\s*t\s*r\s*a\s*e\s*m\s*v\s*i\s*g\s*o\s*r"

desloc_padrao = 450

casos_pendentes = []

"""
logica é:
1. achar uma ocorrencia de nlei
2. procurar pela palavra 'decreto' que aparece imediatamente antes de um resultado de nlei
3. procurar pela expressao 'entra em vigor' que aparece imediatamente depois de um resultado de nlei
4. adicionar uma margem de erro depois de 'entra em vigor' visto que o texto não termina ali oficialmente
5. 'normalizar' os resultados visto que podem estar contidos um nos outros
"""

def get_indexes(search_text, response):

    ocorrencias = re.findall(search_text, response, re.IGNORECASE)
    ocorrencias_indexes = []
    
    start = 0   
    for i in range(len(ocorrencias)):
        index = response.find(ocorrencias[i], start)
        ocorrencias_indexes.append(index)
        start = index + len(ocorrencias[i])
    
    return ocorrencias_indexes

def get_ultima_ocorrencia_antes(ref, lista):
    aux = [0]
    for i in range(len(lista)):
        if lista[i] < ref:
            aux.append(lista[i])
    return aux[-1]

def get_primeira_ocorrencia_depois(ref, lista):
    for i in range(len(lista)):
        if ref < lista[i]:
            return lista[i]

def organiza_cortes(i_normas, i_inicios, i_fins):
    cortes = []

    for i in range(len(i_normas)):
        inicio = get_ultima_ocorrencia_antes(i_normas[i], i_inicios)
        fim = get_primeira_ocorrencia_depois(i_normas[i], i_fins)
        fim += desloc_padrao
        cortes.append((inicio, fim))

    return cortes

def normaliza_cortes(lista_de_cortes):
    casos = len(lista_de_cortes)
    i_dos_descartes = set()
    lista_atualizada = []

    for i in range(casos-1):
        ref = lista_de_cortes[i]        

        for y in range(i+1, casos):
            comparado = lista_de_cortes[y]

            # comparado está contido em ref
            if ref[0] <= comparado[0] <= ref[1] and ref[0] <= comparado[1] <= ref[1]:
                i_dos_descartes.add(y)

            # algum grau de intersecção, porém não contido/contém
            # todo
    
    for c in range(casos):
        if c not in i_dos_descartes:
            lista_atualizada.append(lista_de_cortes[c])

    return lista_atualizada

def collect_norma_text(url):
    response = aux.sanitiza(requests.get(url).text)
    print("\n\ntentando caso de ", url)

    i_normas = get_indexes(nlei, response)
    i_inicios = get_indexes(marcacao_inicio, response)
    i_fins = get_indexes(marcacao_fim, response)

    print("quantidade de normas: ", i_normas)
    print("quantidade de comecos: ", i_inicios)
    print("quantidade de fins: ", i_fins)

    if len(i_normas)==0 or len(i_inicios)==0 or len(i_fins)==0:
        print("\n\nUm caso foi pulado!!!")
        casos_pendentes.append(url)
        return []
        
    lista_de_cortes = organiza_cortes(i_normas, i_inicios, i_fins)
    print("lista de cortes antes: ", lista_de_cortes)
    lista_de_cortes = normaliza_cortes(lista_de_cortes)
    print("lista de cortes depois: ", lista_de_cortes)

    normas = []
    for corte in lista_de_cortes:
        normas.append(response[corte[0]:corte[1]])   
    
    return normas

def save_txt(norma, caminho, nome_arquivo):
    text_file = open(f"{caminho}/{nome_arquivo}.txt", "w")
    text_file.write(norma)
    text_file.close()

def salva(caminho_entrada, arq_entrada, caminho_saida):
    dados = aux.read_data(caminho_entrada, arq_entrada)

    for i in range(len(dados)):
        if dados[i]["STATUS"] == status:
            normas = collect_norma_text(dados[i]["txt_url"])
            for n in range(len(normas)):
                save_txt(normas[n], caminho_saida, f'{dados[i]["date"]}_{dados[i]["state_code"]}_{dados[i]["territory_name"].replace(" ", "-")}_lei-de-governo-digital_{n}')
    
    print(casos_pendentes)

def separa_artigos(texto):
    dici = {}
    aux_list = texto.split("art.")
    for i in range(len(aux_list)):
        if i == 0:
            dici[i] = aux_list[i]
        else:
            dici[i] = "art" + aux_list[i]    
    return dici

def segmenta(entrada_dir, saida_dir):    
    for file in aux.get_all_files(entrada_dir):
        with open(file, 'r') as input_file:
            conteudo = input_file.read()
            dados = separa_artigos(conteudo)
            aux.save_json(dados, saida_dir, file.name[:-4])
