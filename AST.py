from lexer import Token


class ExpressionNode:
    pass



class VariableNode(ExpressionNode):
    variable: Token

    def __init__(self, variable: Token):
        self.variable = variable


class BinOperationNode(ExpressionNode):
    operator: Token
    left_node: ExpressionNode
    right_node: ExpressionNode

    def __init__(self, oparator: Token, left_node: ExpressionNode, right_node: ExpressionNode):
        self.operator = oparator
        self.left_node = left_node
        self.right_node = right_node


class UnarOperationNode(ExpressionNode):
    operator: Token
    operand: ExpressionNode

    def __init__(self, operator: Token, operand: ExpressionNode):
        self.operator = operator
        self.operand = operand
