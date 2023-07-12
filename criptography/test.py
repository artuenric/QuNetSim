from PIL import Image
from algorithm import *
import io

local = get_local_path()

# Carregar a imagem
imagem = Image.open(f'{local}/ratu.jpeg')

# Criar um objeto de memória
buffer = io.BytesIO()

# Salvar a imagem no objeto de memória
imagem.save(buffer, format='JPEG')

# Obter a coleção de bytes
bytes_imagem = buffer.getvalue()

with open('opa.txt', 'wb') as opa:
    opa.write(bytes_imagem)