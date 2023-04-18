from qunetsim.components import Host, Network
from qunetsim.objects import Qubit, Logger

Logger.DISABLED = True

def main():
    # Inicializando a rede e estabelecendo as conexões
    network = Network.get_instance()
    nodes = ["Arthur", "Bob", "Caio", "Diego"]
    network.start(nodes)
    network.delay = 0.2

    host_Arthur = Host('Arthur')
    host_Arthur.add_connection('Bob')
    host_Arthur.start()

    host_Bob = Host('Bob')
    host_Bob.add_connection('Arthur')
    host_Bob.add_connection('Caio')
    host_Bob.start()

    host_Caio = Host('Caio')
    host_Caio.add_connection('Bob')
    host_Caio.add_connection('Diego')
    host_Caio.start()

    host_Diego = Host('Diego')
    host_Diego.add_connection('Caio')
    host_Diego.start()

    network.add_host(host_Arthur)
    network.add_host(host_Bob)
    network.add_host(host_Caio)
    network.add_host(host_Diego)
    
    for qubits in range(10):
        # Cria um qubit de propriedade do Arthur. O qubit por padrão se inicia em |0⟩
        qubit = Qubit(host_Arthur)
        
        # Põe o qubit em estado de superposição com a Porta de Hadamard
        qubit.H()
        
        # Envia o qubit e espera o ACK do Diego
        qubit_ID, ack_arrived = host_Arthur.send_qubit('Diego', qubit, await_ack=True)
        print(f"{qubits + 1}º qubit enviado de Arthur para Diego. \nEsperando ACK...")

        # O send_qubit() retorna uma tupla: (ID tipo str, ACK tipo bool)
        if ack_arrived:
            print("ACK retornou! Eba")
        else: 
            print("ACK não retornou...")
            continue

        # Diego obtém o qubit enviado pelo Arthur
        qubit_recived = host_Diego.get_data_qubit('Arthur', qubit_ID)

        # Confirma o recebimento do qubit, mede-o e mostra o resultado
        if qubit_recived is not None:
            measurement = qubit_recived.measure()
            print(f"A medição do {qubits + 1}º qubit com o ID: {qubit_ID} resultou em {str(measurement)}\n")
        else:
            print('O qubibt é igual a None')

    # Para a rede no final do exemplo
    network.stop(True)

if __name__ == '__main__':
    main()