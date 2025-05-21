import sys

def parse_csv(text):
    """Converte CSV separado por ';' em lista de listas, tratando aspas."""
    rows = []
    field, row = [], []
    in_quotes, i = False, 0

    while i < len(text):
        c = text[i]
        if in_quotes:
            if c == '"':
                if i + 1 < len(text) and text[i + 1] == '"':
                    field.append('"')
                    i += 1
                else:
                    in_quotes = False
            else:
                field.append(c)
        else:
            if c == '"':
                in_quotes = True
            elif c == ';':
                row.append(''.join(field))
                field = []
            elif c in '\r\n':
                if c == '\r' and i + 1 < len(text) and text[i + 1] == '\n':
                    i += 1
                row.append(''.join(field))
                rows.append(row)
                field, row = [], []
            else:
                field.append(c)
        i += 1

    if field or row:
        row.append(''.join(field))
        rows.append(row)

    return rows

def main():
    if len(sys.argv) < 2:
        print("Uso: python script.py <ficheiro.csv>")
        return

    ficheiro_csv = sys.argv[1]

    try:
        with open(ficheiro_csv, encoding="utf-8") as f:
            csv_text = f.read()
    except FileNotFoundError:
        print(f"Erro: ficheiro '{ficheiro_csv}' não encontrado.")
        return

    rows = parse_csv(csv_text)
    if not rows:
        return

    header, data_rows = rows[0], rows[1:]
    compositores = set()
    periodo_obras = {}

    for row in data_rows:
        if len(row) < 7:
            continue
        obra, periodo, compositor = row[0].strip(), row[3].strip(), row[4].strip()
        if compositor:
            compositores.add(compositor)
        if periodo:
            periodo_obras.setdefault(periodo, []).append(obra)

    compositores_ordenados = sorted(compositores)
    obras_por_periodo_ordenadas = {p: sorted(obras) for p, obras in periodo_obras.items()}
    distribuicao = {p: len(obras) for p, obras in periodo_obras.items()}

    print("--Resultados--")
    print("Lista Ordenada de Compositores:", compositores_ordenados)
    print("Dicionario Periodo -> Lista Ordenada de Titulos:", obras_por_periodo_ordenadas)
    print("Distribuicao de Obras por Periodo:", distribuicao)
    print("--------------")

if __name__ == "__main__":
    main()
