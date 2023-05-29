# Importando as dependências
from qunetsim.components import Host, Network
from qunetsim.objects import Qubit, Logger
from random import randint

# Protocolos de envio e recebimento QKD:
def sender_QKD(sender, receiver, key):
  """
    Protocolo QKD 92 para o remetente.

    Args:
        sender (Host): Objeto host que deseja enviar a chave.
        receiver (Host): Objeto host que deseja receber a chave e mensagem.
        key (list): Lista de 0s e 1s que representa a chave quântica.
    """
  print("Iniciando o Protocolo de Envio")

  sent_qubit_counter = 0

  for bit in key:
    # Controle do laço.
    success = False

    while success == False:
      qubit = Qubit(sender)
      # Se quisermos enviar 0, enviaremos |0>
      # Se quisermos enviar 1, enviaremos |+>
      if bit == 1:
        qubit.H()

      # Enviando o qubit para o receptor.
      sender.send_qubit(receiver.host_id, qubit, await_ack=True)

      # Aguardando a mensagem sobre a escolha da base.
      message = sender.get_next_classical(receiver.host_id, wait=20)

      if message is not None:
        if message.content == 'Sucesso!':
          success = True
          sent_qubit_counter += 1

  print(
    f'{sender.host_id} enviou o {sent_qubit_counter}º, e último, bit para {receiver.host_id}.'
  )


def receiver_QKD(receiver, sender, key_size):
  """
    Protocolo QKD B92 para o receptor.

    Args:
        sender (Host): Objeto host que deseja enviar a chave.
        receiver (Host): Objeto host que deseja receber a chave e mensagem.
        key (list): Lista de 0s e 1s que representa a chave quântica.
    """
  print("Iniciando o Protocolo de Recebimento")

  # Chave adquirida/gerada pelo recptor.
  key_receiver = []
  # Contador de bits medidos corretamente pelo receptor. Controle do laço.
  received_counter = 0
  while received_counter < key_size:
    base = randint(0, 1)
    # 0 significa base retilínea e 1 significa base diagonal
    qubit = receiver.get_qubit(sender.host_id, wait=20)

    if qubit is not None:
      if base == 1:
        qubit.H()

      measure = qubit.measure()
      if measure == 1:
        if base == 1:
          resulting_key_bit = 0
        elif base == 0:
          resulting_key_bit = 1
        print(f'{receiver.host_id} recebeu o {received_counter+1}º bit.')
        message_to_send = 'Sucesso!'
        key_receiver.append(resulting_key_bit)
        received_counter += 1
      else:
        message_to_send = 'fail'

      receiver.send_classical(sender.host_id, message_to_send, await_ack=True)
    else:
      receiver.send_classical(sender.host_id, "None", await_ack=True)
  return key_receiver


# Função que se utiliza para interceptar a comunicação:
def sniffing_QKD(sender, receiver, qubit):
  """
    Função utilizada pelo interceptador. Deve ser atribuída à "q_sniffing_fn" do host que irá interceptar.
    Nota: Não se passa nenhum argumento a essa função pois somente se atribui a "q_sniffing_fn", mas pode manipulá-los dentro da função.
    
    Args: 
        sender (Host): Remetente na rede que se deseja xeretar a comunicação.
        receiver (Host): Receptor na rede que se deseja xeretar a comunicação.
        qubit (Qubit): Qubit que se deseja xeretar.
    """
  snff = randint(0, 1)
  if snff == 1:
    base = randint(0, 1)
    if base == 1:
      qubit.H()
    # O qubit não deve ser destruído após a medição.
    qubit.measure(non_destructive=True)

def sender_protocol(sender, receiver):
  key = [0,1,0,1,1,0]
  key_size = len(key)
  sender.send_classical(receiver.host_id, str(key_size))
  sender_QKD(sender, receiver, key)
  
def receiver_protocol(receiver, sender):
  key_size = int(receiver.get_next_classical(sender.host_id).content)
  key = receiver_QKD(receiver, sender, key_size)
  if len(key) == key_size:
    print(key)
      
def running_concurrently(executions, hosts):
  senders =[]
  receivers = []
  
  # Escolhendo os remetentes e receptores do protocolo
  for choice in range(executions):
    sender = hosts[randint(0, len(hosts)-1)]
    receiver = hosts[randint(0, len(hosts)-1)]

    while sender.host_id == receiver.host_id:
      receiver = hosts[randint(0, len(hosts)-1)]
    
    # Adicionando os nós escolhidos nas suas respectvas listas
    senders.append(sender)
    receivers.append(receiver)

  # Rodando os protocolos com os remetentes e receptores escolhidos
  for send, recv in zip(senders, receivers):
    send.run_protocol(sender_protocol, (recv,))
    recv.run_protocol(receiver_protocol, (send,), blocking=True)