# Importando as dependências do QuNetSim:
from qunetsim.components import Host, Network
from qunetsim.objects import Logger

Logger.DISABLE = False

# Funções do QKD
from B92 import sender_QKD, receiver_QKD, sniffing_QKD

# Funções da Criptografia e da Chave
from Cryptography_Algorithm import generate_key, encrypt_file, decrypt_file, key_to_binary, binary_to_key

# Funções para o envio da mensagem
from Send_Message import get_local_path, move_file

# Obtendo o local/caminho onde o programa está sendo executado
path = get_local_path()

from time import sleep

# Função Main
def main():

  # Inicializando a rede e estabelecendo as conexões.
  network = Network.get_instance()
  nodes = ['Alice', 'Node2', 'Node3', 'Node4', 'Eve', 'Node6', 'Node7', 'Node8', 'Node9', 'Node10', 'Node11', 'Bob']

  network.delay = 0
  network.start(nodes)

  host_Alice = Host('Alice')
  host_n2 = Host('Node2')
  host_n3 = Host('Node3')
  host_n4 = Host('Node4')
  host_Eve = Host('Eve')
  host_n6 = Host('Node6')
  host_n7 = Host('Node7')
  host_n8 = Host('Node8')
  host_n9 = Host('Node9')
  host_n10 = Host('Node10')
  host_n11 = Host('Node11')
  host_Bob = Host('Bob')

  hosts = [host_Alice, host_n2, host_n3, host_n4, host_Eve, host_n6, host_n7, host_n8, host_n9, host_n9, host_n10, host_n11, host_Bob]
        
  host_Alice.add_connection('Node2')
  host_n2.add_connections(['Alice', 'Node3'])
  host_n3.add_connections(['Node2', 'Node4'])
  host_n4.add_connections(['Node3', 'Eve'])
  host_Eve.add_connections(['Node4', 'Node6'])
  host_n6.add_connections(['Eve', 'Node7'])
  host_n7.add_connections(['Node6', 'Node8'])
  host_n8.add_connections(['Node7', 'Node9'])
  host_n9.add_connections(['Node8', 'Node10'])
  host_n10.add_connections(['Node9', 'Node11'])
  host_n11.add_connections(['Node10', 'Bob'])
  host_Bob.add_connection('Bob')

  for node in hosts:
    node.start()

  network.add_hosts(hosts)

  interception = input(
    "Deseja que a rede possa ser espionada? 'S' para sim, 'N' para não: ")
  while not interception.upper() in ['S', 'N']:
    interception = input("Insira 'S' ou 'N': ")
  interception = interception.upper()

  if interception == 'S':
    # Se há ou não sniff
    host_Eve.q_relay_sniffing = True
    # A função a ser aplicada aos qubits em trânsito.
    host_Eve.q_relay_sniffing_fn = sniffing_QKD

  def sender_protocol(sender):
    # Gerando a chave AES
    key = generate_key()
    
    # Convertendo key para binário
    key_binary = key_to_binary(key)
    key_size = str(len(key_binary))

    # Enviando o tamanho da chave
    sender.send_classical(host_Bob.host_id, key_size)
    print(f"Remetente - Chave Gerada: {key}")

    # Executando a função de envio QKD
    sender_QKD(sender, host_Bob, key_binary)

    sleep(2)

    # Criptografando a mensagem
    name = input("Digite o nome do arquivo que deseja enviar: ")
    message = f'{path}/alice/{name}'
    encrypt_file(message, key)
    sender.send_classical(host_Bob.host_id, name)

    # "Enviando" a mensagem criptografada para Bob
    print("Enviando mensagem secreta")
    sleep(10)
    source_file = f'{message}.encrypted'
    destination = f'{path}/bob'
    move_file(source_file, destination)


  def receiver_protocol(receiver):
    # Recebedno o tamanho da chave.
    key_size = receiver.get_next_classical(host_Alice.host_id).content
    key_size = int(key_size)
    print(f"Receptor - Tamanho da chave recebida: {key_size}")

    # Executando a função QKD de recebimento da chave
    key_received = receiver_QKD(receiver, host_Alice, key_size)
    
    # Convertendo de binário para chave
    binary_key = binary_to_key(key_received)
    print(f'Receptor - A chave recebida foi: {binary_key}')

    # Decriptando a mensagem com a chave adquirida
    message = receiver.get_next_classical(host_Alice.host_id).content + '.encrypted'
    source_file = f'{path}/bob/{message}'
    
    # Espera um pouquinho...
    sleep(15)
    decrypt_file(source_file, binary_key)


  # Executando os protocolos
  host_Alice.run_protocol(sender_protocol, ())
  host_Bob.run_protocol(receiver_protocol, (), blocking=True)

  # Para a rede no final do exemplo
  network.stop(True)
  exit()

if __name__ == '__main__':
  main()
    



    
