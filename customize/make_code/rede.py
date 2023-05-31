from qunetsim.components import Host, Network
from qunetsim.objects import Logger, Qubit

Logger.DISABLED = False
from qunetsim.backends import EQSNBackend

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
    network = Network.get_instance()
    nodes = ['Node1', 'Node2', 'Node3', 'Node4', 'Node5', 'Node6', 'Node7', 'Node8', 'Node9', 'Node10', 'Node11', 'Node12']
    
    network.delay = 0
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
    
    network.add_hosts(hosts)

    host_n1.run_protocol(protocol_1,(host_n12.host_id,))
    host_n12.run_protocol((protocol_2), (host_n1.host_id,), blocking=True)

    network.draw_quantum_network()
    network.stop(True)
    exit()

if __name__ == '__main__':
  main()