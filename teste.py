import re
execution = 0
qubit_info = '1214fc39-bcbf-4430-9912-e2ea2cb4c2dc[0]'
regex = fr'.*\[{execution}\]$'
buffer = []
print(qubit_info)
# Se a mensagem recebida condiz com esta execução
if re.fullmatch(regex, qubit_info):
    # Add qubit ID no buffer
    buffer.append(qubit_info[:36])
print(buffer)