salvar_cobertura = False

from datetime import date
hoje = str(date.today())

diretivas = [    
    # instrumentos
    "lei",
    "federal", 
    "estadual", 
    "plano", 
    "programa",
    "politica municipal",

    # ações
    "designa", "designo"
    "nomeia", "nomeio", "nomear",             
    "exonera", "exonero", "exonerar", 
    "regulamenta", "regulamento", "regulamentar",       
    "cria", "crio", 
    "determina", "determino",
    "institui", "instituida",
    "decret",           #decreta, decreto
    "atribu",           #atribui, atribuo 
    "aprov",            #aprova, aprovo
    "sancion",          #sanciona, sanciono
    "alter",            #altera, altero, alteracao
    "resolve",          
    
    # organização
    "secretaria",
    "comissao", 
    "comite", 
    "grupo de trabalho",
]

lista_de_pesquisas = [   
    # {
    #     "dir-resultados": "",   
    #     "nome-arquivo": "",
    #     "busca": '',
    #     "inicio": "", # "YYYY-MM-DD"
    #     "fim": hoje,  # ou "YYYY-MM-DD"
    #     "termos-de-busca": [
    #     ],
    #     "incluir-diretivas": True,
    #     "palavras-filtro":  [
    #     ],
    # }, 
    
    {
        "dir-resultados": "lei_governo_digital",
        "nome-arquivo": "leigovdigital",
        "busca": '"14129" "14.129" "governo digital"~2',
        "inicio": "2021-03-29",
        "fim": hoje,
        "termos-de-busca": [
            "14129", 
            "14.129",
            "governo digital" 
        ],
        "incluir-diretivas": True,
        "palavras-filtro":  [
            "secretaria especial de desburocratizacao, gestao e governo digital", 
            "seges",
            "inteligencia de dados",
            "software",
            "catalogo",
            "solucao", "solucoes",
            "tic", "pdtic",
            "gratuidade",    # costuma aparecer em uma das redações do decreto
            "escolavirtual", # muita menção a curso da enap nos excertos 
            "digital",
        ],
        "descartes": [
            [("s", "escolavirtual")],
            [("s", "14129"), ("n", "governo digital")],
            [("s", "14129"), ("n", "federal")],
            [("s", "14.129"), ("n", "digital")],
        ],
        "interesses": [
            [("s", "14.129"), ("s", "regulament")],
            [("s", "14129"), ("s", "regulament")],
            [("s", "governo digital"), ("s", "regulament")],
            [("s", "gratuidade")],
        ]
    },

    # {
    #     "dir-resultados": "lei_acesso_informacao",
    #     "nome-arquivo": "lai",          
    #     "busca": '"12.527"', #'"12527" "12.527" "LAI" "acesso informação"~2 "acesso informacao"~2 "acesso informaçao"~2 "acesso informacão"~2',
    #     "inicio": "2024-01-01",
    #     "fim": hoje,        
    #     "termos-de-busca": [
    #         "12527", 
    #         "12.527", 
    #         "lai", 
    #         "acesso a informacao"
    #     ],
    #     "incluir-diretivas": True,
    #     "palavras-filtro":  [
    #     ]
    # },

    # {
    #     "dir-resultados": "lei_protecao_de_dados",
    #     "nome-arquivo": "lgpd",
    #     "busca": '"13.709"', #'"13709" "13.709" "LGPD" "proteção dados"~2 "protecao dados"~2 "proteçao dados"~2 "protecão dados"~2',
    #     "inicio": "2024-01-01",
    #     "fim": hoje,        
    #     "termos-de-busca": [
    #         "13709", 
    #         "13.709",
    #         "lgpd",
    #         "protecao",
    #     ],
    #     "incluir-diretivas": True,
    #     "palavras-filtro":  [
    #         "complience", 
    #         "compliance", 
    #         "privacidade",
    #         "encarregad"
    #     ],
    # }, 
]



## LEGADO
"""
BUSCAS
#    ("governanca", ['"governança dados"~2 "governança pública"~2 "governança integridade"~2']),
#    ("govaberto", ['"governo aberto" "dados abertos" "dados públicos" "dados publicos" "transparencia ativa" "transparência ativa" "transparência passiva" "transparencia passiva"']),
#    ("recfacial", ['"reconhecimento facial"']),
#    ("clima", ['"mitigação clima"~5 "mitigação climática"~5']),
#    ("ciencia", ['"política tecnologia"~5 "politica tecnologia"~5 "política ciência"~5 "politica ciência"~5 "política ciencia"~5 "politica ciencia"~5 "ciência aberta"~2 "ciencia aberta"~2']),

FILTROS
#    "governanca", "dados", "integridade",
#    "governo aberto", "dados abertos", "dados publicos", "transparencia", "transparencia ativa", "transparencia passiva",
#    "seguranca",
#    "tecnologia", "ciencia", "ciencia aberta",
"""