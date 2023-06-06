# Importando as dependências do QuNetSim:
from qunetsim.components import Host, Network
from qunetsim.objects import Logger, Qubit
from random import randint
from time import sleep
import re

Logger.DISABLED = False

def sender_QKD(sender, receiver, execution, key):
  """
    Função de envio da chave QKD B92.

    Args:
        sender (Host): Objeto host que deseja enviar a chave.
        receiver (Host): Objeto host que deseja receber a chave e mensagem.
        key (list): Lista de 0s e 1s que representa a chave quântica.
    """
  
  sent_qubit_counter = 0
  loss_message = 0
  
  for bit in key:
    # Controle do laço.
    success = False

    while success == False:
      qubit = Qubit(sender)
      # Se quisermos enviar 0, enviaremos |0>
      # Se quisermos enviar 1, enviaremos |+>
      if bit == 1:
        qubit.H()
      
      # c8d2bd32-db4a-40d8-9ee0-3294cd321724[execution]
      data = f'{qubit.id}[{execution}]'
      sender.send_classical(receiver.host_id, data, await_ack=True)

      # Enviando o qubit para o receptor.
      sender.send_qubit(receiver.host_id, qubit, await_ack=True)

      # Aguardando a mensagem sobre a escolha da base.
      message = sender.get_next_classical(receiver.host_id, wait=20)

      if message is not None:
        if message.content == f'sucess[{execution}]':
          success = True
          sent_qubit_counter += 1
      else:
        loss_message += 1


def receiver_QKD(receiver, sender, execution, key_size):
  """
    Função de recebimento da chave QKD B92.

    Args:
        sender (Host): Objeto host que deseja enviar a chave.
        receiver (Host): Objeto host que deseja receber a chave e mensagem.
        key (list): Lista de 0s e 1s que representa a chave quântica.
    """

  # Chave adquirida/gerada pelo recptor.
  key_receiver = []
  # Contador de bits medidos corretamente pelo receptor. Controle do laço.
  received_counter = 0
  # Dados de quais qubits se deve tratar
  buffer = []

  while received_counter < key_size:

    # Recebendo informações sobre o qubit que deve ser considerado
    qubit_info = receiver.get_next_classical(sender.host_id)      
    regex = fr'.*/[{execution}/]$'

    # Se a mensagem recebida condiz com esta execução
    if re.fullmatch(regex, qubit_info.content):
      # Add qubit ID no buffer
      buffer.append(qubit_info.content[:36])

    # 0 significa base retilínea e 1 significa base diagonal
    base = randint(0, 1)
    qubit = receiver.get_qubit(sender.host_id, wait=10)

    if qubit is not None:
      if qubit.id in buffer:
        if base == 1:
          qubit.H()
        measure = qubit.measure()
      
        if measure == 1:
          if base == 1:
            resulting_key_bit = 0
          elif base == 0:
            resulting_key_bit = 1
          message_to_send = f'sucess[{execution}]'
          key_receiver.append(resulting_key_bit)
          received_counter += 1
        else:
          message_to_send = f'fail[{execution}]'
          receiver.send_classical(sender.host_id, message_to_send, await_ack=True)
    else:
      receiver.send_classical(sender.host_id, f'none[{execution}]', await_ack=True)
  
  return key_receiver


# Protocolos modularizado com as funções criadas anteriormente
def sender_protocol(sender, receiver, execution):
  """"
  Protocolo QKD para o remetente.
  
  Args:
    sender (Host): Host que deseja enviar a chave com QKD
    receiver (Host): Host que deseja receber a chave com QKD
  """

  key = []
  for bit in range(10):
    key.append(randint(0, 1))
  
  print(f'''{sender.host_id} - {receiver.host_id}: Iniciando o Protocolo de Envio.
Chave gerada: {key}''')

  key_size = len(key)
  sender.send_classical(receiver.host_id, f'{key_size}')
  sender_QKD(sender, receiver, execution, key)
  
  
def receiver_protocol(receiver, sender, execution):
  """"
  Protocolo QKD para o receptor.
  
  Args:
    receiver (Host): Host que deseja receber a chave com QKD
    sender (Host): Host que deseja enviar a chave com QKD
  """

  print(f"{sender.host_id} - {receiver.host_id}: Iniciando o Protocolo de Recebimento.")
  msg_key_size = receiver.get_next_classical(sender.host_id).content
  while msg_key_size.isdigit() == False:
    msg_key_size = receiver.get_next_classical(sender.host_id).content
  key_size = int(msg_key_size)
  
  key = receiver_QKD(receiver, sender, execution, key_size)
  
  if len(key) == key_size:
    print(f'''{sender.host_id} - {receiver.host_id}: Último bit recebido.
Chave recebida: {key}''')


def main():
  # Inicializando a rede e estabelecendo as conexões.
  network = Network.get_instance()
  network.delay = 0
  nodes = ['Node1', 'Node2', 'Node3']
  network.start(nodes)

  host_n1 = Host('Node1')
  host_n2 = Host('Node2')
  host_n3 = Host('Node3')
  
  hosts = [host_n1, host_n2, host_n3]
  
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

  host_n1.run_protocol(sender_protocol, (host_n3, 0))
  host_n3.run_protocol(receiver_protocol,  (host_n1, 0))

  sleep(50)

  # Para a rede no final do exemplo
  network.stop(True)
  exit()

if __name__ == '__main__':
    main()