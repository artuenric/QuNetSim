def comparacao(gerada, recebida):
    """
    Compara as duas listas (chaves geradas e recebidas) e retorna a quantidade de acertos do sniffer.

    Args:
        gerada (lista): Lista com a chave gerada.
        recebida (lista): Lista com a chave recebida.
    """
    
    sniffer_acertou = 0
    for bit_gerado, bit_recebido in zip(gerada, recebida):
        if bit_recebido != bit_gerado:
            sniff_acertou += 1    
    return sniffer_acertou








def achar_gerada(txt, indice):
    with open(txt, 'r') as f:
        conteudo = f.readlines()
    chave = str(chave)
    for linha in conteudo:
        if f"{indice} Chave gerada:" in linha:
            chave = linha.split(':')[1]
        
    
"""def check(txt, execs):
    contador = 1
        
    while contador <= execs:
        for linha in conteudo:
            if contador in linha:"""
                

conteudo =  ["[3] Chave gerada:[1, 0, 1, 1, 1, 0, 0, 0, 0, 1]"]
indice = 3
for linha in conteudo:
    if f"[{indice}] Chave gerada:" in linha:
        chave = linha.split(':')
        print(chave[1])