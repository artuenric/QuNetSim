# Importando as dependências do QuNetSim:
from qunetsim.components import Host, Network
from qunetsim.objects import Logger, Qubit

Logger.DISABLE = False

# Funções do QKD
from b92 import sender_QKD, receiver_QKD, sniffing_QKD

# Função Main
def main():

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

  hosts = [host_n1, host_n2, host_n3, host_n4, host_n5, host_n6, host_n7, host_n8, host_n9, host_n9, host_n10, host_n11, host_n12]
        
  for i, node in enumerate(hosts):
    if i == 0:
      node.add_connection(hosts[1].host_id)
    elif 0 > i > len(hosts)-1:
      node.add_connection(hosts[i-1].host_id)
      node.add_connection(hosts[i+1].host_id)
    else:
      node.add_connection(hosts[i-1].host_id)
      
      
  host_n1.add_connection('Node2')
  host_n2.add_connections(['Node1', 'Node3'])
  host_n3.add_connections(['Node2', 'Node4'])
  host_n4.add_connections(['Node3', 'Node5'])
  host_n5.add_connections(['Node4', 'Node6'])
  host_n6.add_connections(['Node5', 'Node7'])
  host_n7.add_connections(['Node6', 'Node8'])
  host_n8.add_connections(['Node7', 'Node9'])
  host_n9.add_connections(['Node8', 'Node10'])
  host_n10.add_connections(['Node9', 'Node11'])
  host_n11.add_connections(['Node10', 'Node12'])
  host_n12.add_connection('Node11')

  for node in hosts:
    node.start()
    print(node.get_connections())

  network.add_hosts(hosts)
  
  q = Qubit(host_n1)
  host_n1.send_qubit(host_n12.host_id, q)
  host_n12.get_qubit(host_n1.host_id, wait=5)
  network.draw_classical_network()
  
"""  interception = input(
    "Deseja que a rede possa ser espionada? 'S' para sim, 'N' para não: ")
  while not interception.upper() in ['S', 'N']:
    interception = input("Insira 'S' ou 'N': ")
  interception = interception.upper()

  if interception == 'S':
    # Se há ou não sniff
    host_n5.q_relay_sniffing = True
    # A função a ser aplicada aos qubits em trânsito.
    host_n5.q_relay_sniffing_fn = sniffing_QKD


  # Executando os protocolos
  host_n1.run_protocol(sender_protocol, ())
  host_Bob.run_protocol(receiver_protocol, (), blocking=True)"""

  # Para a rede no final do exemplo
  

if __name__ == '__main__':
  main()
    



    
