from qunetsim.components import Host
from qunetsim.components import Network
from qunetsim.objects import Logger

Logger.DISABLED = True

def protocol_1(host, receiver):
    """
    Protocolo emissor para envio de 5 pares EPR.

    Args:
        host (Host): O host emissor dos pares EPR.
        receiver (str): O ID do receptor dos pares EPR.
    """
    # Código do protocolo para o host.
    for i in range(5):
        print(f'Enviando o {i+1}º par EPR')
        epr_id, ack_arrived = host.send_epr(receiver, await_ack=True)

        # Se o receptor recebeu o EPR, o ACK voltou. É seguro usar o par EPR.
        if ack_arrived:
            qubit = host.get_epr(receiver, q_id=epr_id)
            measurement = str(qubit.measure())
            print(f'Host 1 medido: {measurement}')
        else:
            print('ACK não voltou. O par EPR não foi devidamente estabelecido.')
    print('Fim do Protocolo Emissor.\n')


def protocol_2(host, sender):
    """
    Protocolo emissor para receber 5 pares EPR.

    Args:
        host (Host): O Host receptor dos pares EPR.
        sender (str): O ID do emissor dos pares EPR.
    """

    # Host 2 aguarda 5 segundos até receber o par EPR.
    for _ in range(5):
        qubit = host.get_epr(sender, wait=5)
        # qubit é igual a None se o tempo expirar
        if qubit is not None:
            measurement = str(qubit.measure())
            print(f'Host 2 medido: {measurement}')
        else:
            print('Host 2 não recebeu um par EPR')
    print('Fim do Protocolo Receptor')


def main():
    # Inicializando a rede e estabelecendo as conexões
    network = Network.get_instance()
    nodes = ['A', 'B', 'C']
    network.start(nodes)
    network.delay = 0.1

    host_A = Host('A')
    host_A.add_connection('B')
    host_A.delay = 0
    host_A.start()

    host_B = Host('B')
    host_B.add_connection('A')
    host_B.add_connection('C')
    host_B.delay = 0
    host_B.start()

    host_C = Host('C')
    host_C.add_connection('B')
    host_C.delay = 0
    host_C.start()

    network.add_host(host_A)
    network.add_host(host_B)
    network.add_host(host_C)

    # blocking=True: Aguarde até que o thread pare antes de prosseguir
    host_A.run_protocol(protocol_1, (host_C.host_id, ), blocking=True)
    host_C.run_protocol(protocol_2, (host_A.host_id, ), blocking=True)
    
    # Para a rede no final do exemplo
    network.stop(True)

if __name__ == '__main__':
    main()