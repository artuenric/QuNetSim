"""
Estas funções permitem alterar a quantidade de nós em uma rede antes da execução dos protocolos em um código, caso isso seja desejado.
O objetivo é testar a escalabilidade do simulador. Por padrão, os nomes dos nós da rede já estarão definidos, de Node1 até Node(n), sendo N o número de nós escolhidos.
"""

def create_nodes(n):
    nodes_list = []
    for node in range(n):
        nodes_list.append(f'Node{node+1}')
    print(nodes_list)

create_nodes(9)