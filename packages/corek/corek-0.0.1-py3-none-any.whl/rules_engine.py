from lark import Lark
import src
from src.corek_transformer import CorekTransformer
from importlib_resources import files, as_file

class RulesEngine():

    def __init__(self):
        source_grammar = files(src).joinpath('corek_grammar.lark')
        with open(source_grammar,'r') as cgfd:
            self.corek_grammar = cgfd.read()

    def evaluate_rule(self, rule, input_values):
        parser = Lark(self.corek_grammar, parser='lalr')
        transformer = CorekTransformer(input_values=input_values)
        ast = parser.parse(rule)
        print(ast.pretty())
        evaluated_rule = transformer.transform(ast)
        return evaluated_rule


