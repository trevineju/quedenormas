import scripts_auxiliares.aux as aux
import numpy as np
import pandas as pd
from nltk.metrics.distance import jaro_winkler_similarity
import plotly.express as px


def coleta_todos(entrada_dir):
    todos = {}

    for file in aux.get_all_files(entrada_dir):
        pedacos = file.name.split("_")
        data = pedacos[0]
        uf = pedacos[1]
        municipio = pedacos[2]        
        id = f"{municipio}-{uf}"
        
        dados = aux.read_json_file(entrada_dir, file.name)

        todos[id] = {
            "n_decreto": "",
            "data": data,
            "texto": dados,
        }
    return todos

def troca_indices(dados, i_inicial):
    textos = {}
    for key in dados.keys():
        textos[i_inicial] = dados[key]
        i_inicial += 1
    return i_inicial, textos

def normaliza_indices(dados):
    qnt_artigos = 0

    for e_keys in dados.keys():
        qnt_artigos, textos = troca_indices(dados[e_keys]["texto"], qnt_artigos)
        dados[e_keys]["texto"] = textos

    return dados

def cria_ref_indices(dados):
    todos = {}

    for e_keys in dados.keys():
        for i_keys in dados[e_keys]["texto"]:
            todos[i_keys] = aux.sanitiza_e_concatena(dados[e_keys]["texto"][i_keys])
    
    return todos

def matriz_comparacao(indices):
    tam = len(indices)
    m_comp = np.zeros(shape=(tam,tam))

    for i in range(tam-1):
        print(f"Progresso de comparações: {i}/{tam-1}")

        for y in range(i+1, tam):
            m_comp[i,y] = jaro_winkler_similarity(indices[i], indices[y])
    
    return m_comp

def exibe(matriz):
    df = pd.DataFrame(matriz)

    fig = px.density_heatmap(df)
    fig.write_image("fig1.png")

def compara(entrada_dir):
    artigos_dict = coleta_todos(entrada_dir)
    artigos_dict = normaliza_indices(artigos_dict)

    indices = cria_ref_indices(artigos_dict)
    matriz = matriz_comparacao(indices)
    exibe(matriz)
    
