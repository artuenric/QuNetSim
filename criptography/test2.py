
from PIL import Image
import io
from algorithm import *

filename = get_local_path()

with open(filename+'\opa.txt', 'rb') as file:
    file_data = file.read()
    
# Obter a coleção de bytes
bytes_imagem = file_data

# Criar um objeto de memória com a coleção de bytes
buffer = io.BytesIO(bytes_imagem)

# Abrir a imagem a partir do objeto de memória
imagem = Image.open(buffer)

with open('img.jpeg', 'wb') as img:
    img.write(bytes_imagem)