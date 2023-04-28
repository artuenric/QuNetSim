import numpy as np
from random import randint

from qunetsim.components import Host
from qunetsim.components import Network
from qunetsim.objects import Qubit
from qunetsim.objects import Logger

Logger.DISABLED = False

def alice_qkd():
    sequence_nr = 0
    # iterate over all bits in the secret key.

    for bit in secret_key:
        ack = False
    
        while ack == False:
            print(f"Alice sent {sequence_nr + 1} key bits")
            # Obtendo uma base aleatória. 0 para base Z and 1 para base X.
            base = random.randint(0, 1)

            # Criando qubit
            qubit = Qubit(alice)

            # Define o qubit para o bit da chave secreta.
            if bit == 1:
                qubit.X()

            # Aplica a alteração de base ao bit, se necessário.
            if base == 1:
                qubit.H()

            # Envia Qubit para Bob
            alice.send_qubit(receiver, qubit, await_ack=True)

            # Get measured basis of Bob
            message = alice.get_classical(host_eve, msg_buff, sequence_nr)

            # Compare to send basis, if same, answer with 0 and set ack True and go to next bit,
            # otherwise, send 1 and repeat.
            print(sequence_nr)
            print(base)

            a = (f'{sequence_nr}:{base}')
            print(message)
            if message == (f'{sequence_nr}: {base}'):
                ack = True
                alice.send_classical(receiver, ("%d:0" % sequence_nr), await_ack=True)
            else:
                ack = False
                alice.send_classical(receiver, ("%d:1" % sequence_nr), await_ack=True)

            sequence_nr += 1



# Inicializando a rede e estabelecendo as conexões
network = Network.get_instance()
nodes = ['Alice', 'Eve', 'Bob']
network.start(nodes)
network.delay = 0

host_Alice = Host('Alice')
host_Alice.add_connection('Bob')
host_Alice.delay = 0
host_Alice.start()

host_Bob = Host('Bob')
host_Bob.add_connection('Alice')
host_Bob.add_connection('Eve')
host_Bob.delay = 0
host_Bob.start()

host_Eve = Host('Eve')
host_Eve.add_connection('Bob')
host_Eve.delay = 0
host_Eve.start()

network.add_host(host_Alice)
network.add_host(host_Bob)
network.add_host(host_Eve)

# Para a rede no final do exemplo
network.stop(True)
