import pandas
from unidecode import unidecode
import csv
import os
import json

def save_data(dados, path, arquivo):
    """ dados is list
    """
    df = pandas.DataFrame(dados)
    df.to_csv(f'{path}/{arquivo}.csv', encoding = 'utf-8')

def read_data(path, arquivo):
    dados = []
    with open(f'{path}/{arquivo}.csv', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            dados.append(row)
    csvfile.close()
    return dados

def read_json_file(path, arquivo):
    with open(f'{path}/{arquivo}') as json_file:
        return json.load(json_file)
    
def save_json(dados, path, arquivo):
    file = open(f"{path}/{arquivo}.json", "w", encoding="utf-8")
    json.dump(dados, file, indent=4)
    file.close()

def get_all_files(dir):
    return [file for file in os.scandir(dir)]

def sanitiza(texto):
    texto = unidecode(texto.lower())

    # remove "-\n"
    texto = texto.replace("-\n", "")

    # substitui "\n" por blankspace
    texto = texto.replace("\n", " ")

    while "  " in texto:
        texto = texto.replace("  ", " ")

    return texto

def sanitiza_e_concatena(texto):
    return sanitiza(texto).replace(" ", "")