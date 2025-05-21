import ply.lex as lex

# Tokens
tokens = ['PA', 'PF', 'NUM']
literals = ['+', '-', '*']

t_PA = r'\('
t_PF = r'\)'

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = ' \t\n'

def t_error(t):
    print(">> Caráter inválido:", t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

# Parser recursivo
prox_simb = None

def erro(simb):
    print("Erro sintático:", simb)
    exit(1)

def consumir(simb):
    global prox_simb
    if prox_simb and (prox_simb.type == simb or prox_simb.value == simb):
        val = prox_simb.value
        prox_simb = lexer.token()
        return val
    else:
        erro(prox_simb)

# Factor → (Expr) | NUM
def factor():
    global prox_simb
    if prox_simb.type == 'PA':
        consumir('PA')
        val = expr()
        consumir('PF')
        return val
    elif prox_simb.type == 'NUM':
        return consumir('NUM')
    else:
        erro(prox_simb)

# Term' → * Factor Term' | ε
def termp(inherited):
    global prox_simb
    if prox_simb and prox_simb.value == '*':
        consumir('*')
        val = factor()
        return termp(inherited * val)
    return inherited

# Term → Factor Term'
def term():
    return termp(factor())

# Expr' → + Term Expr' | - Term Expr' | ε
def exprp(inherited):
    global prox_simb
    if prox_simb and prox_simb.value == '+':
        consumir('+')
        return exprp(inherited + term())
    elif prox_simb and prox_simb.value == '-':
        consumir('-')
        return exprp(inherited - term())
    return inherited

# Expr → Term Expr'
def expr():
    return exprp(term())

# Interface
def parse(data):
    global prox_simb
    lexer.input(data)
    prox_simb = lexer.token()
    result = expr()
    if prox_simb is not None:
        erro(prox_simb)
    print("= ", result)

if __name__ == "__main__":
    print("Calculadora (operadores +, -, *, parêntesis):")
    while True:
        entrada = input(">> ")
        parse(entrada)
