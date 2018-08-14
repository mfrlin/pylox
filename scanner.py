class Token():
    TOKEN_TYPES = [
        # single-characters tokens
        'LEFT_PAREN',
        'RIGHT_PAREN',
        'LEFT_BRACE',
        'RIGHT_BRACE',
        'COMMA',
        'DOT',
        'MINUS',
        'PLUS',
        'SEMICOLON',
        'SLASH',
        'STAR',

        # one or two character tokens
        'BANG',
        'BANG_EQUAL',
        'EQUAL',
        'EQUAL_EQUAL',
        'GREATER',
        'GREATER_EQUAL',
        'LESS',
        'LESS_EQUAL',

        # literals
        'IDENTIFIER',
        'STRING',
        'NUMBER',

        # keywords
        'AND',
        'CLASS',
        'ELSE',
        'FALSE',
        'FUN',
        'FOR',
        'IF',
        'NIL',
        'OR',
        'PRINT',
        'RETURN',
        'SUPER',
        'THIS',
        'TRUE',
        'VAR',
        'WHILE',

        'EOF',

    ]
    def __init__(self, type_, line_num, lexeme='', literal=None):
        if type_ not in TOKEN_TYPES:
            raise ValueError('Unrecognized token type: {}'.format(type_))
        self.type_ = type_
        self.lexeme = lexeme
        self.literal = literal
        self.line_num = line_num

    def __str__(self):
        return ' '.join([self.type_, self.lexeme, self.literal])


def scan_tokens(source):
    while not finished:
        start = 

    tokens.add(Token('EOF', line))
