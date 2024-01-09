import pytest

from corek.rules_engine import RulesEngine

@pytest.fixture
def rules_engine():
    engine = RulesEngine()
    return engine

@pytest.mark.parametrize("rule, input_data, expected_result", [
    ('a == 10',{'a':10},True),
    ('a == 10',{'a':11},False),
    ('a > 10',{'a':11},True),
    ('a > 10',{'a':10},False),
    ('(a + b) > 10',{'a':10,'b':1},True),
    ('(a + b * c) > 10',{'a':10,'b':2,'c':0},False),
    ('(a + b * c) > 9',{'a':10,'b':2,'c':0},True),
    ('(a / b * c) < 10',{'a':10,'b':2,'c':3},False),
    ('(a / b - c) < 10',{'a':10,'b':2,'c':3},True),
    ('a + 2 == 12',{'a':10},True),
    ('a + 3 == 12',{'a':10},False),
])
def test_simple_numeric_conditions(rules_engine, rule, input_data, expected_result):
    actual = rules_engine.evaluate_rule(rule, input_data)
    assert actual == expected_result

@pytest.mark.parametrize("rule, input_data, expected_result", [
    ('a == "hello"',{'a':'hello'},True),
    ("a == \"hello\"",{'a':'hello'},True),
])
def test_simple_string_comparisons(rules_engine, rule, input_data, expected_result):
    actual = rules_engine.evaluate_rule(rule, input_data)
    assert actual == expected_result