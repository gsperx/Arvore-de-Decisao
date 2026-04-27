#[>------- Identificações dos Sensores -------<]
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
#[>-------------------------------------------<]



class NodeDecisao:
    def __init__(self,
                 ID_variavel=None, #-> Define qual o tipo de variável usada por sua posição de identificação na lista
                 limiar=None, #--------> Define onde será a "divisão de decisão". Será usado o sinal " > ".
                 esquerda=None, #--------> Define o que será feito caso a decisão retorne VERDADEIRO
                 direita=None, #-----------> Define o que será feito caso a decisão retorne FALSO
                 decisao_final=None): #------> Caso seja um Nó-Folha, define a decisão final tomada
        
        self.ID_variavel = ID_variavel
        self.limiar = limiar
        self.esquerda = esquerda
        self.direita = direita
        self.decisao_final = decisao_final

    def checar_se_folha(self):
        return self.decisao_final is not None #---> Caso haja qualquer decisao final, é um Nó-Folha.        

    def previsao(self, dados=None):
        if self.checar_se_folha(): #---> Caso seja um nó-folha, retorna o valor nele.
            return self.decisao_final
        
        if dados == None:
            return "Erro em NodeDecisao - Sem lista de Dados"
        
        else:   
            if dados[self.ID_variavel] > self.limiar:
                return self.esquerda.previsao(dados)

            else:
                return self.direita.previsao(dados)