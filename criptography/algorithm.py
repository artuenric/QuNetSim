# Importando biblioteca de criptografia
from cryptography.fernet import Fernet
import os

def get_local_path():
    """
    Obtém o caminho absoluto do diretório do código
    
    returns: 
        current_dir (str): Caminho do código no computador.
    """

    current_dir = os.path.abspath(os.path.dirname(__file__))
    return current_dir

def generate_key():
    """
    Gera a chave AES em modo CBC.

    returns:
        Chave AES
    """
    return Fernet.generate_key()
    

def encrypt_file(filename, key):
    """
    Criptografa um arquivo usando o algoritmo AES (Advanced Encryption Standard) em modo CBC (Cipher-Block Chaining).

    Args:
        filename (str): O nome do arquivo a ser criptografado.
        key (bytes): A chave de criptografia no formato Fernet (32 bytes).

    """
    # Ler o conteúdo do arquivo
    with open(filename, 'rb') as file:
        file_data = file.read()

    # Criar uma instância do objeto Fernet com a chave fornecida
    fernet = Fernet(key)

    # Criptografar os dados do arquivo
    encrypted_data = fernet.encrypt(file_data)

    # Escrever os dados criptografados em um novo arquivo
    encrypted_filename = filename + '.encrypted'
    with open(encrypted_filename, 'wb') as encrypted_file:
        encrypted_file.write(encrypted_data)

    print('Arquivo criptografado com sucesso:', encrypted_filename)


def decrypt_file(encrypted_filename, key):
    """
    Descriptografa um arquivo criptografado usando o algoritmo AES em modo CBC.

    Args:
        filename (str): O nome do arquivo criptografado.
        key (bytes): A chave de descriptografia no formato Fernet (32 bytes).

    """
    #try:
    # Ler o conteúdo do arquivo criptografado
    with open(encrypted_filename, 'rb') as file:
        encrypted_data = file.read()

    # Criar uma instância do objeto Fernet com a chave fornecida
    fernet = Fernet(key)

    # Descriptografar os dados do arquivo
    decrypted_data = fernet.decrypt(encrypted_data)

    # Remover a extensão ".encrypted" do nome do arquivo original
    filename = encrypted_filename.rsplit('.', 1)[0]

    # Escrever os dados descriptografados em um novo arquivo
    with open(filename, 'wb') as decrypted_file:
        decrypted_file.write(decrypted_data)
    print('Arquivo descriptografado com sucesso:', filename)

    #except Exception as e:
    #    print("Ocorreu um erro ao desincriptar o arquivo. Devemos tentar de novo.")
    
