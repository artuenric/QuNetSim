# | W⟩ = 1/√3 (|001⟩ + |010⟩ + |100⟩)
# Se um dos qubits se perder, os outros dois continuam emaranhados

from qunetsim.backends import EQSNBackend
from qunetsim.components import Host
from qunetsim.components import Network
from qunetsim.objects import Logger


Logger.DISABLED = False

def main():
    # Inicializando a rede e estabelecendo as conexões
    network = Network.get_instance()
    nodes = ["Alice", "Bob", "Eve", "Dean"]
    network.start(nodes)
    network.delay = 0.1

    host_alice = Host('Alice')
    host_alice.add_connection('Bob')
    host_alice.add_connection('Eve')
    host_alice.start()

    host_bob = Host('Bob')
    host_bob.add_connection('Alice')
    host_bob.add_connection('Eve')
    host_bob.start()

    host_eve = Host('Eve')
    host_eve.add_connection('Bob')
    host_eve.add_connection('Dean')
    host_eve.add_connection('Alice')
    host_eve.start()

    host_dean = Host('Dean')
    host_dean.add_connection('Eve')
    host_dean.start()

    network.add_host(host_alice)
    network.add_host(host_bob)
    network.add_host(host_eve)
    network.add_host(host_dean)

    share_list = ["Bob", "Eve", "Dean"]
    qubit_sent_ID, ack_received = host_alice.send_w(share_list, await_ack=True)

    print(f"Alice recebeu ACK de todos? {str(ack_received)}")

    q1 = host_alice.get_w('Alice', qubit_sent_ID, wait=10)
    q2 = host_bob.get_w('Alice', qubit_sent_ID, wait=10)
    q3 = host_eve.get_w('Alice', qubit_sent_ID, wait=10)
    q4 = host_dean.get_w('Alice', qubit_sent_ID, wait=10)

    m1 = q1.measure()
    m2 = q2.measure()
    m3 = q3.measure()
    m4 = q4.measure()

    print(f"Os resultados das medições são {m1}, {m2}, {m3}, {m4}")

    # Para a rede no final do exemplo
    network.stop(True)
    exit()


if __name__ == '__main__':
    main()
