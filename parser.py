from AST import BinOperationNode, ExpressionNode, UnarOperationNode, VariableNode
from lexer import Token, TokenType, token_types_list


class Parser:
    tokens: "list[Token]"
    pos: int = 0
    variable_values: dict[str, int]

    def __init__(self, tokens: "list[Token]"):
        self.tokens = tokens

    def set_variable_values(self, variable_values: dict[str, int]):
        self.variable_values = variable_values

    def match(self, *expected: list[TokenType]) -> Token | None:
        if self.pos < len(self.tokens):
            current_token = self.tokens[self.pos]
            if len(list(filter(lambda x: x.name == current_token.type_.name, expected))) > 0:
                self.pos += 1
                return current_token
        return None

    def parse_binary_operator(self) -> Token | None:
        operator = self.match(token_types_list['AND'], token_types_list['OR'], token_types_list['IMPLICATION'], token_types_list['EQUIVALENCE'])
        if operator is not None:
            return operator
        return None

    def require(self, *expected: "list[TokenType]") -> Token:
        token = self.match(*expected)
        if not token:
            raise Exception(f"На позиції {self.pos} очікується {expected[0].name}")
        return token

    def parse_unar(self) -> ExpressionNode:
        operator_unar = self.match(token_types_list['DENIAL'])
        if operator_unar is not None:
            token = self.match(token_types_list['VARIABLE'], token_types_list['LPAR'])
            if token is None:
                raise Exception(f"На позиції {self.pos} помилка")
            self.pos -= 1
            operand = None
            if token.type_.name == token_types_list['VARIABLE'].name:
                operand = self.parse_variable()
            elif token.type_.name == token_types_list['LPAR'].name:
                operand = self.parse_parentheses()
            return UnarOperationNode(operator_unar, operand)
        raise Exception(f"Очікується унарний оператор {self.pos} на позиції")

    def parse_variable(self) -> ExpressionNode:
        variable = self.match(token_types_list['VARIABLE'])
        if variable is not None:
            return VariableNode(variable)
        raise Exception(f"Очікується змінна на {self.pos} позиції")

    def parse_parentheses(self) -> ExpressionNode:
        if self.match(token_types_list['LPAR']) is not None:
            node = self.parse_formula()
            self.require(token_types_list['RPAR'])
            return node
        else:
            if self.match(token_types_list['VARIABLE']) is not None:
                self.pos -= 1
                return self.parse_variable()
            return self.parse_unar()

    def parse_formula(self) -> ExpressionNode:
        left_node = self.parse_parentheses()
        operator = self.parse_binary_operator()
        while operator is not None:
            right_node = self.parse_parentheses()
            left_node = BinOperationNode(operator, left_node, right_node)
            operator = self.parse_binary_operator()
        return left_node

    def parse_expression(self) -> ExpressionNode:
        variable_node = None

        if self.match(token_types_list['VARIABLE']) is not None:
            self.pos -= 1
            variable_node = self.parse_variable()
        elif self.match(token_types_list['LPAR']) is not None:
            self.pos -= 1
            variable_node = self.parse_parentheses()
        else:
            variable_node = self.parse_unar()

        binary_operator = self.parse_binary_operator()
        if binary_operator is not None:
            right_expression = self.parse_formula()
            binary_node = BinOperationNode(binary_operator, variable_node, right_expression)
            return binary_node
        elif variable_node is not None:
            return variable_node
        raise Exception(f"Помилка на {self.pos} позиції")

    def run(self, node: ExpressionNode):
        if isinstance(node, VariableNode):
            return self.variable_values[node.variable.text]
        if isinstance(node, UnarOperationNode):
            if node.operator.type_.name == token_types_list['DENIAL'].name:
                return 1 if self.run(node.operand) == 0 else 0
        if isinstance(node, BinOperationNode):
            node_bin_type = node.operator.type_.name
            if node_bin_type == token_types_list['AND'].name:
                return self.run(node.left_node) and self.run(node.right_node)
            elif node_bin_type == token_types_list['OR'].name:
                return self.run(node.left_node) or self.run(node.right_node)
            elif node_bin_type == token_types_list['IMPLICATION'].name:
                return int(not(self.run(node.left_node)) or self.run(node.right_node))
            elif node_bin_type == token_types_list['EQUIVALENCE'].name:
                return int(self.run(node.left_node) == self.run(node.right_node))
