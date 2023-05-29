import math
import random
from qunetsim.components import Host
from qunetsim.components import Network
from qunetsim.objects import Logger

# Disable QuNetSim logging
Logger.DISABLED = True

# Número de rodadas do jogo.
PLAYS = 20

# Estratégia quântica ou clássica para o jogo.
strategy = ""
while strategy.upper() not in ["Q", "C"]:
    strategy = input(f'Qual estratégia deseja seguir? ("Q" para quântica, "C" para clássica): ')
if strategy.upper() == "Q": strategy = 'QUANTUM'
elif strategy.upper() == "C": strategy = 'CLASSICAL'

# Criação dos protocolos:
def alice_classical(alice_host, referee_id):
    """
    Protocolo clássico de Alice para o jogo CHSH

    Args:
        alice_host (Host): Objeto Alice host.
        referee_id (str): ID do Host árbitro.
    """
    for i in range(PLAYS):
        _ = alice_host.get_next_classical(referee_id, wait=5)
        alice_host.send_classical(referee_id, "0")


def alice_quantum(alice_host, referee_id, bob_id):
    """
    Protocolo quântico de Alice para o jogo CHSH.

    Args:
        alice_host (Host): Objeto Alice Host.
        referee_id (str): ID do Host árbitro.
        bob_id (str): Host ID de Bob (para o acesso dos pares EPR)
    """
    
    # Recebe uma mensagem (bit) por rodada.
    for i in range(PLAYS):
        referee_message = alice_host.get_next_classical(referee_id, wait=5)
        # get_next_classical retorna Sender, Content, Sequence Number
        x = int(referee_message.content)
        epr = alice_host.get_epr(bob_id)

        if x == 0:
            result = epr.measure()
            alice_host.send_classical(referee_id, str(result))
        else:
            epr.H()
            result = epr.measure()
            alice_host.send_classical(referee_id, str(result))


def bob_classical(bob_host, referee_id):
    """
    Protocolo clássico de Bob para o jogo CHSH.

    Args:
        bob_host (Host): Objeto Bob Host.
        referee_id (str): ID do Host árbitro.
    """
    for i in range(PLAYS):
        _ = bob_host.get_next_classical(referee_id, wait=5)
        bob_host.send_classical(referee_id, "0")


def bob_quantum(bob_host, referee_id, alice_id):
    """
       Protocolo quântico de Bob para o jogo CHSH.

       Args:
           bob_host (Host): Objeto Bob Host
           referee_id (str): ID do Host árbitro
           alice_id (str): ID do Host Alice (somente para acesso do par EPR)
    """
    for i in range(PLAYS):
        referee_message = bob_host.get_next_classical(referee_id, wait=5)

        y = int(referee_message.content)
        epr = bob_host.get_epr(alice_id)

        if y == 0:
            # Executa uma rotação com a porta Pauli Y.
            epr.ry(-2.0 * math.pi / 8.0)
            res = epr.measure()
            bob_host.send_classical(referee_id, str(res))
        else:
            epr.ry(2.0 * math.pi / 8.0)
            res = epr.measure()
            bob_host.send_classical(referee_id, str(res))


def referee(ref, alice_id, bob_id):
    """
    Protocolo do árbitro para o jogo CHSH.

    Args:
        ref (Host): Objeto Host árbitro.
        alice_id (str): ID do Host Alice
        bob_id (str): ID do Host Bob.
    """

    wins = 0
    for i in range(PLAYS):
        x = random.choice([0, 1])
        ref.send_classical(alice_id, str(x))
        y = random.choice([0, 1])
        ref.send_classical(bob_id, str(y))

        alice_response = ref.get_classical(alice_id, seq_num=i, wait=5)
        bob_response = ref.get_classical(bob_id, seq_num=i, wait=5)

        a = int(alice_response.content)
        b = int(bob_response.content)

        print(f'{i+1}º Rodada:')
        print(f'''X | Y | A | B
--------------
{x} | {y} | {a} | {b}''', end='  ')
        if x & y == a ^ b:
            print('VITÓRIA!\n')
            wins += 1
        else:
            print('DERROTA!\n')

    print(f'Proporção de vitórias {100 * wins / PLAYS}')


def main():
    network = Network.get_instance()
    network.start()

    host_A = Host('A')
    host_A.add_c_connection('C')
    host_A.start()

    host_B = Host('B')
    host_B.add_c_connection('C')
    host_B.start()

    host_C = Host('C')
    host_C.add_c_connection('A')
    host_C.add_c_connection('B')
    host_C.start()

    network.add_host(host_C)

    # Para criação do entrelaçamento
    host_A.add_connection('B')
    host_B.add_connection('A')

    network.add_host(host_A)
    network.add_host(host_B)

    if strategy == 'QUANTUM':
        print('Criando o entrelaçamento inicial')
        for i in range(PLAYS):
            host_A.send_epr('B', await_ack=True)
        print('Criação do entrelaçamento inicial concluída!')

    # Remove the connection from Alice and Bob
    #host_A.remove_connection('B')
    #host_B.remove_connection('A')
    #network.update_host(host_A)
    #network.update_host(host_B)

    print(f'Iniciando o Jogo...\nEstratégia: {strategy}')

    # Jogando de forma clássica
    if strategy == 'CLASSICAL':
        host_A.run_protocol(alice_classical, (host_C.host_id,))
        host_B.run_protocol(bob_classical, (host_C.host_id,))

    # Jogando de forma quântica
    if strategy == 'QUANTUM':
        host_A.run_protocol(alice_quantum, (host_C.host_id, host_B.host_id))
        host_B.run_protocol(bob_quantum, (host_C.host_id, host_A.host_id))

    host_C.run_protocol(referee, (host_A.host_id, host_B.host_id), blocking=True)

    # Para a rede no final do exemplo
    network.stop(True)
    exit()

if __name__ == '__main__':
    main()
