from random import randint
def encrypt(key, text):
    encrypted_text = ""
    for indice, char in enumerate(text):
        encrypted_text += chr(ord(key[indice]) ^ ord(char))
    return encrypted_text

def decrypt(key, encrypted_text):
    return encrypt(key, encrypted_text)

message = input("Digite a mensagem que deseja enviar: ")
key_size = len(message)
key = []

for bit in range(key_size):
    key.append(str(randint(0, 1)))
print(key)

texto_encript = encrypt(key, message)
print(texto_encript)
print(decrypt(key, texto_encript))
