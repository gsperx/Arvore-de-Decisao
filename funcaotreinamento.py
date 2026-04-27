#[>------- Identificações dos Sensores -------<]
#    Usado por todas as identificaçoes ao     #|
#  longo do código                            #|
#                                             #|
ID_conectado   = 0                            #|
ID_voltagem    = 1                            #|
ID_temperatura = 2                            #|
ID_ruido       = 3                            #|
ID_resposta    = 4                            #|
#                                             #|
dados_entrada = [None, #cronometro_rega       #|
                 None, #luminosidade          #|
                 None, #temperatura           #|
                 None, #umidade_solo          #|
                 None] #umidade_atmosferica   #|
#                                             #|
fator_precisao = 1000       #Para as entradas #|
#                                             #|
# OBS: O fator de precisão deve ser maior     #|
#     que a maioria se não todas as divisões  #|
#     de corte para não reduzir precisão.     #|
#                                             #|
max_ocorrencias = (1,                         #|
                   1,                         #|
                   1,                         #|
                   1)                         #|
#                                             #|
#[>-------------------------------------------<]


#[>------- Identificação das Respostas -------<]
#    Define diferentes respostas a depender   #|
#  do valor médio exibido nas listas finais   #|
#                                             #|
respostas = ["Não carregar", #-> 0            #|
             "Carregar"] #-----> 1            #|
#                                             #|
#[>-------------------------------------------<]



def treinar_arvore(dados=None, #lista ATUAL de dados
                   min_registros=0,
                   min_ganho=0.0,
                   ocorrencias_restantes=[-1 for x in max_ocorrencias], #lista de valores maximos de ocorrencia de cada variavel
                   possiveis_respostas=None):
    if dados == None:
        return "ERRO - Lista de dados não fornecida"
    ID_variavel = len(dados[0])-1

    ocorrencias_restantes = list(ocorrencias_restantes) #transforma em array mutável, por garantia
    if possiveis_respostas is None:
        possiveis_respostas = [str(x) for x in range(len(respostas))] # Usa a global como fallback
    if min_ganho <= 0:
        min_ganho = 0
    ID_resposta = len(dados[0])-1

    temp_contagem = [0] * len(possiveis_respostas)
    for linha in dados:
        temp_resposta = linha[ID_resposta]
        temp_contagem[temp_resposta] += 1
    contagem_respostas = tuple(temp_contagem) #tupla de n de vezes que cada resposta (ID) aparece
    del temp_contagem, temp_resposta

    contagem_respostas_total = len(dados)

    gini_pai = 1 - sum((x/contagem_respostas_total)**2 for x in contagem_respostas)

    resposta_mais_frequente = possiveis_respostas[contagem_respostas.index(max(contagem_respostas))]

    #Primeiro limitador: se o ganho minimo for impossivel de alcançar, nao gera no de decisao
    if gini_pai < min_ganho:
        return "NodeDecisao(decisao_final="+str(resposta_mais_frequente)+")"
    
    #Segundo limitador: número mínimo de registros para gerar um nó de decisão
    if contagem_respostas_total < min_registros:
        return "NodeDecisao(decisao_final="+str(resposta_mais_frequente)+")"

    melhor_ganho = 0

    ID_variaveis_restantes = [] #armazena os ponteiros
    for x in range(len(ocorrencias_restantes)):
        if ocorrencias_restantes[x]:  #se for diferente de 0
            ID_variaveis_restantes.append(x)
        
    melhor_pos_linha = 0
        
    for ID_variavel in ID_variaveis_restantes:
        dados_ordenados = sorted(dados, key=lambda x: x[ID_variavel])

        contagem_respostas_verdadeiro = list(contagem_respostas) #copia a lista de variaveis completa
        contagem_respostas_falso = [0] * len(contagem_respostas)

        contagem_respostas_verdadeiro_total = len(dados_ordenados) #conta numericamente o total de respostas presentes na parte aceita do corte
        contagem_respostas_falso_total = 0

        valor_corte = 0 #No caso de haver lista inteira com apenas um estado, sem variação

        for pos_linha in range(1, contagem_respostas_total): #é essencialmente o comprimento da lista

            contagem_respostas_verdadeiro[dados_ordenados[pos_linha-1][ID_resposta]] -= 1 #--> Move uma variavel por vez
            contagem_respostas_falso[dados_ordenados[pos_linha-1][ID_resposta]] += 1      #/

            contagem_respostas_verdadeiro_total -= 1
            contagem_respostas_falso_total += 1

            if dados_ordenados[pos_linha-1][ID_variavel] != dados_ordenados[pos_linha][ID_variavel]: #Caso tenha alcançado o corte
                valor_corte = int((dados_ordenados[pos_linha-1][ID_variavel] + dados_ordenados[pos_linha][ID_variavel])/2)

                ganho = gini_pai - ((contagem_respostas_verdadeiro_total/contagem_respostas_total) * (1 - sum((resposta/contagem_respostas_verdadeiro_total)**2 for resposta in contagem_respostas_verdadeiro))
                                    + (contagem_respostas_falso_total/contagem_respostas_total) * (1 - sum((resposta/contagem_respostas_falso_total)**2 for resposta in contagem_respostas_falso)))
                
                if ganho > melhor_ganho:
                    melhor_ID_variavel = ID_variavel
                    melhor_corte = valor_corte
                    melhor_ganho = ganho
                    melhor_pos_linha = pos_linha
                    melhor_dados_ordenados = dados_ordenados
    
    if melhor_ganho > min_ganho:
        melhor_lista_verdadeiro = melhor_dados_ordenados[melhor_pos_linha:]
        melhor_lista_falso = melhor_dados_ordenados[:melhor_pos_linha]

        ocorrencias_restantes[melhor_ID_variavel] -= 1

        return "NodeDecisao(ID_variavel="+str(melhor_ID_variavel)+", limiar="+str(melhor_corte)+", esquerda="+treinar_arvore(dados=melhor_lista_verdadeiro, min_registros=min_registros, min_ganho=min_ganho, ocorrencias_restantes=ocorrencias_restantes, possiveis_respostas=possiveis_respostas)+", direita="+treinar_arvore(dados=melhor_lista_falso, min_registros=min_registros, min_ganho=min_ganho, ocorrencias_restantes=ocorrencias_restantes, possiveis_respostas=possiveis_respostas)+")"
    
    return "NodeDecisao(decisao_final="+str(resposta_mais_frequente)+")"