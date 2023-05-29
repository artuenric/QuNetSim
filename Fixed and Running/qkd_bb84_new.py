"""
Alice deseja mandar uma mensagem para Bob sem que Eve possa se intrometrometer.
A rede tem essa aparência: Alice <---> Eve <--> Bob. 
O objetivo é compartilhar uma chave por meio de um canal quântico. A chave é utilizada para criptografar e descriptografar a mensagem. 
Como Eve não tem acesso à chave, ele não pode decifrar a mensagem, que é compartilhada de forma clássica.

"""

# Importando as dependências
from qunetsim.components import Host, Network
from qunetsim.objects import Qubit, Logger
from random import randint

# Criptografia
# Nota: O algoritmo aqui utilizado para criptografia é extremamente simples, pode, e deve, ser trocado.
def encrypt(key, text):
    encrypted_text = ""
    for indice, char in enumerate(text):
        bit = str(key[indice])
        encrypted_text += chr(ord(bit) ^ ord(char))
    return encrypted_text

def decrypt(key, encrypted_text):
    return encrypt(key, encrypted_text)

# Mensagem a ser enviada:
msg = input("Digite a mensagem que deseja enviar: ")

# Criação da chave aleatória
key_size = len(msg)
key = []
for bit in range(key_size):
    key.append(randint(0, 1))
print(f"Chave gerada: {key}")

# Protocolos:
# Criação de um protocolo sender_QKD e outra receiver_QKD.
def sender_QKD(sender, receiver, key, msg):
    """
    Protocolo QKD BB84 para o remetente.

    Args:
        sender (Host): Objeto host que deseja enviar a chave.
        receiver (Host): Objeto host que deseja receber a chave e mensagem.
        key (list): Lista de 0s e 1s que representa a chave quântica.
        msg (str): Mensagem que será enviada.
    """
    
    # Guarda e especifica qual qubit trabalharemos.
    seq_num = 0
    for bit in key:
        ack = False
        while ack == False:
            qubit = Qubit(sender)
            # Critérios para definir a medição dos qubits:
            base = randint(0, 1)
            print("Remetente - Base escolhida:", base)
            if bit == 1: # Depende da key.
                qubit.X()
            if base == 1: # Depende da base.
                qubit.H()
            
            # Envio do qubit transformado de acordo com as alterações aleatórias.
            print(f"Remetente - Eniviando o Qubit {seq_num}")
            sender.send_qubit(receiver.host_id, qubit, await_ack=True)
            
            # Agora recebemos de Bob a base utilizada em sua medição (por meio de uma mensagem clássica).
            # Nota: "receiver" e "sender" do QKD, não dessa mensagem clássica.
            message = sender.get_classical(receiver.host_id, seq_num, wait=10)    
            print(f"Remetente - Recebeu a mensagem: {message.content}")

            # Este padrão de sintaxe define se podemos ou não partir para o próximo qubit.
            # Nº qubit : base utilizada.
            if message.content == (f'{seq_num}:{base}'):
                # Mesma base, confirma para ir para o próximo qubit.
                ack = True
                # Envia uma mensagem clássica com "Nº qubit : 0", 0 confirma para o receptor que a base estava correta.
                sender.send_classical(receiver.host_id, (f"{seq_num}:0"), await_ack=True)

            else:
                ack = False
                # 1 significa que a base está errada.
                sender.send_classical(receiver.host_id, (f"{seq_num}:1"), await_ack=True)

            # Próximo qubit.    
            seq_num += 1

    # Criptografando a mensagem.
    encrypt_msg = encrypt(key, msg)
    # Envio da mensagem criptografada.
    print(f"Remetente - Enviando mensagem criptografada: {encrypt_msg}")
    sender.send_classical(receiver.host_id, encrypt_msg, await_ack=True)
    

def receiver_QKD(receiver, sender, key_size):
    """
    Protocolo QKD BB84 para o receptor.

    Args:
        receiver (Host): Objeto host que deseja receber a chave e mensagem.
        sender (Host): Objeto host que deseja enviar a chave.
        key_size (int): Tamanho da chave. Utilizado para controle do laço.

    """
    
    # A key "gerada" pelo reptor.
    key_receiver = []
    # Controle do laço.
    received_counter = 0
    # Nº qubit.
    seq_num = 0

    while received_counter < key_size:
        # Receber o qubit enviado pelo remetente.
        qubit = receiver.get_qubit(sender.host_id, wait=5)
        while qubit == None:
            print("Receptor - O Qubit recebido vale None.")
            qubit = receiver.get_qubit(sender.host_id, wait=10)
        print("Receptor - Qubit recebido!")
        # Mesma lógica simples para escolha de base.
        base = randint(0, 1)
        if base == 1:
            qubit.H()
        measure = qubit.measure()
        print(f"Receptor - Base escolhida: {base}.")
        print(f"Receptor - Enviando mensagem: {seq_num}:{base}")

        # Envio da base utilizada para o Sender.
        # Nota: "receiver" e "sender" do QKD, não dessa mensagem clássica.
        receiver.send_classical(sender.host_id, (f'{seq_num}:{base}'), await_ack=True)

        # Recebimento da mensagem clássica de confirmação, ou não, do uso da base correta.
        message = receiver.get_classical(sender.host_id, seq_num, wait=10)
        # get_classical retorna sender: host_id e content: conteúdo da mensagem.

        # Checando a mensagem:
        if message != None:
            if message.content == (f'{seq_num}:0'):
                # Adiciona 1 ao contador de recebimento de confirmação.
                received_counter += 1
                print(f"Macth!\n{receiver.host_id} recebeu o {received_counter}º bit da chave secreta!\n")
                key_receiver.append(measure)
            elif message.content == (f'{seq_num}:1'):
                print("Não houve match. Próximo qubit.\n")
        else: 
            print("Algo de errado aconteceu. Mensagem sobre a base não recebida...\n")

        # Próximo qubit
        seq_num += 1

    print(f"Receptor (Secreto) - A chave recebida foi: {key_receiver}")
    
    # Recebendo mensagem criptografada:
    msg = receiver.get_next_classical(sender.host_id)
    print(f"Receptor - A mensagem criptografada recebida é: {msg.content}")
    msg = decrypt(key_receiver, msg.content)
    print(f"Receptor (Secreto) - A mensagem foi: {msg}")
    

def main():

    # Inicializando a rede e estabelecendo as conexões.
    network = Network.get_instance()
    nodes = ['Alice', 'Eve', 'Bob']
    network.start(nodes)
    network.delay = 0.5

    host_Alice = Host('Alice')
    host_Alice.add_connection('Eve')
    host_Alice.delay = 0.5
    host_Alice.start()

    host_Eve = Host('Eve')
    host_Eve.add_connection('Alice')
    host_Eve.add_connection('Bob')
    host_Eve.delay = 0.5
    host_Eve.start()

    host_Bob = Host('Bob')
    host_Bob.add_connection('Eve')
    host_Bob.delay = 0.5
    host_Bob.start()

    network.add_host(host_Alice)
    network.add_host(host_Eve)
    network.add_host(host_Bob)

    # Executando os protocolos:
    host_Alice.run_protocol(sender_QKD, (host_Bob, key, msg))
    host_Bob.run_protocol(receiver_QKD, (host_Alice, key_size), blocking=True)

    # Para a rede no final do exemplo
    network.stop(True)

if __name__ == '__main__':
    main()
