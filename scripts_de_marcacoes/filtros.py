from unidecode import unidecode
import scripts_auxiliares.aux as aux


def confere_palavras(palavra, texto):
    palavra = unidecode(palavra.lower()).replace(" ", "")

    if palavra in texto:
        return "s"
    else:
        return "n"

def marca_filtros(resultados, lista_filtros):
    for filtro in lista_filtros:
        filtro = aux.sanitiza_e_concatena(filtro)
        for i in range(len(resultados)):
            resultados[i][filtro] = confere_palavras(filtro, resultados[i]['no_whitespaces'])
 
    return resultados

def add_colunas(dados):
    for i in range(len(dados)):
        dados[i]["clear_excerpt"] = aux.sanitiza(dados[i]['excerpts'])
        dados[i]["no_whitespaces"] = aux.sanitiza_e_concatena(dados[i]['excerpts'])
    return dados

def aplica(termos_de_busca, incluir_filtro, filtros_comuns, filtros_especificos, caminho, entrada, saida):
    dados = aux.read_data(caminho, entrada)
    dados = add_colunas(dados)
    dados = marca_filtros(dados, termos_de_busca + filtros_especificos)

    if incluir_filtro:
        dados = marca_filtros(dados, filtros_comuns)

    aux.save_data(dados, caminho, saida)
    
    