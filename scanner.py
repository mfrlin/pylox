import string


class Token():
    # single-characters tokens
    LEFT_PAREN = 'LEFT_PAREN'
    RIGHT_PAREN = 'RIGHT_PAREN'
    LEFT_BRACE = 'LEFT_BRACE'
    RIGHT_BRACE = 'RIGHT_BRACE'
    COMMA = 'COMMA'
    DOT = 'DOT'
    MINUS = 'MINUS'
    PLUS = 'PLUS'
    SEMICOLON = 'SEMICOLON'
    STAR = 'STAR'

    # one or two character tokens
    SLASH = 'SLASH'
    # can continue with equal
    BANG = 'BANG'
    BANG_EQUAL = 'BANG_EQUAL'
    EQUAL = 'EQUAL'
    EQUAL_EQUAL = 'EQUAL_EQUAL'
    GREATER = 'GREATER'
    GREATER_EQUAL = 'GREATER_EQUAL'
    LESS = 'LESS'
    LESS_EQUAL = 'LESS_EQUAL'

    # literals
    IDENTIFIER = 'IDENTIFIER'
    STRING = 'STRING'
    NUMBER = 'NUMBER'

    # keywords
    AND = 'AND'
    CLASS = 'CLASS'
    ELSE = 'ELSE'
    FALSE = 'FALSE'
    FUN = 'FUN'
    FOR = 'FOR'
    IF = 'IF'
    NIL = 'NIL'
    OR = 'OR',
    PRINT = 'PRINT'
    RETURN = 'RETURN'
    SUPER = 'SUPER'
    THIS = 'THIS'
    TRUE = 'TRUE'
    VAR = 'VAR'
    WHILE = 'WHILE'

    EOF = 'EOF'

    ALL_TYPES = [AND, BANG, BANG_EQUAL, CLASS, 
        COMMA, DOT, ELSE, EOF, EQUAL, EQUAL_EQUAL,
        FALSE, FOR, FUN, GREATER, GREATER_EQUAL, 
        IDENTIFIER, IF, LEFT_BRACE, LEFT_PAREN, LESS, 
        LESS_EQUAL, MINUS, NIL, NUMBER, OR, PLUS, PRINT, 
        RETURN, RIGHT_BRACE, RIGHT_PAREN, SEMICOLON, SLASH, 
        STAR, STRING, SUPER, THIS, TRUE, VAR, WHILE,
        ]

    def __init__(self, type_, line_num, lexeme='', literal=None):
        if type_ not in self.ALL_TYPES:
            raise ValueError('Invalid type: {}'.format(type_))
        self.type_ = type_
        self.lexeme = lexeme
        self.literal = literal
        self.line_num = line_num

    def __str__(self):
        return 'Token: {}, literal={}, line={}'.format(self.type_, self.literal, self.line_num)


class Scanner():
    SINGLE_CHAR_TOKEN_MAP = {
        '(': Token.LEFT_PAREN,
        ')': Token.RIGHT_PAREN,
        '{': Token.LEFT_BRACE,
        '}': Token.RIGHT_BRACE,
        ',': Token.COMMA,
        '.': Token.DOT,
        '-': Token.MINUS,
        '+': Token.PLUS,
        ';': Token.SEMICOLON,
        '+': Token.STAR,
    }

    ONE_OR_TWO_CHAR_TOKEN_MAP = {
        '!': (Token.BANG, Token.BANG_EQUAL),
        '=': (Token.EQUAL, Token.EQUAL_EQUAL),
        '>': (Token.GREATER, Token.GREATER_EQUAL),
        '<': (Token.LESS, Token.LESS_EQUAL),
    }

    KEYWORD_MAP = {
        'and': Token.AND,
        'class': Token.CLASS,
        'else': Token.ELSE,
        'false': Token.FALSE,
        'fun': Token.FUN,
        'for': Token.FOR,
        'if': Token.IF,
        'nil': Token.NIL,
        'or': Token.OR,
        'print': Token.PRINT,
        'return': Token.RETURN,
        'super': Token.SUPER,
        'this': Token.THIS,
        'tru': Token.TRUE,
        'var': Token.VAR,
        'while': Token.WHILE,
    }

    def __init__(self, source):
        self._source = source
        self._current = -1
        self._line = 1
        self.tokens = []

    def scan_tokens(self):
        error_occured = False
        while True:
            try:
                self._scan_token()
            except ValueError as e:
                error_occured = True
                print(e)
            except IndexError:
                if error_occured:
                    print('Scanning finished with error')
                break

        self._append_token('EOF')
        return self.tokens

    def _scan_token(self):
        c = self._get_next_char()
        start_of_lexeme = self._current
        if c in self.SINGLE_CHAR_TOKEN_MAP:
            self._append_token(self.SINGLE_CHAR_TOKEN_MAP[c])
        elif c == '/':
            # // is comment
            if self._check_ahead('/'):
                self._skip_to_end_of_line()
            else:
                self._append_token(Token.SLASH)
        elif c in self.ONE_OR_TWO_CHAR_TOKEN_MAP:
            possible_token_types = self.ONE_OR_TWO_CHAR_TOKEN_MAP[c]
            if self._check_ahead('='):
                self._get_next_char()
                self._append_token(possible_token_types[1])
            else:
                self._append_token(possible_token_types[0])
        # skip whitespace
        elif c in [' ', '\t', '\r']:
            pass
        elif c == '\n':
            self._line += 1
        elif c == '"':
            try:
                self._collect_string()
            except IndexError:
                raise ValueError('Unexpected EOF while parsing string. Line: {}'.format(self._line))
            self._append_token(Token.STRING, literal=self._source[start_of_lexeme + 1:self._current])
        elif c.isdigit():
            self._collect_number()
            self._append_token(Token.NUMBER, literal=float(self._source[start_of_lexeme:self._current+1]))
        elif c.isalpha() or c == '_':
            self._collect_identifier()
            identifier = self._source[start_of_lexeme:self._current+1]
            token_type = self.KEYWORD_MAP.get(identifier, Token.IDENTIFIER)
            self._append_token(token_type, literal=identifier)
        else:
            raise ValueError('Unexpected character [{}] at line: {}'.format(c, self._line))

    def _check_ahead(self, c):
        return self._peek() == c

    def _peek(self, n=1):
        try:
            return self._source[self._current + n]
        except IndexError:
            return None

    def _skip_to_end_of_line(self):
        while not self._check_ahead('\n'):
            self._get_next_char()

    def _collect_string(self):
        c = self._get_next_char()
        while c != '"':
            c = self._get_next_char()
            # support multiline strings
            if c == '\n':
                self._line += 1

    def _collect_number(self):
        while self._peek() is not None and self._peek() in string.digits:
            self._get_next_char()
        if self._peek() == '.' and self._peek(2) is not None and self._peek(2) in string.digits:
            # consume dot only if it continues with a digit so we know it is a part of the number
            self._get_next_char()
            while self._peek() is not None and self._peek() in string.digits:
                # consume all the digits after the dot
                self._get_next_char()

    def _collect_identifier(self):
        c  = self._peek()
        while c is not None and (c.isalpha() or c.isdigit() or c == '_'):
            self._get_next_char()
            c = self._peek()


    def _append_token(self, type_, lexeme='', literal=None):
        self.tokens.append(Token(type_, self._line, lexeme=lexeme, literal=literal))

    def _get_next_char(self):
        self._current += 1
        return self._source[self._current]
