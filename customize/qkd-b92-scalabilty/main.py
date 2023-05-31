# Importando as dependências do QuNetSim:
from qunetsim.components import Host, Network
from qunetsim.objects import Logger, Qubit

# Funções do QKD
from b92 import sniffing_QKD, choice, running_concurrently
from time import sleep
def main():
  Logger.DISABLED = False
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
  interception = 'N'
  while not interception.upper() in ['S', 'N']:
    interception = input("Insira 'S' ou 'N': ")
  interception = interception.upper()

  # Definindo o número de execuções do protocolo
  #execs = input("Quantas execuções simultâneas a rede deve ter? ")
  execs = '50'

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
    
  # Finalmente, executando os protocolos simultaneamente.
  running_concurrently(senders, receivers)
  
  sleep(360)
  # Para a rede no final do exemplo
  network.stop(True)
  exit()

if __name__ == '__main__':
  import sys
  import os

  # Armazena a referência para o stdout original
  stdout_original = sys.stdout
  
  # Obtém o caminho do diretório atual
  path = current_dir = os.path.abspath(os.path.dirname(__file__))

  # Abre o arquivo de texto em modo de escrita
  with open(f'{path}/log.txt', 'w', encoding='utf-8') as arquivo:
      # Redireciona a saída padrão para o arquivo
      sys.stdout = arquivo
      main()
      sys.stdout = stdout_original