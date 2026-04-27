import csv
from random import randint

nome_arquivo = "biblioteca_dados.csv"
delimitador = '|' #caractere separador
espacamento = 1 #define o espaço entre o separador e o item


#o cabeçalho já começa espaçado, para facilitar a leitura durante homogeneização de comprimento
cabecalho = ["conectado", "voltagem", "temperatura", "ruido", "ativacao"] 

#========================================================> Geração de dados de teste <========================================================
numero_iteracoes = 10000
fator_precisao = 10
fator_seguranca = 1000
dados = []
comprimento_grafico = 100
for n in range(1, numero_iteracoes+1):
    conectado = int(randint(0, 1) * fator_seguranca)
    voltagem = int(randint(25, 45) * fator_seguranca)
    temperatura = int(randint(-100, 600) * fator_seguranca)
    ruido = int(randint(-100, 100) * fator_seguranca)

    if conectado == 1 * fator_seguranca and voltagem <= 42 * fator_seguranca and temperatura > 0 and temperatura < 450 * fator_seguranca:
        ativar = 1
    else:
        ativar = 0

    dados.append([conectado, voltagem, temperatura, ruido, ativar])
    
    
    print("[" + round(comprimento_grafico*n/numero_iteracoes) * '■' + (comprimento_grafico - round(comprimento_grafico*n/numero_iteracoes)) * '□' + f"] - Iteração nº{n}", sep = '', end = ('\r' if n != numero_iteracoes else ''))
#=============================================================================================================================================

#abre o arquivo no modo 'a+' para que ele seja criado caso não existente,
#caso exista, adiciona sobre o conteúdo, alem de permitir controle de cursor.
with open(nome_arquivo, mode='a+', newline='', encoding="utf-8") as arquivo:


    #gera a variavel escritora do modulo, usando o delimitador definido
    escritor_csv = csv.writer(arquivo, delimiter=delimitador)


    #move o cursor de leitura para o primeiro bit
    arquivo.seek(0)
    #se não houver nada escrito (arquivo recem-criado), adiciona o cabeçalho
    if arquivo.readline() == '':
        escritor_csv.writerow(cabecalho)

    escritor_csv.writerows(dados)