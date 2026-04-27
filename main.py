"""#[>------- Identificações dos Sensores -------<]
#    Usado por todas as identificaçoes ao     #|
#  longo do código                            #|
#                                             #|
ID_cronometro_rega     = 0                    #|
ID_luminosidade        = 1                    #|
ID_temperatura         = 2                    #|
ID_umidade_solo        = 3                    #|
ID_umidade_atmosferica = 4                    #|
ID_ativacao            = 5                    #|
#                                             #|
dados_entrada = [None, #cronometro_rega       #|
                 None, #luminosidade          #|
                 None, #temperatura           #|
                 None, #umidade_solo          #|
                 None] #umidade_atmosferica   #|
#                                             #|
fator_precisao = 100 #Para dados dos sensores #|
#                                             #|
# OBS: O fator de precisão deve ser maior     #|
#     que a maioria se não todas as divisões  #|
#     de corte para não reduzir precisão.     #|
#                                             #|
max_ocorrencias = (1, #cronometro_rega        #|
                   1, #luminosidade           #|
                   2, #temperatura            #|
                   1, #umidade_solo           #|
                   1) #umidade_atmosferica    #|
#                                             #|
#[>-------------------------------------------<]


#[>------- Identificação das Respostas -------<]
#    Define diferentes respostas a depender   #|
#  do valor médio exibido nas listas finais   #|
#                                             #|
respostas = ["Não regar", #-> 0               #|
             "Regar"] #-----> 1               #|
#                                             #|
#[>-------------------------------------------<]"""

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

#class NodeDecisao:
#    def __init__(self,
#                 ID_variavel=None, #-> Define qual o tipo de variável usada por sua posição de identificação na lista
#                 limiar=None, #--------> Define onde será a "divisão de decisão". Será usado o sinal " > ".
#                 esquerda=None, #--------> Define o que será feito caso a decisão retorne VERDADEIRO
#                 direita=None, #-----------> Define o que será feito caso a decisão retorne FALSO
#                 decisao_final=None): #------> Caso seja um Nó-Folha, define a decisão final tomada

#def treinar_arvore(dados, #lista ATUAL de dados
#                   min_registros=0,
#                   min_ganho=0.0,
#                   ocorrencias_restantes=[-1 for x in max_ocorrencias], #lista de valores maximos de ocorrencia de cada variavel
#                   possiveis_respostas=None):

import csv

from modulodecisao import NodeDecisao
from funcaotreinamento import treinar_arvore

nome_arquivo_entrada = "biblioteca_dados.csv"
delimitador_entrada = "|"

nome_arquivo_saida = "arvore_decisao.txt"

with open(nome_arquivo_entrada, mode="r", newline='', encoding="utf-8") as arquivo:
    leitor_csv = csv.reader(arquivo, delimiter=delimitador_entrada)

    cabecalho = next(leitor_csv)

    #suporta apenas se for um valor INTEIRO
    dados = [[int(item) for item in linha] for linha in leitor_csv]

    arvore = treinar_arvore(dados=dados
                            ,min_registros=0
                            ,min_ganho=0.00
                            ,ocorrencias_restantes=max_ocorrencias
                            ,possiveis_respostas=respostas)

with open(nome_arquivo_saida, mode="w", newline='', encoding="utf-8") as arquivo:
    arquivo.write(arvore)

print("\n- Treinamento de Árvore finalizado! Resultado salvo em \"" + nome_arquivo_saida + "\". Prévia:\n\n   ", arvore, "\n", sep='')
