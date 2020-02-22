#Aluno: Daniel Martins Reis

import random
import math
import time
import os
import sys
    
class QLearn:
    def __init__(self, filename, epsilon, alpha, gamma):
        self.execution = 1                  #Contador de execução
        self.filename = filename            #Nome do arquivo
        self.filenameOutQ = "q.txt"
        self.filenameOutP = "pi.txt"
        
        self.width = 0                      #Dimensão do mundo => largura
        self.height = 0                     #Dimensão do mundo => altura
        self.world = []                     #Mundo
        self.policy = []                    #Política
        
        self.qTable = {}                    #Tabela que mapeia ação x recompensa
        self.epsilon = epsilon              #E-greedy
        self.alpha = alpha                  #Coeficiente de aprendizado
        self.gamma = gamma                  #Ponderação do futuro
        
        self.actions = ['L','R','U','D']    #Ações
        self.state = (0,0)                  #Posição do agente no mundo
        self.lastState = None               #Último estado
        self.sumRewardEpisode = 0           #Soma das recompensas de um episódio
        self.sumRewardDiscountedEpisode = 0 #Soma das recompensas discontadas pelos fatores de um episódio
        self.contRewardEpisode = 0          #Contador de vezes que chegou ao estado objetivo de um episódio
        
        self.WALL = '#'                     #Parede
        self.PILL = '0'                     #Pílula
        self.GHOST = '&'                    #Fantasma
        self.SPACEFREE = '-'                #Espaço livre
        self.REWARD_PILL = 10               #Recompensa => pílula
        self.REWARD_GHOST = -10             #Recompensa => fantasma
        self.REWARD_SPACEFREE = -1          #Recompensa => espaço vazio (viver no mundo)
        
    #Posiciona o agente inicialmente em um local aleatório
    def defineRandomPositionAgent(self):
        #Gera uma posição aleatória respeitando o intervalo de tamanho do mundo
        x = random.randint(0, self.height-1)
        y = random.randint(0, self.width-1)
        #Seta o estado
        self.state = (x, y)
        #Armazena o elemento correspondente a posição gerada no mundo
        element = self.world[self.state[0]][self.state[1]]
        
        #Enquanto a posição inicial do agente gerada aleatoriamente não for um lugar vazio
        while (element is not self.SPACEFREE):
            #Gera uma posição aleatória respeitando o intervalo de tamanho do mundo
            x = random.randint(0, self.height-1)
            y = random.randint(0, self.width-1)
            #Seta o estado
            self.state = (x, y)
            #Armazena o elemento correspondente a posição gerada no mundo
            element = self.world[self.state[0]][self.state[1]]
            
    #Carrega a instância do mundo
    def loadWorld(self):
        #Acessa o arquivo
        dataFile = open(self.filename, 'r')
        #Acessa a primeira linha do arquivo
        firstLine = dataFile.readline()
        
        #Identifica as dimensões do mundo
        l = firstLine.split(" ")
        self.height = int(l[0])
        self.width = int(l[1])
        
        #Acessa o conteúdo do arquivo
        dataContent = dataFile.readlines()
        
        #Percorre cada linha do arquivo
        for line in dataContent:
            #Identifica os elementos
            self.world.append(line)
        
        #Fecha o arquivo
        dataFile.close()
        
    #Retorna o q-valor para um estado e ação
    def getQValue(self, state, action):
        #Retorna o Q-valor para um estado e uma ação da tabela ou zero caso seja nulo
        return self.qTable.get((state, action), 0.0)

    #Dado o estado atual retorna uma ação escolhida
    def chooseAction(self):
        #Gera um valor aleatório entre 0 e 1. Se ele for menor que um epsilon, explora
        if random.random() < self.epsilon:
            #Retorna uma ação aleatória dentre as possíveis ações
            return random.choice(self.actions)
        #Senão, exploita
        else:
            #Armazena em q os valores da qTable para a ação solicitada e as possíveis ações a serem realizadas a partir desse estado
            q = [self.getQValue(self.state, a) for a in self.actions]
            #Armazena o maior q => leva ao estado que maximiza
            maxq = max(q)
            #Seleciona uma ação x => Se dentre os possíveis q-valores houver empate entre os que maximizam
            if q.count(maxq) > 1:
                #Mapeia em best uma lista contendo as ações que respondem ao valor máximo
                best = [x for x in range(len(self.actions)) if q[x] == maxq]
                #Obtém o índice da ação escolhida => escolha aleatória dentre as melhores ações (best)
                indexActionSelected = random.choice(best)
            #Seleciona uma ação x => Se dentre os possíveis q-valores não houver empate entre os que maximizam
            else:
                #Obtém o índice da ação escolhida => ação que maximiza
                indexActionSelected = q.index(maxq)
            #Retorna a ação de índice selecionado
            return self.actions[indexActionSelected]
    
    #Calcula recompensa
    def calcReward(self):
        #Seleciona o elemento na posição determinada
        element = self.world[self.state[0]][self.state[1]]
        #Calcula a recompensa
        reward = 0
        if (element == self.SPACEFREE):
            reward = self.REWARD_SPACEFREE      #Viver no mundo
        elif (element == self.PILL):
            reward = self.REWARD_PILL           #Pílula
        elif (element == self.GHOST):
            reward = self.REWARD_GHOST          #Fantasma
        #Retorna a recompensa calculada
        return reward

    #Aprende => Dado um estado 1, uma ação 1 e uma recompensa, aprende qual a ação ele deve tomar
    def learn(self, state1, action1, reward, state2):
        #Q-valor atual para o estado 1 com uma ação 1 ou nulo caso não exista
        oldqvalue = self.qTable.get((state1, action1), None)
        #Calcula o novo Q-valor -> Se oldqvalue for nulo, retorna o valor da recompensa, senão calcula o novo valor poderado
        if oldqvalue is None:
            newqvalue = reward
            #Conta a recompensa recebida
            self.sumRewardEpisode = self.sumRewardEpisode + reward
            self.sumRewardDiscountedEpisode = self.sumRewardDiscountedEpisode + reward
            self.contRewardEpisode = self.contRewardEpisode + 1
        else:
            #Q-valor máximo entre as ações do estado 2
            maxqTable = max([self.getQValue(state2, a) for a in self.actions])
            #Calcula a recompensa recebida
            received = self.alpha * (reward + self.gamma * maxqTable - oldqvalue)
            newqvalue = oldqvalue + received
            #Conta a recompensa recebida
            self.sumRewardEpisode = self.sumRewardEpisode + reward
            self.sumRewardDiscountedEpisode = self.sumRewardDiscountedEpisode + newqvalue
            self.contRewardEpisode = self.contRewardEpisode + 1

        #Atualiza o valor do novo Q-valor para aquele estado e ação
        self.qTable[(state1, action1)] = newqvalue
    
    #Realiza movimento do agente => Retorna True caso seja realizado o movimento e False caso contrário
    def moveAgent(self, action):
        #Armazena o índice da posição atual
        h = self.state[0]
        w = self.state[1]
        
        #Movimento para esquerda
        if (action is self.actions[0] and w-1 >= 0 and self.world[h][w-1] is not self.WALL):
            self.lastState = self.state
            self.state = (h,w-1)
            return True
            
        #Movimento para direita
        elif (action is self.actions[1] and w+1 < self.width and self.world[h][w+1] is not self.WALL):
            self.lastState = self.state
            self.state = (h,w+1)
            return True
           
        #Movimento para cima
        elif (action is self.actions[2] and h-1 >= 0 and self.world[h-1][w] is not self.WALL):
            self.lastState = self.state
            self.state = (h-1,w)
            return True
        
        #Movimento para baixo
        elif (action is self.actions[3] and h+1 < self.height and self.world[h+1][w] is not self.WALL):
            self.lastState = self.state
            self.state = (h+1,w)
            return True
        
        return False
    
    #Exibe um cabeçalho
    def printHead(self):
        #Limpa o console
        #os.system('cls' if os.name == 'nt' else 'clear')
        
        #Exibe os dados
        print("--------------------------------------------------------------------------------")
        print("Developer: Daniel Reis")
        print("--------------------------------------------------------------------------------")
        
    #Exibe a execução atual
    def printExecution(self):
        #Exibe os dados
        print("Execution: " + str(self.execution))
        print("--------------------------------------------------------------------------------")

    #Exibe os dados do mundo no momento
    def printWorld(self):
        #Exibe o mundo
        print("--------------------------------------------------------------------------------")
        for h in range(self.height):                    #Para cada linha da matriz
            print("|", end = "")
            for w in range(self.width):                 #Para cada coluna dessa linha
                if (h is self.state[0] and w is self.state[1]):
                    print("X|", end = "")
                else:
                    print(self.world[h][w] + "|", end = "")
            print("")
        print("--------------------------------------------------------------------------------")
    
    #Exibe a posição atual do agente no mundo
    def printAgentPositionNow(self):
        #Exibe os dados
        print("Position agent now: (" + str(self.state[0]) + "," + str(self.state[1]) + ")")
        
    #Exibe a Q-table
    def printQTable(self):
        print("-------------------------------------QTABLE-------------------------------------")
        #Exibe
        for x in self.qTable:
            print(str(x[0][0]) + "," + str(x[0][1]) + "," + x[1] + "," + "{:.3f}".format(self.qTable[x]))
        print("--------------------------------------------------------------------------------")

    #Ordena e exibe a Q-table
    def sortAndPrintQTable(self): 
        #Ordena a q-table pelo valor de x,y
        sortedqTable = sorted(self.qTable.items(), key=lambda kv: kv[0][0])
        #Atualiza a q-table com a ordenação
        self.qTable = sortedqTable
        
        #Cria o arquivo
        fileoutq = open(self.filenameOutQ, 'w')
        
        #Exibe => Percorre o dictionary da QTable
        for x in self.qTable:
            #Separa os valores
            h = x[0][0][0]
            w = x[0][0][1]
            moviment = x[0][1]
            qvalue = x[1]
            #Agrupa os valores no formato (h,w,moviment,qvalue)
            value = str(h) + "," + str(w) + "," + moviment + "," + "{:.3f}".format(qvalue)
            
            #Escreve no arquivo
            fileoutq.write(value + "\n")
            #Exibe no console
            print(value)
            
        #Fecha o arquivo
        fileoutq.close()
            
    #Computa e exibe a política ótima
    def computyAndPrintGreatPolicy(self):
        #Cria clone do mundo
        self.policy = []                                    #Cria matriz
        for h in range(self.height):                        #Para cada linha da matriz
            li = []                                         #Cria uma lista que vai armazenar uma linha da matriz
            for w in range(self.width):                     #Para cada coluna dessa linha
                #Se for uma parede, preenche com (valor, INFINITO), senão preenche com (espaço livre, -INFINITO) para posteriormente computar o menor
                li.append(((self.SPACEFREE, -math.inf) if (self.world[h][w] is self.SPACEFREE) else (self.world[h][w], math.inf)))
            self.policy.append(li)                          #Adiciona a linha criada a matriz

        #Percorre a q-table e gera a tabela
        for x in self.qTable:
            h = x[0][0][0]
            w = x[0][0][1]
            moviment = x[0][1]
            qvalue = x[1]
            #Se o q-valor anterior for maior que o atual, atualiza para o atual, pois ele é maior
            oldqvalue = self.policy[h][w][1]
            if qvalue > oldqvalue:
                self.policy[h][w] = (moviment, qvalue)
                
        #Cria o arquivo
        fileoutp = open(self.filenameOutP, 'w')
        
        #Exibe a política
        print("--------------------------------------------------------------------------------")
        for h in range(self.height):                    #Para cada linha da matriz
            print("|", end = "")
            for w in range(self.width):                 #Para cada coluna dessa linha
                #Escreve no arquivo
                fileoutp.write(self.policy[h][w][0])
                #Exibe no console
                print(self.policy[h][w][0] + "|", end = "")
            #Escreve no arquivo
            fileoutp.write("\n")
            #Exibe no console
            print("")
        print("--------------------------------------------------------------------------------")
   
        #Fecha o arquivo
        fileoutp.close()
        
    #Executa
    def runEpisode(self):
        #Inicializa os contadores        
        self.sumRewardEpisode = 0           #Soma das recompensas de um episódio
        self.sumRewardDiscountedEpisode = 0 #Soma das recompensas discontadas pelos fatores de um episódio
        self.contRewardEpisode = 0          #Contador de vezes que chegou ao estado objetivo de um episódio
        
        while(1):
            #Exibe o cabeçalho
#            self.printHead()

            #Exibe a execução atual
#            self.printExecution()
            
            #Exibe a posição atual do agente no mundo
#            self.printAgentPositionNow()
            
            #Calcula a recompensa imediata da posição atual
            reward = self.calcReward()
#            print("Imediate reward: " + str(reward))
            
            #Seleciona uma ação a partir do estado atual
            action = self.chooseAction()
#            print("Action selected: " + action)
            
            #Realiza movimento do agente => realiza a ação escolhida caso seja possível
            if self.moveAgent(action):
                #Aprende
                self.learn(self.lastState, action, reward, self.state)
            else:
                #Recebe novamente a recompensa do estado que ele está
                self.learn(self.state, action, reward, self.state)
            
            #Exibe qTable
#            self.printQTable()
            
            #Exibe o mundo no momento
#            self.printWorld()
            
            #Se chegou ao estado terminal, finaliza o episódio
            if self.world[self.state[0]][self.state[1]] is self.GHOST or self.world[self.state[0]][self.state[1]] is self.PILL:
                break

class Main:
    #Executa o jogo
    @staticmethod
    def runGame(filenameInput, filenameOutput, epsilon, alpha, gamma, n):
        #Inicializa
        qlearn = QLearn(filenameInput, epsilon, alpha, gamma)
        #Carrega os dados do mundo
        qlearn.loadWorld()
        #Coloca o agente numa posição aleatória
        qlearn.defineRandomPositionAgent()
        #Exibe o mundo no momento
        qlearn.printHead()
#        qlearn.printExecution()
#        qlearn.printAgentPositionNow()
#        qlearn.printWorld()

        #Cria diretório de saída
        filepathOutput = 'out/'
        if not os.path.exists(filepathOutput):
            os.mkdir(filepathOutput)
        #Cria o arquivo
        fileoutp = open(filepathOutput + filenameOutput, 'w')
        #Identifica o nome do arquivo
        filename = filenameInput
        for i in range(0, len(filename)):
            if ("/" in filename):
                filename = filename[1:len(filename)]
            else:
                break
        #Escreve no arquivo
        fileoutp.write(str(filename) + ";" + str(epsilon) + ";" + str(alpha) + ";" + str(gamma) + ";" + str(n) + "\n")
            
        #Realiza n episódios
        for execution in range(n):
            #Coloca o agente numa posição aleatória
            qlearn.defineRandomPositionAgent()
            #Executa o episódio
            qlearn.runEpisode()
            qlearn.execution += 1
            #Contabiliza a recompensa média do episódio
            v1 = qlearn.sumRewardEpisode / qlearn.contRewardEpisode                 #Média das recompensas de um episódio
            v2 = qlearn.sumRewardDiscountedEpisode / qlearn.contRewardEpisode       #Média das recompensas discontadas pelos fatores de um episódio
            #Formata os valores
            a1 = str(qlearn.contRewardEpisode).replace(".", ",")
            a2 = str(v1).replace(".", ",")
            a3 = str(v2).replace(".", ",")
            fileoutp.write(str(execution+1) + ";" + a1 + ";" + a2 + ";" + a3 + "\n")
#            print(v1)
#            print(v2)
            
        #Exibe a QTable ordenada
        qlearn.sortAndPrintQTable()
            
        #Computa e exibe a política ótima
        qlearn.computyAndPrintGreatPolicy()
    
    def runMain(self):
        try:
            #Leitura dos paramêtros de entrada
            filename = sys.argv[1]
            alpha = float(sys.argv[2])
            epsilon = float(sys.argv[3])
            n = int(sys.argv[4])
            gamma = 0.9

            #Executa
            self.runGame(filename, "qlearn_out", epsilon, alpha, gamma, n)
        except:
            print("python3 tp_daniel_reis_qlearning.py \"pacmaze.txt\" 0.3 0.9 300")
            print("    \"pacmaze.txt\" => input file name")
            print("              0.3 => alpha")
            print("              0.9 => epsilon (e-greedy)")
            print("              300 => n (number of executions)")
            print("Note: gamma = 0.9 (default)")
            print("      Output files:")
            print("             q.txt => Q-Table")
            print("            pi.txt => Policy")
            
    #Executa testes automáticos
    def runTests(self):   
        filepathInput = 'in/'
        filepathOutput = 'out/'

        #Executa
        nvalues = [300, 1000, 20000, 25000]
        gamma = 0.9
        totalExecution = 1
        f = 0
        for filename in ["pacmaze.txt", "pacmaze-01-tiny.txt", "pacmaze-02-mid-sparse.txt", "pacmaze-03-tricky.txt"]:
            n = nvalues[f]
            f = f+1
            
            for alpha in [0.1, 0.3, 0.5, 0.9]:
                for epsilon in [0.1, 0.5, 0.9]:
                    for execution in range(totalExecution):
                        #Exibe o que tá executando
                        print(str(execution+1) + " >> " + str(filename) + " " + str(epsilon) + " " + str(alpha) + " " + str(gamma) + " " + str(n))
                        #Executa
                        filenameOutput = "automaticTests_" + str(execution+1) + "_" + str(filename) + "_" + str(alpha) + "_" + str(epsilon) + "_" + str(gamma) + ".csv"
                        self.runGame(filepathInput + filename, filenameOutput, epsilon, alpha, gamma, n)
                        
        #Merge nos arquivos
        files = []
        for alpha in [0.1, 0.3, 0.5, 0.9]:
            for epsilon in [0.1, 0.5, 0.9]:
                files.append("_" + str(alpha) + "_" + str(epsilon) + "_" + str(gamma) + ".csv")
        for filename in ["pacmaze.txt", "pacmaze-01-tiny.txt", "pacmaze-02-mid-sparse.txt", "pacmaze-03-tricky.txt"]:
            #Cria diretório de saída
            filepathOutput = 'out/'
            if not os.path.exists(filepathOutput):
                os.mkdir(filepathOutput)
            #Cria o arquivo
            fout = open(filepathOutput + "merge" + filename + ".csv", 'w')
            #Acessa os dados de todos arquivos
            arq = []
            for name in files:
                arq.append(open(filepathOutput + "automaticTests_1_" + filename + name, 'r'))
            #Captura os dados de todos arquivos
            texto = []
            for a in arq:
                texto.append(a.readlines())
            #Junta os dados e escreve no arquivo de saída
            cont = 0
            for l in range(len(texto[0])):
                tt = ""
                if (cont == 0):
                    for k in range(len(files)):
                        tt = tt + texto[k][l].replace("\n","") + ";" + "\n"
                    cont = 1
                else:
                    for k in range(len(files)):
                        s = texto[k][l].replace("\n","").split(";")
                        for y in range(len(s)):
                            if (y % 2 is not 0):
                                tt = tt + s[y] + ";"
                #Escreve no arquivo de saída
                fout.write(tt + "\n")
#                print(tt)
            #Fecha o arquivo de saída
            fout.close()
           
        #Fecha os arquivos
        for a in arq:
            a.close()
        
if __name__ == "__main__":
    main = Main()
    main.runMain()
#    main.runTests()
