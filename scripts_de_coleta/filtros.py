from unidecode import unidecode
import pandas as pd
import csv


def filtro(resultados, lista_filtros):
    for filtro in lista_filtros:
        for i in range(len(resultados)):
            resultados[i][filtro] = confere_palavras(filtro, resultados[i]['no_blankspaces'])
 
    return resultados

def confere_palavras(palavra, texto):
    palavra = unidecode(palavra.lower()).replace(" ", "")

    if palavra in texto:
        return "s"
    else:
        return "n"

def save_csv_from_list(resultados, arquivo):
    df_resultados = pd.DataFrame(resultados)
    df_resultados.to_csv(f'./dados/1-resultados/{arquivo}.csv', encoding = 'utf-8')

def read(file_path):
    dados = []

    with open(f'./dados/1-resultados/{file_path}.csv', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            dados.append(row)

    return dados

def aplica(lista_filtros, nome_arquivo):
    dados = read(f"{nome_arquivo}_bruto")
    dados = filtro(dados, lista_filtros)
    save_csv_from_list(dados, f"{nome_arquivo}_filtro")