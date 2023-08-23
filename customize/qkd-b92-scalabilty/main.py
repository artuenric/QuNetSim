"""
Realiza mútiplas execuções simultâneas de QKD em uma rede com topologia em linha com, ou sem, um interceptador.
No terminal, utiliza-se `python3 > log.txt` para guardar as saídas do código em um arquivo chamado log.txt que será utilizado para criação de gráficos.
"""

# Importando as dependências do QuNetSim:
from qunetsim.components import Host, Network
from qunetsim.objects import Logger, Qubit

# Funções do QKD
from b92 import sniffing_QKD, choice, running_concurrently

# Funções para colher os dados e plotar o gráfico.
from plot import organize

# Demais dependências
from time import sleep


def main():
  Logger.DISABLED = True
  # Inicializando a rede e estabelecendo as conexões.
  network = Network.get_instance()
  network.delay = 0
  nodes = ['Node1', 'Node2', 'Node3', 'Node4', 'Node5', 'Node6', 'Node7', 'Node8', 'Node9', 'Node10', 'Node11', 'Node12']
  network.start(nodes)

  host_n1 = Host('Node1')
  host_n2 = Host('Node2')
  host_n3 = Host('Node3')
  host_n4 = Host('Node4')
  host_n5 = Host('Node5')
  host_n6 = Host('Node6')
  host_n7 = Host('Node7')
  host_n8 = Host('Node8')
  host_n9 = Host('Node9')
  host_n10 = Host('Node10')
  host_n11 = Host('Node11')
  host_n12 = Host('Node12')

  # Criando lista com os nós da rede
  hosts = [host_n1, host_n2, host_n3, host_n4, host_n5, host_n6, host_n7, host_n8, host_n9, host_n10, host_n11, host_n12]
  
  # Adicionando as conexões entre os nós da rede. A rede se parece com isso: (N1) <--> (N2) <--> ... <--> (N11) <--> (N12)
  for i, node in enumerate(hosts):
    if i == 0:
      node.add_connection(hosts[1].host_id)
    elif i < len(hosts)-1:
      node.add_connection(hosts[i-1].host_id)
      node.add_connection(hosts[i+1].host_id)
    else:
      node.add_connection(hosts[i-1].host_id)
      
  # Inicializando os Hosts
  for node in hosts:
    node.start()

  # Adicionando os hosts à rede  
  network.add_hosts(hosts)
  
  # Plotando o grafo da rede
  # network.draw_classical_network()
  
  # Definindo se a rede deve ou não ser espionada
  # interception = input("Deseja que a rede possa ser espionada? (S/N): ")
  interception = 'S'
  while not interception.upper() in ['S', 'N']:
    interception = input("Insira 'S' ou 'N': ")
  interception = interception.upper()

  # Definindo o número de execuções do protocolo
  execs = '4'

  # Escolhendo aleatoriamente quem participa das comunicações
  senders, receivers, sniffers = choice(hosts, execs)

  # Se a rede deve ter interceptação:
  if interception == 'S':
    for pair, sniffer in zip(list(sniffers.keys()), list(sniffers.values())):
      if sniffer != 'None':
        # Se há ou não sniff
        hosts[sniffer-1].q_relay_sniffing = True
        # A função a ser aplicada aos qubits em trânsito.
        hosts[sniffer-1].q_relay_sniffing_fn = sniffing_QKD
    
  # Executando os protocolos simultaneamente e colhendo os dados
  infos, generated_keys, received_keys = running_concurrently(senders, receivers)  
  print(infos)
  
  # Visualizar quais os hosts escolhidos
  organize(generated_keys)
  print(generated_keys)
  
  # Tempo fornecido para a execução de todos os protocolos
  sleep(60)
  
  organize(received_keys)
  print(received_keys)
  # Para a rede no final do exemplo
  network.stop(True)
  exit()

if __name__ == '__main__':
  main()