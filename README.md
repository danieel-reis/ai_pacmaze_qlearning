# Resolvedor do 8-puzzle utilizando Inteligência Artificial com Aprendizado por Reforço (QLearning)

O presente trabalho consiste em implementar e comparar um labirinto simpliﬁcado do Jogo Pac-Man chamado Pac-Maze. O objetivo geral é exercitar o básico sobre aprendizado por reforço apresentado durante o curso da disciplina de Inteligência Artiﬁcial ministrado pelo professor Luiz Chaimowicz.

## Cénario: Arquivo de entrada
O cenário é um mundo bidimensional, representado por uma matriz de caracteres. A pastilha é representada por 0 (zero), um fantasma por & (e comercial), uma parede por #, e um espaço vazio por -.

## Modelagem
O mundo é modelado como um MDP <S, A, R, T> com as seguintes características:

* S: conjunto de estados são as posições onde o agente pode estar (-, 0 ou &);
* A: conjunto de ações: acima (U), abaixo (D), esquerda (L) e direita (R);
* R: a função de recompensa é a seguinte: em - a recompensa é -1, em 0 a recompensa é 10 (pílula!) e em & a recompensa é -10 (fantasma!). Isso vai incentivar o Pac-Man a encontrar o menor caminho até a pílula, evitando fantasmas; 
* T: para facilitar, a função de transição é determinística: o agente consegue se mover na direção desejada. Por exemplo, a ação “U” em (3,1) leva o agente a (2,1). Se tentar se mover para uma parede, o Pac-Man não se desloca e recebe (novamente) a recompensa do estado onde está. Dessa forma, o mundo foi armazenado por meio de uma matriz contendo em cada posição um valor (#, -, 0 ou &) que referem-se respectivamente a (parede, espaço vazio, pílula e fantasma); as ações por um vetor ["L","R","U","D"] e a Q-Table como um dicionário do python, contendo uma tupla (estado [x,y] na matriz, ação, movimento realizado e recompensa).

## Carregando a instância do mundo
Lê as linhas do arquivo de entrada, identiﬁca as dimensões do mundo, cria uma matriz de tamanho das dimensões e preenche a matriz com as informações lidas.

## Posicionando o agente num local aleatório
Gera uma posição aleatória e veriﬁca se ela é válida (ou seja, é um espaço vazio). Dessa forma, faz isso até que escolha uma posição válida.

## Retornando o q-valor para um par estado x ação
Retorna o Q-valor para um par estado x ação da tabela ou zero, simplesmente porque a Q-Table é um dicionário do python, ou seja, o elemento procurado pode não está lá. Caso não esteja, o valor retornado é zero.

## Retornando uma ação escolhida
Gera um valor aleatório entre 0 e 1. Se ele for menor que um epsilon, explora, ou seja, apenas retorna uma ação aleatória dentre as possiveis ações. Senão, exploita. No processo de exploitar, o que se faz é armazenar em q os valores da qTable para a ação solicitada e as possíveis ações a serem realizadas a partir desse estado, e a partir disso encontrar o maior q. Nisso, temos dois casos (empate ou não), ou seja, duas ou mais opções podem ser a melhor. Quando temos empate, o que se faz é escolher aleatoriamente dentre as ações empatadas.

## Calculando a recompensa
Seleciona o elemento na posição determinada e retorna a recompensa de acordo com o tipo da célula (Viver no mundo, pílula ou fantasma)
* REWARD_PILL = 10 => Recompensa da pílula;
* REWARD_GHOST = -10 => Recompensa do fantasma;
* REWARD_SPACEFREE = -1 => Recompensa do espaço vazio (viver no mundo).

## Aprendendo
Dado um estado 1, uma ação 1 e uma recompensa, o agente aprende qual a ação ele deve tomar. Para isso, guarda o Q-valor máximo entre as ações do estado 2 e o Qvalor atual para o estado 1 com uma ação 1 ou nulo caso não exista e calcula o novo Q-valor, de forma que se o Q-valor atual for nulo, retorna o valor da recompensa imediata. Senão, calcula o novo valor poderado. Por ﬁm, atualiza o valor do novo Q-valor para aquele par estado e ação.

## Movimentando o agente
Armazena o índice da posição atual e analisa o movimento escolhido (esquerda, direita, cima ou baixo). Caso seja possível realizá-lo (a posição seja válida e não seja uma parede, realiza o movimento e retorna True. Caso contrário, retorna False.

## Ordenando, salvando e exibindo a Q-table
Ordena a q-table pelo valor de x,y, atualiza a q-table com a ordenação, agrupa os valores no formato (h, w, moviment, qvalue) em que:
* "h" representa a posição na altura da matriz;
* "w" representa a posição na na largura da matriz;
* "moviment" representa o movimento realizado;
* "qvalue" representa o Q-Valor na tabela. Por ﬁm, salva os dados agrupados no arquivo de saída (denominado "q.txt").

## Computando, salvando e exibindo a política ótima
Cria a matriz de política a partir de um clone do mundo, em que percorre cada posição do mundo e veriﬁca:
* Se for uma parede, preenche com (valor, INFINITO);
* Se não preenche com (espaço livre, -INFINITO). A utilização do INFINITO E -INFINITO se justiﬁca para permitir posteriormente computar o menor elemento. Portanto, percorre a Q-Table, e se o q-valor anterior (presente na política) for maior que o atual, atualiza a política para o atual, pois ele é maior, já que o objetivo é maximizar a recompensa esperada. Nesse processo, os dadosdapolíticaótimaobtidasãosalvosnoarquivodesaída(denominado"pi.txt").


## Executando um episódio
Cada episódio, consiste em setar o agente numa posição aleatória válida e ﬁca num loop:
* Calcula a recompensa imediata da posição atual;
* Seleciona uma ação a partir do estado atual;
* Realiza movimento do agente => realiza a ação escolhida caso seja possível e aprende; Vale ressaltar, que o que marca o ﬁm de um episódio é o ato de chegar ao estado terminal. Dessa forma, os episódios são realizados n vezes com os parâmetros lidos determinados (alpha, gamma, epsilon, n).

## Testes de execução
Entradas de exemplo:
* "pacmaze.txt";
* "pacmaze-01-tiny.txt";
* "pacmaze-02-mid-sparse.txt";
* "pacmaze-03-tricky.txt".

Para cada arquivo, pode-se usar as combinações geradas pelas seguintes conﬁgurações:
* Alpha: [0.1, 0.3, 0.5, 0.9]
* Epsilon: [0.1, 0.5, 0.9]
* Gamma ﬁxo = 0.9
* N = Número de execuções => varia de acordo com a instância