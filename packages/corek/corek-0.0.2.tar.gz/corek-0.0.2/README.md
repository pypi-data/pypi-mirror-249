# Corek
An expression parser and evaluator for simple comparison expressions in Python. Only supports numeric comparisons.

## Example

```python

from corek import RulesEngine

engine = RulesEngine()

input_data = {
    'a': 10,
    'b': 2,
    'c':3
}

print(engine.evaluate_rule('a == 10', input_data)) # True
print(engine.evaluate_rule('a > 10', input_data)) # False
print(engine.evaluate_rule('(a + b) > 10', input_data)) # True

```