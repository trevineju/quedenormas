import criterios_de_pesquisa as cp

import scripts_de_coleta.cobertura as cobertura
import scripts_de_coleta.coleta as coleta

import scripts_de_marcacoes.filtros as filtros
import scripts_de_marcacoes.excertos as excertos

import scripts_de_tratamento_de_texto.decretos as decretos
import scripts_de_tratamento_de_texto.artigos as artigos

import os
from datetime import date
today = date.today()

for p in cp.lista_de_pesquisas:
    dir_raw_data = f'./dados/1-resultados/{p["dir-resultados"]}'
    base_nome = f'{today}_{p["nome-arquivo"]}_{p["inicio"]}-{p["fim"]}'
    resultados_brutos = f"{base_nome}_dados-brutos"
    cobertura_resultados = f"{base_nome}_cobertura-no-qd"
    resultados_filtrados = f"{base_nome}_filtros"
    resultados_comparados = f"{base_nome}_comparacoes"       
    if not os.path.exists(dir_raw_data): os.mkdir(dir_raw_data)
  
    # coleta
    coleta.resultados(p["busca"], p["inicio"], p["fim"], dir_raw_data, resultados_brutos)   
    if cp.salvar_cobertura: cobertura.municipios_com_resultados(dir_raw_data, resultados_brutos, cobertura_resultados)
    
    # marcacoes
    filtros.aplica(p["termos-de-busca"], p["incluir-diretivas"], cp.diretivas, p["palavras-filtro"], dir_raw_data, resultados_brutos, resultados_filtrados)
    excertos.compara(dir_raw_data, resultados_filtrados, resultados_comparados)

    # validacao humana
    dir_validaded_data = f'./dados/2-resultados_analisados/{p["dir-resultados"]}'    
    if not os.path.exists(dir_validaded_data): os.mkdir(dir_validaded_data)
    resultados_validados = f"{base_nome}_validado"
    # todo: salvar uma copia?
    
    # tratamento
    dir_decretos_data = f'./dados/3-decretos/{p["dir-resultados"]}'    
    dir_segmentos_data = f'./dados/4-segmentos_de_decretos/{p["dir-resultados"]}'    
    
    if not os.path.exists(dir_decretos_data): os.mkdir(dir_decretos_data)
    if not os.path.exists(dir_segmentos_data): os.mkdir(dir_segmentos_data)

    decretos.salva(dir_validaded_data, resultados_validados, dir_decretos_data)
    decretos.segmenta(dir_decretos_data, dir_segmentos_data)
    artigos.compara(dir_segmentos_data)


