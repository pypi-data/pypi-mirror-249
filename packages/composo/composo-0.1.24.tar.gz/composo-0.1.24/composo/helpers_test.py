import pytest
from composo.helpers import match_parameters, parse_parameters
from composo.package_primitives import *

class TestMatchParameters:
    def test_function_with_no_params_and_nothing_passed(self):
        def adder():
            return

        assert match_parameters(adder, *[], **{}) == {}

    def test_function_with_no_params_and_stuff_passed(self):
        def adder():
            return

        assert match_parameters(adder, *[1], **{'b': 2}) == {}

    def test_function_with_args_only_and_args_passed(self):
        def adder(a, b):
            return

        assert match_parameters(adder, *[1, 2], **{}) == {'a': 1, 'b': 2}

    def test_function_with_args_only_and_kwargs_passed(self):
        def adder(a, b):
            return

        assert match_parameters(adder, *[], **{'a': 1, 'b': 2}) == {'a': 1, 'b': 2}

    def test_function_with_kwargs_only_and_kwargs_passed(self):
        def adder(a=3, b=4):
            return

        assert match_parameters(adder, *[], **{'a': 1, 'b': 2}) == {'a': 1, 'b': 2}

    def test_function_with_kwargs_only_and_nothing_passed(self):
        def adder(a=3, b=4):
            return

        assert match_parameters(adder, *[], **{}) == {'a': 3, 'b': 4}

    def test_function_with_kwargs_only_and_arg_passed(self):
        def adder(a=3, b=4):
            return

        assert match_parameters(adder, *[1], **{}) == {'a': 1, 'b': 4}

    def test_function_with_mixed_and_mixed_passed(self):
        def adder(a, b=4):
            return

        assert match_parameters(adder, *[], **{'a': 1}) == {'a': 1, 'b': 4}

RANDOM_STRING = "lsdkjhfksd"
class TestParameterParsing:
    
    def test_empty(self):
        
        def adder():
            return

        assert parse_parameters(adder, *[], **{}) == []
    
    def test_simple(self):
        
        def adder(a: IntParam(description=RANDOM_STRING, min=0, max=1), b: StrParam(description=RANDOM_STRING), c=3):
            return

        ret = parse_parameters(adder, *[1, "asdasf"], **{})
        assert ret[0].description == RANDOM_STRING
        assert ret[0].allowableMin == 0
        assert ret[0].param_type == ParameterType.INTEGER.value
        assert ret[2].live_working_value == 3
        
        
if __name__ == "__main__":
    pytest.main([__file__])
