from lark import Transformer, v_args

@v_args(inline=True)    # Affects the signatures of the methods
class CorekTransformer(Transformer):
    from operator import add, sub, mul, truediv as div, neg, \
        gt, lt, ge, le, eq, ne, or_, and_
    number = float
    
    def custom_str(self, string_val):
        if string_val[0] == '"' and string_val[-1] == '"':
            return string_val[1:-1]  # Remove the first and last character (the quotes)
        else:
            # Raise an exception if the first and last characters aren't quotes
            raise ValueError(f"Expected a string enclosed in double quotes, got: {string_val}")

    def __init__(self, input_values: dict):
        self.input_values = input_values

    def var(self, name):
        try:
            val = self.input_values[name]
            return val
        except KeyError:
            raise Exception("Variable not found: %s" % name)
            


