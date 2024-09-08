import criterios_de_pesquisa as cp

import scripts_de_coleta.cobertura as cobertura
import scripts_de_coleta.coleta as coleta

import scripts_de_marcacoes.filtros as filtros
import scripts_de_marcacoes.excertos as excertos

import scripts_de_tratamento_de_texto.salva_decretos as salva_decretos
import scripts_de_tratamento_de_texto.segmenta_artigos as segmenta_artigos

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
  
    coleta.resultados(p["busca"], p["inicio"], p["fim"], dir_raw_data, resultados_brutos)   
    if cp.salvar_cobertura: cobertura.municipios_com_resultados(dir_raw_data, resultados_brutos, cobertura_resultados)
    filtros.aplica(p["termos-de-busca"], p["incluir-diretivas"], cp.diretivas, p["palavras-filtro"], dir_raw_data, resultados_brutos, resultados_filtrados)
    excertos.compara(dir_raw_data, resultados_filtrados, resultados_comparados)

# salva_decretos.recorta_textos(caminho, nome_arquivo)
# segmenta_artigos.main()


