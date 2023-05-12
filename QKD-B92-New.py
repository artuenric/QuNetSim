# Importando as dependências
from qunetsim.components import Host, Network
from qunetsim.objects import Qubit, Logger
from random import randint

Logger.DISABLED = True

def sniffing_QKD(sender, receiver, qubit):
    """
    Função utilizada pelo interceptador. Deve ser atribuída à "q_sniffing_fn" do host que irá interceptar.
    """
    if sender == 'Alice':
        r = randint(0, 1)
        if r > 1:
            base = randint(0, 1)
            if base == 1:
                qubit.H()
            # O qubit não deve ser destruído após a medição.
            qubit.measure(non_destructive=True)

def sender_QKD(sender, receiver, key):
    """
    Protocolo QKD 92 para o remetente.
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
                    print(f'{sender.host_id} enviou o {sent_qubit_counter+1}º para {receiver.host_id}.')

def receiver_qkd(receiver, sender, key_size):
    """
    Protocolo QKD B92 para o receptor.
    """

    # Chave adquirida/gerada pelo recptor.
    key_receiver = []
    # Contador de bits medidos corretamente pelo receptor. Controle do laço.
    received_counter = 0
    print('1')
    while received_counter < key_size:
        print(received_counter)
        base = randint(0, 1)
        # 0 significa base retilínea e 1 significa base diagonal
        qubit = receiver.get_data_qubit(sender.host_id, wait=20)
        
        if qubit is not None:
            if base == 1:
                qubit.H()

            measure = qubit.measure()
            if measure == 1:
                if base == 1:
                    resulting_key_bit = 0
                elif base == 0:
                    resulting_key_bit = 1
                print(f'Bob recebeu o {received_counter+1}º bit.')
                message_to_send = 'Sucesso!'
                key_receiver.append(resulting_key_bit)
                received_counter += 1
            else:
                message_to_send = 'fail'
            receiver.send_classical(sender.host_id, message_to_send, await_ack=True)
        else: receiver.send_classical(sender.host_id, "None pra crlh", await_ack=True)
    print(key_receiver)

def main():
    # Inicializando a rede e estabelecendo as conexões.
    network = Network.get_instance()
    nodes = ['Alice', 'Eve', 'Bob']
    network.start(nodes)
    network.delay = 0.1

    host_Alice = Host('Alice')
    host_Alice.add_connection('Bob')
    host_Alice.delay = 0.1
    host_Alice.start()

    host_Eve = Host('Eve')
    host_Eve.add_connection('Alice')
    host_Eve.add_connection('Bob')
    host_Eve.delay = 0.1
    host_Eve.start()

    host_Bob = Host('Bob')
    host_Bob.add_connection('Eve')
    host_Bob.delay = 0.1
    host_Bob.start()

    network.add_host(host_Alice)
    network.add_host(host_Eve)
    network.add_host(host_Bob)

    interception = True
    if interception == True:
            # Se há ou não sniff
            host_Eve.q_relay_sniffing = True
            # A função a ser aplicada aos qubits em trânsito.
            host_Eve.q_relay_sniffing_fn = sniffing_QKD
    
    key = [0, 1, 0, 1, 1, 0, 1]
    key_size = len(key)
    print(key_size)

    def protocolo_sender(sender):
        sender_QKD(sender, host_Bob, key)

    def protocolo_receiver(receiver):
        receiver_qkd(receiver, host_Alice, key_size)

    host_Alice.run_protocol(protocolo_sender,())
    host_Bob.run_protocol(protocolo_receiver, (), blocking=True)

    # Para a rede no final do exemplo
    network.stop(True)
    exit()

if __name__ == '__main__':
    main()