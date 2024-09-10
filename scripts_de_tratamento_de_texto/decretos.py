import requests
import re
import scripts_auxiliares.aux as aux

status = "aderente"

marcacao_inicio_1 = "decreto"
marcacao_inicio_2 = "resolucao"
marcacao_meio = "regulament*14.129"
marcacao_fim = "entra em vigor"

desloc_padrao = 250

casos_pendentes = []

def modifica_regex(texto):
    final = ""
    um_espaco_talvez = "\s?"
    qualquer = ".*"

    for i in range(len(texto)):
        if texto[i] == ".":
            final += "\."
        elif texto[i] == " ":
            pass
        elif texto[i] == "*":
            final += qualquer
        else:
            final += texto[i] + um_espaco_talvez
    
    return final

def cria_regex():
    marc_inicio_1 = modifica_regex(marcacao_inicio_1)
    marc_inicio_2 = modifica_regex(marcacao_inicio_2)
    marc_meio = modifica_regex(marcacao_meio)
    marc_fim = modifica_regex(marcacao_fim)

    regex = f"({marc_inicio_1}|{marc_inicio_2}).+{marc_meio}(?:(?!{marc_meio}).)*?{marc_fim}"
    return regex

def find_recursivo(regex, texto, lado, qnt): 
    if lado == "esq":
        resultado = re.search(regex, texto[qnt:], re.IGNORECASE)

    if lado == "dir":
        resultado = re.search(regex, texto[:-qnt], re.IGNORECASE)

    if resultado is None:
        return texto

    return find_recursivo(regex, resultado.group(), lado, qnt)    

def collect_norma_text(url):
    response = aux.sanitiza(requests.get(url).text)

    regex_completa = cria_regex()
    reduz_a_esquerda = find_recursivo(regex_completa, response, "esq", 2)
    reduz_a_direita = find_recursivo(regex_completa, reduz_a_esquerda, "dir", 2)
    
    index_inicial = max(0, response.find(reduz_a_direita) - desloc_padrao)
    index_final = min(index_inicial + len(reduz_a_direita) + desloc_padrao, len(response))
    norma = response[index_inicial:index_final]

    if response == norma:
        return None

    return norma
 

def save_txt(norma, caminho, nome_arquivo):
    text_file = open(f"{caminho}/{nome_arquivo}.txt", "w")
    text_file.write(norma)
    text_file.close()

def salva(caminho_entrada, arq_entrada, caminho_saida):
    dados = aux.read_data(caminho_entrada, arq_entrada)

    for i in range(len(dados)):
        if dados[i]["STATUS"] == status:
            norma = collect_norma_text(dados[i]["txt_url"])
            if norma:
                save_txt(norma, caminho_saida, f'{dados[i]["date"]}_{dados[i]["state_code"]}_{dados[i]["territory_name"].replace(" ", "-")}_lei-de-governo-digital')
            else:
                casos_pendentes.append(dados[i]["txt_url"])
    
    print("CASOS SEM MATCH: \n", casos_pendentes)

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
