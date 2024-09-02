import criterios_de_pesquisa as cp
import scripts_de_coleta.intervalos_de_cobertura as intervalos_de_cobertura
import scripts_de_coleta.pesquisa_termos as pesquisa_termos
import scripts_de_coleta.filtros as filtros
import scripts_de_coleta.compara_excertos as compara_excertos

import scripts_de_tratamento_de_texto.salva_decretos as salva_decretos
import scripts_de_tratamento_de_texto.segmenta_artigos as segmenta_artigos

from datetime import date

today = date.today()

if cp.filtro:
    nome_arquivo = f"{today}_{cp.arquivo}_{cp.inicio}-{cp.fim}"
else: 
    nome_arquivo = f"{today}_{cp.arquivo}"

pesquisa_termos.buscas(cp.pesquisas, cp.filtro, cp.inicio, cp.fim, nome_arquivo)
filtros.aplica(cp.filtro_lexical, nome_arquivo)
compara_excertos.executa(nome_arquivo)

if cp.salvar_intervalos_de_cobertura:
    intervalos_de_cobertura.coleta(nome_arquivo)

salva_decretos.recorta_textos(nome_arquivo)
segmenta_artigos.main()


