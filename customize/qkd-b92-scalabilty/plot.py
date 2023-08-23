def organize(qkd_keys):
    """
    Organiza o dicionário com as chaves qkd pelo índice de forma crescente.

    Args:
        qkd_keys (dict): Dicionário com índice da execução e a sua respectiva chave.
    """
    sorted_keys = {k: qkd_keys[k] for k in sorted(qkd_keys)}
    qkd_keys.clear()
    qkd_keys.update(sorted_keys)
    
