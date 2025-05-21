import json

class Maquina:
    def __init__(self):
        with open("stock.json", "r", encoding="utf-8") as f:
            produtos_lista = json.load(f)
        self.produtos = {p['cod']: p for p in produtos_lista}
        self.saldo = 0

    def listar_produtos(self):
        print("Produtos disponíveis:")
        for p in self.produtos.values():
            print(f"{p['cod']}: {p['nome']} - {p['preco']:.2f}€ (Qt: {p['quant']})")

    def inserir_saldo(self, valor):
        self.saldo += valor
        print(f"Saldo atual: {self.saldo:.2f}€")

    def comprar(self, cod):
        produto = self.produtos.get(cod)
        if not produto:
            print("Produto não encontrado.")
            return
        if produto['quant'] == 0:
            print(f"O produto {produto['nome']} está esgotado.")
            return
        if self.saldo < produto['preco']:
            print(f"Saldo insuficiente para {produto['nome']}.")
            return
        produto['quant'] -= 1
        self.saldo -= produto['preco']
        print(f"Comprou {produto['nome']}. Saldo restante: {self.saldo:.2f}€")

    def salvar(self):
        with open("stock.json", "w", encoding="utf-8") as f:
            json.dump(list(self.produtos.values()), f, indent=4, ensure_ascii=False)
