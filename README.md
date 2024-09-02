# Sobre
Repositório para coletar e processar texto de atos oficiais a partir de busca na API do Querido Diário

# Arquivos gerados
Toda a lista segue a ordem de consumo, ou seja, o arquivo listado seguinte é produzido a partir do arquivo listado anterior, mesmo que em seções (1, 2, ...) diferentes

1. Em [1-resultados](dados/1-resultados) tem:
- `nome_do_arquivo + _bruto`: resultados conforme o QD entrega
- `nome_do_arquivo + _filtro`: resultados com colunas marcadas por palavras-chave de interesse 
- `nome_do_arquivo + _repeticoes`: resultados marcados casos o miolo dos excertos seja repetido
- `nome_do_arquivo + _proximidade`: resultados marcados caso seus textos sejam parecidos
(usando jaro_winkler_similarity)

2. Em [2-resultados_analisados](dados/2-resultados_analisados) tem:
- `nome_do_arquivo + _verificado`: resultados lidos por humano e classificados quanto ao seu grau de adesão

3. Em [3-decretos](dados/3-decretos) tem:
- arquivos TXT para cada decreto considerado

4. Em [4-segmentos_de_decretos](dados/4-segmentos_de_decretos) tem:
- arquivos JSON para cada decreto segmentado em parágrafos


# Fluxo
1. Atualizar o arquivo [criterios_de_pesquisa.py](criterios_de_pesquisa.py) com as configurações da busca
2. Executar `python3 main.py`, que vai:
    
