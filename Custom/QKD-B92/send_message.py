
"""
Este código, especialmente nestas funções, representa o envio de uma mensagem (arquivo) de um lugar para outro. Essa simulação se dá na forma de troca de diretórios.
O arquivo é movido do diretório 'alice' para o diretório 'bob', ou seja, Alice está enviando o arquivo em questão para Bob. O intuito é de ilustrar a transferência.
"""
import os

def get_local_path():
    """
    Obtém o caminho absoluto do diretório do código
    
    returns: 
        current_dir (str): Caminho do código no computador.
    """

    current_dir = os.path.abspath(os.path.dirname(__file__))
    return current_dir

def move_file(source, destination):
    """
    Move o arquivo para outro diretório.
    Nota: Isso representa um envio de uma mensagem através de um canal clássico no contexto QKD.

    Args:
        source (str): Caminho de origem do arquivo.
        destination (str): Caminho de destino do arquivo.
    """
    # Verificar se o arquivo de origem existe
    if not os.path.isfile(source):
        print(f"O arquivo de origem '{source}' não existe.")
        return

    # Mover o arquivo para o diretório de destino
    try:
        os.rename(source, os.path.join(destination, os.path.basename(source)))
        print(f"Arquivo enviado com sucesso para '{destination}'.")
    except Exception as e:
        print("Ocorreu um erro ao enviar o arquivo:", str(e))
