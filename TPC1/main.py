import sys

def extrair_numeros(token):
    """Extrai inteiros de uma string."""
    numeros = []
    num = ''
    for ch in token:
        if ch.isdigit():
            num += ch
        elif num:
            numeros.append(int(num))
            num = ''
    if num:
        numeros.append(int(num))
    return numeros

soma_ativa = True
total = 0

for linha in sys.stdin:
    tokens = linha.strip().split()
    output = []

    for token in tokens:
        lower_token = token.lower()

        if lower_token == "on":
            soma_ativa = True
            output.append(token)
            continue
        elif lower_token == "off":
            soma_ativa = False
            output.append(token)
            continue

        if "=" in token:
            partes = token.split("=")
            reconstruido = ""
            for i, parte in enumerate(partes):
                if soma_ativa:
                    total += sum(extrair_numeros(parte))
                reconstruido += parte
                if i < len(partes) - 1:
                    reconstruido += "="
                    output.append(reconstruido)
                    print(" ".join(output))
                    print(">>", total)
                    output = []
                    reconstruido = ""
            if reconstruido:
                if reconstruido.lower() == "on":
                    soma_ativa = True
                elif reconstruido.lower() == "off":
                    soma_ativa = False
                output.append(reconstruido)
        else:
            if soma_ativa:
                total += sum(extrair_numeros(token))
            output.append(token)

    if output:
        print(" ".join(output))

print(">>", total)
