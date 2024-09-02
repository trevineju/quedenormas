salvar_intervalos_de_cobertura = False
arquivo = "lei-gov-digital"

filtro = True
# "YYYY-MM-DD"
inicio = "2021-03-29"     
fim = None #"2024-07-25"

# TODO: reorganizar para deixar pesquisas e seus filtros juntos
# certa pesquisa usar todos os filtros, ou não, pode ser algo opcional

"""
formato da tupla (nome-do-arquivo, lista-de-palavras-chaves)
"""
pesquisas = [
#    ("lai", ['"12527" "12.527" "LAI" "acesso informação"~2 "acesso informacao"~2 "acesso informaçao"~2 "acesso informacão"~2']),
 
    ("leigovdigital", ['"14.129"']), # OU '"14129" "14.129" "governo digital"~2' 

#    ("lgpd", ['"13709" "13.709" "LGPD" "proteção dados"~2 "protecao dados"~2 "proteçao dados"~2 "protecão dados"~2 "complience" "compliance" "privacidade"']),

#    ("governanca", ['"governança dados"~2 "governança pública"~2 "governança integridade"~2']),

#    ("govaberto", ['"governo aberto" "dados abertos" "dados públicos" "dados publicos" "transparencia ativa" "transparência ativa" "transparência passiva" "transparencia passiva"']),

#    ("recfacial", ['"reconhecimento facial"']),

#    ("clima", ['"mitigação clima"~5 "mitigação climática"~5']),

#    ("ciencia", ['"política tecnologia"~5 "politica tecnologia"~5 "política ciência"~5 "politica ciência"~5 "política ciencia"~5 "politica ciencia"~5 "ciência aberta"~2 "ciencia aberta"~2']),
]

filtro_lexical = [
## SEÇÃO: afinar resultados das buscas acima (uma linha por busca)
##################################################################

#    "12527", "12.527", "lai", "acesso a informacao",

    "14129", "14.129", "governo digital", "secretaria especial de desburocratizacao, gestao e governo digital", "seges",

#    "13709", "13.709", "lgpd", "protecao", "complience", "compliance", "privacidade", "encarregad",

#    "governanca", "dados", "integridade",

#     "governo aberto", "dados abertos", "dados publicos", "transparencia", "transparencia ativa", "transparencia passiva",

#    "seguranca",
    
# nenhum filtro pra busca de clima

#    "tecnologia", "ciencia", "ciencia aberta",

## SEÇÃO : palavras de interesse geral
######################################
    "federal",
    "lei",
    "design", #designa, designo
    "nome", #nomeia, nomeio, nomear
    "exoner", 
    "regulament", #regulamenta, regulamento
    "cria", "crio", 
    "determin", #determina, determino 
    "institui", #institui, instituida
    "decret", #decreta, decreto
    "atribu", #atribui, atribuo 
    "aprov", #aprova, aprovo
    "sancion", #sanciona, sanciono
    "alter", #altera, altero, alteracao
    "resolv", #resolve
    "plano", 
    "programa",
    "politica",
    "comissao", "comite", "grupo de trabalho",
    "secretaria",
    "gratuidade",
    "inteligencia de dados",
    "software",
    "catalogo",
    "soluc", #solucao, solucoes
    "tic", "pdtic",
    "escolavirtual", #muita menção a curso     
]