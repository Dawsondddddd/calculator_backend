import math
import re

MAX_EXPRESSION_LENGTH = 200

TOKEN_PATTERN = re.compile(r"\s*(?:(\d+(?:\.\d+)?|\.\d+)|([()+\-*/]))")


class ExpressionError(ValueError):
    pass


def tokenize(text):
    tokens = []
    position = 0
    while position < len(text):
        match = TOKEN_PATTERN.match(text, position)
        if match is None:
            raise ExpressionError("非法字符: %s" % text[position])
        number, operator = match.groups()
        tokens.append(number if number is not None else operator)
        position = match.end()
    if not tokens:
        raise ExpressionError("表达式不能为空")
    return tokens


class ExpressionParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def parse(self):
        value = self.expression()
        if self.position != len(self.tokens):
            raise ExpressionError("表达式格式错误")
        return value

    def peek(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def expression(self):
        value = self.term()
        while self.peek() in ("+", "-"):
            operator = self.tokens[self.position]
            self.position += 1
            right = self.term()
            value = value + right if operator == "+" else value - right
        return value

    def term(self):
        value = self.unary()
        while self.peek() in ("*", "/"):
            operator = self.tokens[self.position]
            self.position += 1
            right = self.unary()
            if operator == "*":
                value *= right
            else:
                if right == 0:
                    raise ExpressionError("除数不能为 0")
                value /= right
        return value

    def unary(self):
        token = self.peek()
        if token in ("+", "-"):
            self.position += 1
            value = self.unary()
            return value if token == "+" else -value
        return self.primary()

    def primary(self):
        token = self.peek()
        if token is None:
            raise ExpressionError("表达式不完整")
        if token == "(":
            self.position += 1
            value = self.expression()
            if self.peek() != ")":
                raise ExpressionError("括号不匹配")
            self.position += 1
            return value
        if token == ")" or token in ("+", "-", "*", "/"):
            raise ExpressionError("表达式格式错误")
        self.position += 1
        return float(token)


def calculate(expression):
    if not isinstance(expression, str):
        raise ExpressionError("表达式必须是字符串")

    text = expression.strip()
    if not text:
        raise ExpressionError("表达式不能为空")
    if len(text) > MAX_EXPRESSION_LENGTH:
        raise ExpressionError("表达式过长")

    value = ExpressionParser(tokenize(text)).parse()
    if not math.isfinite(value):
        raise ExpressionError("计算结果无效")

    value = round(value, 10)
    return int(value) if value.is_integer() else value
