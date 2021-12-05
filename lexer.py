import re
from dataclasses import dataclass


@dataclass
class TokenType:
    name: str
    regex: str


@dataclass
class Token:
    type_: TokenType
    text: str
    pos: int


token_types_list = {
    'VARIABLE': TokenType('VARIABLE', r'[A-Z]'),
    'AND': TokenType('AND', r'&'),
    'OR': TokenType('OR', r'\|'),
    'EQUIVALENCE': TokenType('EQUIVALENCE', r'<\->'),
    'IMPLICATION': TokenType('IMPLICATION', r'\->'),
    'DENIAL': TokenType('DENIAL', r'~'),
    'SPACE': TokenType('SPACE', r'[ \n\t\r]'),
    'LPAR': TokenType('LPAR', r'\('),
    'RPAR': TokenType('RPAR', r'\)'),
}


class Lexer:
    code: str
    pos: int = 0
    token_list: list[Token] = []

    def __init__(self, code: str):
        self.code = code

    def lex_analysis(self) -> list[Token]:
        while self.next_token():
            pass
        self.token_list = list(filter(lambda x: x.type_ != token_types_list['SPACE'], self.token_list))
        return self.token_list

    def next_token(self) -> bool:
        if self.pos >= len(self.code):
            return False
        
        for token_type in token_types_list.values():
            result = re.match('^' + token_type.regex, self.code[self.pos:])
            if result:
                token = Token(token_type, result.group(0), self.pos)
                self.pos += len(result.group(0))
                self.token_list.append(token)
                return True
        raise Exception(f"На позиції {self.pos} помилка!")
        
