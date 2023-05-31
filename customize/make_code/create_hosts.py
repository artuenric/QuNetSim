def create_nodes(n):
    """
    Cria uma lista com os hosts_id dos n nós da rede.
    Começa pelo Node1 até o Node(n).

    Args:
        n (int): Número de nós desejados.

    Returns:
        list: Lista com os nomes/host_ids dos nós da rede.
    """
    nodes_list = []
    for node in range(n):
        nodes_list.append(f'Node{node+1}')
    return nodes_list

def linear_connections(hosts):
    """
    Adiciona conexões entre os nós da rede de maneira linear. Do primeiro até o último da lista.

    Args:
        hosts (list): Lista com os hosts da rede.
    """
    for i, node in enumerate(hosts):
        print(i)
        print(node.host_id)
        if i == 0:
            node.add_connection(hosts[1].host_id)
        elif i < len(hosts)-1:
            node.add_connection(hosts[i-1].host_id)
            node.add_connection(hosts[i+1].host_id)
        else:
            node.add_connection(hosts[i-1].host_id)
