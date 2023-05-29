# Importando as dependências do QuNetSim:
from qunetsim.components import Host, Network
from qunetsim.objects import Logger, Qubit

# Funções do QKD
from b92 import sender_QKD, receiver_QKD, sniffing_QKD, running_concurrently

# Função Main
def main():
  
  # Inicializando a rede e estabelecendo as conexões.
  network = Network.get_instance()
  network.delay = 0
  nodes = ['Node1', 'Node2', 'Node3', 'Node4', 'Node5', 'Node6', 'Node7', 'Node8', 'Node9', 'Node10', 'Node11', 'Node12']
  network.start(nodes)

  host_n1 = Host('Node1')
  #host_n1.delay = 1
  host_n2 = Host('Node2')
  #host_n2.delay = 5
  host_n3 = Host('Node3')
  #host_n3.delay = 0.2
  host_n4 = Host('Node4')
  #host_n4.delay = 1.2
  host_n5 = Host('Node5')
  #host_n5.delay = 0.8
  host_n6 = Host('Node6')
  #host_n6.delay = 4
  host_n7 = Host('Node7')
  #host_n7.delay = 0.7
  host_n8 = Host('Node8')
  #host_n8.delay = 0.5
  host_n9 = Host('Node9')
  #host_n9.delay = 0
  host_n10 = Host('Node10')
  #host_n10.delay = 0.2
  host_n11 = Host('Node11')
  #host_n11.delay = 0.3
  host_n12 = Host('Node12')
  #host_n12.delay = 1.5

  hosts = [host_n1, host_n2, host_n3, host_n4, host_n5, host_n6, host_n7, host_n8, host_n9, host_n10, host_n11, host_n12]
  
  # Adicionando as conexões entre os nós da rede. A rede deve se parecer com isso N1<-->N2<-->...<-->N11<-->N12
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
    
  network.add_hosts(hosts)
  
  network.draw_classical_network()
  
  interception = input("Deseja que a rede possa ser espionada? (S/N): ")
  while not interception.upper() in ['S', 'N']:
    interception = input("Insira 'S' ou 'N': ")
  interception = interception.upper()

  if interception == 'S':
    # Se há ou não sniff
    host_n5.q_relay_sniffing = True
    # A função a ser aplicada aos qubits em trânsito.
    host_n5.q_relay_sniffing_fn = sniffing_QKD
  
  
  execs = input("Quantas execuções simultâneas a rede deve ter? ")
  while not execs.isdigit():
    execs = input("Quantas execuções simultâneas a rede deve ter? ")
  execs = int(execs)
  
  running_concurrently(execs, hosts)
  
  # Para a rede no final do exemplo
  network.stop(True)
  exit()

if __name__ == '__main__':
  main()
    