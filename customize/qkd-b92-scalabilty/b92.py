# Importando as dependências
from qunetsim.components import Host, Network
from qunetsim.objects import Qubit, Logger
from random import randint
from time import sleep
import re

# Funções de envio e recebimento da chave pelo QKD:
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

      # Enviados os dados do qubit
      sender.send_classical(receiver.host_id, f'{qubit.id}[{execution}]')
      
      # Enviando o qubit para o receptor.
      sender.send_qubit(receiver.host_id, qubit, await_ack=True)
      
      # Aguardando a mensagem sobre a escolha da base.
      message = sender.get_next_classical(receiver.host_id, wait=5)

      if message is not None:
        if message.content == 'sucess':
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
  # Os qubits que devem ser considerados
  correct_qubit_ID = ''
  
  while received_counter < key_size:
    base = randint(0, 1)
    
    # Recebendo as informações do qubits que devem ser considerados
    data = receiver.get_next_classical(sender.host_id, wait=5)
    regex = fr'.*\[{execution}\]$'
    if data != None:
      if re.fullmatch(regex, data.content):
        correct_qubit_ID = data.content[:36]
    else: continue
    
    # 0 significa base retilínea e 1 significa base diagonal
    qubit = receiver.get_qubit(sender.host_id, wait=5)

    # Se o qubit tratado não é o correto, pule
    if not qubit.id == correct_qubit_ID:
      continue
    
    if qubit is not None:
      if base == 1:
        qubit.H()

      measure = qubit.measure()
      if measure == 1:
        if base == 1:
          resulting_key_bit = 0
        elif base == 0:
          resulting_key_bit = 1
        message_to_send = 'sucess'
        key_receiver.append(resulting_key_bit)
        received_counter += 1
      else:
        message_to_send = 'fail'

      receiver.send_classical(sender.host_id, message_to_send, await_ack=True)
    else:
      receiver.send_classical(sender.host_id, "None", await_ack=True)
    print(f'{execution} - {key_receiver}')
  return key_receiver


# Função utilizada para interceptar a comunicação:
def sniffing_QKD(sender, receiver, qubit):
  """
    Função utilizada pelo interceptador. Deve ser atribuída à "q_sniffing_fn" do host que irá interceptar.
    Nota: Não se passa nenhum argumento a essa função pois somente se atribui a "q_sniffing_fn", mas pode manipulá-los dentro da função.
    
    Args: 
        sender (Host): Remetente na rede que se deseja xeretar a comunicação.
        receiver (Host): Receptor na rede que se deseja xeretar a comunicação.
        qubit (Qubit): Qubit que se deseja xeretar.
  """
  base = randint(0, 1)
  if base == 1:
    qubit.H()
  # O qubit não deve ser destruído após a medição.
  qubit.measure(non_destructive=True)

    
# Função para escolher os pares participante do QKD e seus respectivos sniffers      
def choice(hosts, executions=10):
  """
  Escolhe aleatoriamente quais serão os receptores e os remetentes QKD, além dos seus respectivos sniffers, caso seja possível.
  O Snffer só existirá se houver intermediários na comunicação entre o remetente o receptor.

  Args:
    hosts (lista): Lista com os objetos hosts da rede utilizada
    executions (int): Número de execuções simultâneas do protocolo

  Returns:
    senders (list): Lista com os remetentes das chaves pelo QKD
    receivers (list): Lista com os receptores das chaves pelo QKD
    sniffers (dict): As chaves são as comunicações e os valores são o sniffer para aquela comunicação
  """

  # Definindo o número de execuções
  while not executions.isdigit():
    executions = input("Quantas execuções simultâneas a rede deve ter? ")
  executions = int(executions)
              
  # Lista com os remetentes, receptores, e seus sniffers
  senders = []
  receivers = []
  sniffers = {}
  
  # Escolhendo os remetentes e receptores do protocolo
  for choice in range(executions):
    sender = hosts[randint(0, len(hosts)-1)]
    receiver = hosts[randint(0, len(hosts)-1)]
    
    # Guardar informações dos hosts escolhidos
    sender_num = int(sender.host_id[4:])
    receiver_num = int(receiver.host_id[4:])
    
    # Receiver e Sender não devem ser o mesmo Host (não há como realizar o protocolo) ou Hosts adjacentes (não é possível um sniffer)
    while (sender_num == receiver_num) or (sender_num == receiver_num + 1) or (sender_num == receiver_num - 1):
      receiver = hosts[randint(0, len(hosts)-1)]
      receiver_num = int(receiver.host_id[4:])

    # Adicionando os nós escolhidos nas suas respectvas listas
    senders.append(sender)
    receivers.append(receiver)
  
  # Escolhendo os sniffers.
  for send, recv in zip(senders, receivers):
    # Obtém o número do host ID. Por exemplo, o 1 do Node1.
    sender_n = int(send.host_id[4:])
    receiver_n = int(recv.host_id[4:])
    
    # Se a comunicação seja da esquerda para direita. Por exemplo, sender é o Node1 e receiver é o Node4
    if sender_n < receiver_n:  
      sniffers[f'{sender_n}-{receiver_n}'] = randint(sender_n + 1, receiver_n - 1)

    # Se a comunicação é da direita para a esquerda:
    else:
      if sender_n - 1 != receiver_n:
        sniffers[f'{sender_n}-{receiver_n}'] = randint(receiver_n + 1, sender_n - 1)

  return senders, receivers, sniffers


# Protocolos modularizado com as funções criadas anteriormente
def sender_protocol(sender, receiver, execution, generated_keys):
  """"
  Protocolo QKD para o remetente.
  
  Args:
    sender (Host): Host que deseja enviar a chave com QKD
    receiver (Host): Host que deseja receber a chave com QKD
    generated_keys (lista): Lista de todas as chaves geradas
  """

  # Gera a chave com tamanho igual a 256
  key = []
  for bit in range(10):
    key.append(randint(0, 1))
  
  print(f'[{execution}] Chave gerada:{key}')
  generated_keys[f'{execution}'] = key
  
  key_size = len(key)
  sender.send_classical(receiver.host_id, str(key_size))
  sender_QKD(sender, receiver, execution, key)
  
  
def receiver_protocol(receiver, sender, execution, received_keys):
  """"
  Protocolo QKD para o receptor.
  
  Args:
    receiver (Host): Host que deseja receber a chave com QKD
    sender (Host): Host que deseja enviar a chave com QKD
    received_keys (lista): Lista de todas as chaves recebidas
  """

  msg = receiver.get_next_classical(sender.host_id).content
  while msg.isdigit() == False:
    msg = receiver.get_next_classical(sender.host_id).content
  key_size = int(msg)
  key = receiver_QKD(receiver, sender, execution, key_size)
  
  if len(key) == key_size:
    print(f'[{execution}] Chave recebida:{key}')
    received_keys[f'{execution}'] = key


# Função para execução de várias comunicações simultâneas dos protocolos
def running_concurrently(senders, receivers):
  """
  Realiza N execuções dos protocolos simultâneamente. O número de execuções depende do tamanho das listas que recebe como argumento.

  Args:
    senders (lista): Lista com os Hosts que serão os remetentes do protocolo QKD.
    receivers (lista): Lista com os Hosts que serão os receptores do protocolo QKD.
    time (float): Tempo estimado para a execução de todos os protocolos.
  """
  
  execution = 0
  executions_info = []
  received_keys = dict()
  generated_keys = dict()
  
  # Rodando os protocolos com os remetentes e receptores escolhidos
  for send, recv in zip(senders, receivers):
    executions_info.append(f'[{execution}]:{send.host_id}-{recv.host_id}')
    send.run_protocol(sender_protocol, (recv, execution, generated_keys))
    recv.run_protocol(receiver_protocol, (send, execution, received_keys) )
    execution += 1
  
  return executions_info, generated_keys, received_keys