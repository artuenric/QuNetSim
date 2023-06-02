import os

def get_local_path():
    """
    Obtém o caminho absoluto do diretório do código
    
    returns: 
        current_dir (str): Caminho do código no computador.
    """

    current_dir = os.path.abspath(os.path.dirname(__file__))
    return current_dir


def read_log(txt):
    path = get_local_path()
    #with open(f'{path}/log.txt', 'w', encoding='utf-8') as snff:
        
