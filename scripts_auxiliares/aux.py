import pandas
from unidecode import unidecode
import csv


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