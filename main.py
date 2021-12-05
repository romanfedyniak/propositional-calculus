import re
from itertools import product

from lexer import Lexer
from parser import Parser


print(
"""A-Z    Variable
~   Negation
&   Conjunction
|   Disjunction
->  Implication
<-> Equivalence
"""
)
expression = input('print the expression: ')
lexer = Lexer(expression)
lexer.lex_analysis()
parser = Parser(lexer.token_list)
root_node = parser.parse_expression()

format_string = '{}\t{}'
variables = sorted(set(re.findall(r'[A-Z]', expression)))
all_options = product([0, 1], repeat=len(variables))

print()
print(format_string.format("\t".join(variables), expression))
for option in all_options:
    parser.set_variable_values({key: value for key, value in zip(variables, option)})
    print(format_string.format("\t".join(map(str, option)), parser.run(root_node)))
