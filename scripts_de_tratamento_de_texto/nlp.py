# https://medium.com/turing-talks/uma-an%C3%A1lise-de-dom-casmurro-com-nltk-343d72dd47a7
# https://www.nltk.org/book/

# import re
# import nltk
# from nltk.probability import FreqDist
# from nltk.tokenize import word_tokenize
# nltk.download('punkt')
# nltk.download('stopwords')
            

"""
def get_texto(response):
    count = 0
    texto = ""

    for item in response['gazettes']:
        for excerto in item['excerpts']:
            count += 1
            texto = texto + excerto
            texto = texto + " "

    return texto, count

def pre_processamento(texto):  
    texto = saneamento(texto)

    # seleciona apenas letras e coloca todas em minúsculo 
    texto =  re.findall(r'\b[A-zÀ-úü]+\b', texto.lower())

    # remove stopwords
    stopwords = nltk.corpus.stopwords.words('portuguese') + specific_stopwords()

    #JU: talvez adicionar novas stopwors próprias de diários oficiais

    stop = set(stopwords)
    sem_stopwords = [w for w in texto if w not in stop]

    # juntando os tokens novamente em formato de texto
    texto_limpo = " ".join(sem_stopwords)

    return texto_limpo

def specific_stopwords():
    return [
        "municipal",
        "município",
        "sobre",
        "dia",
        "rede",     
    ]

"""

# for i in range(len(resultados['gazettes'])):
#     resultados['gazettes'][i]['excerpts'] = saneamento(resultados['gazettes'][i]['excerpts'][0])

# subconjunto = filtro(resultados)

# arquivo = "resultados_reconhecimento-facial"
# save_csv(subconjunto, arquivo)

# # pre processamento

# texto, conta_excertos = get_texto(resultados)

# print("NUMERO DE EXCERTOS: ", conta_excertos)

# texto = pre_processamento(texto)

# # tokenizando 
# tokens = word_tokenize(texto)

# # contagem de frequencia
# fd = FreqDist(tokens)
# # print(fd.most_common(50))

# # contexto 
# aux = nltk.Text(tokens)
# contextos = aux.concordance('menstrual')

# # bigramas
# bigramas = aux.collocations()

# plot
# import matplotlib.pyplot as plt
# plt.figure(figsize = (13, 8))
# fd.plot(30, title = "Frequência de Palavras")




