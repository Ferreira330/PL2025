from maquina import Maquina

moedas = {"2e": 2.0, "1e": 1.0, "50c": 0.5, "20c": 0.2,
          "10c": 0.1, "5c": 0.05, "2c": 0.02, "1c": 0.01}

def main():
    m = Maquina()
    print("Bem-vindo à Máquina de Venda Automática")

    while True:
        cmd = input("Comando (LISTAR, MOEDA, SELECIONAR, SALDO, SAIR): ").strip().upper()
        if cmd == "LISTAR":
            m.listar_produtos()
        elif cmd.startswith("MOEDA"):
            # Exemplo: MOEDA 2e, 50c
            moeda_str = cmd[6:].strip()  # Pega a string depois de 'MOEDA '
            partes = [m.strip() for m in moeda_str.split(',')]

            for p in partes:
                p = p.strip()
                if p in moedas:
                    m.inserir_saldo(moedas[p])
                else:
                    print(f"Moeda inválida: {p}")
        elif cmd.startswith("SELECIONAR"):
            cod = cmd[9:].strip()
            m.comprar(cod)
        elif cmd == "SALDO":
            print(f"Saldo atual: {m.saldo:.2f}€")
        elif cmd == "SAIR":
            m.salvar()
            print("Estado salvo. Até à próxima!")
            break
        else:
            print("Comando desconhecido.")

if __name__ == "__main__":
    main()
