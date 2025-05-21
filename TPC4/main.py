import sys
from ply.lex import lex

tokens = (
    "COMANDO",
    "VARIAVEL",
    "LCRLYB",
    "RCRLYB",
    "PONTO",
    "DOIS_PONTOS",
    "NUM",
    "LINGUA",
    "STRING",
    "INFO"
)

t_LCRLYB = r'\{'
t_RCRLYB = r'\}'
t_PONTO = r'\.'
t_DOIS_PONTOS = r'\:'
t_ignore = ' \t'

def t_COMANDO(t):
    r'(select|where|LIMIT)'
    return t

def t_VARIAVEL(t):
    r'\?\w+'
    return t

def t_INFO(t):
    r'\w+:\w+'
    return t

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_LINGUA(t):
    r'\@[a-z]+'
    return t

def t_STRING(t):
    r'\"[^"]*\"'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_COMMENT(t):
    r'\#.*'
    pass

def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex()

def main():
    if len(sys.argv) != 2:
        print("Uso: python lexer.py nome_ficheiro")
        return
    
    filename = sys.argv[1]
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            texto = f.read()
    except FileNotFoundError:
        print(f"Erro: ficheiro '{filename}' não encontrado.")
        return

    lexer.input(texto)
    for tok in lexer:
        print(f"Token ({tok.type}, '{tok.value}')")

if __name__ == "__main__":
    main()
