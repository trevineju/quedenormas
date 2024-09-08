# Import module
import os
import json

diretorio_de_normas = "dados/3-decretos"

def segmenta(texto):
    dici = {}
    aux_list = texto.split("art.")
    for i in range(len(aux_list)):
        if i == 0:
            dici[str(i)] = aux_list[i]
        else:
            dici[str(i)] = "art" + aux_list[i]    
    return dici

def save_json(dados, path, caminho, nome_arquivo):
    file = open(f"{path}/dados/4-segmentos_de_decretos/{nome_arquivo}.json", "w", encoding="utf-8")
    json.dump(dados, file, indent=4)
    file.close()

def main():
    for filename in os.scandir(diretorio_de_normas):
        if ".txt" in filename.name:
            parent_directory = os.path.split(os.path.dirname(__file__))[0]
            with open(os.path.join(parent_directory, filename), 'r') as input_file:
                conteudo = input_file.read()
                dados = segmenta(conteudo)                
                save_json(dados, parent_directory, filename.name[:-4])