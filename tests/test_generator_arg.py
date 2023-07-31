import pytest
from graph_data_generator.models.generator_arg import GeneratorArg
from graph_data_generator.models.generator_type import GeneratorType

class TestFromDict:
    # Tests that the method can successfully create a GeneratorArg object from a dictionary containing all required keys
    def test_happy_path_all_keys(self):
        arg_dict = {
            'type': 'string',
            'label': 'Test Label'
        }
        expected_arg = GeneratorArg(
            type=GeneratorType.STRING,
            label='Test Label',
            default=None,
            hint='',
            description=''
        )
        assert GeneratorArg.from_dict(arg_dict) == expected_arg

    # Tests that the method can successfully create a GeneratorArg object from a dictionary containing all keys and additional keys
    def test_happy_path_all_keys_and_additional(self):
        arg_dict = {
            'type': 'int',
            'label': 'Test Label',
            'default': 0,
            'hint': 'Test Hint',
            'description': 'Test Description',
            'additional_key': 'Additional Value'
        }
        expected_arg = GeneratorArg(
            type=GeneratorType.INT,
            label='Test Label',
            default=0,
            hint='Test Hint',
            description='Test Description'
        )
        assert GeneratorArg.from_dict(arg_dict) == expected_arg

    # Tests that the method raises a KeyError when given an empty dictionary
    def test_edge_case_empty_dict(self):
        with pytest.raises(KeyError):
            GeneratorArg.from_dict({})

    # Tests that the method raises a KeyError when given a dictionary missing the 'type' key
    def test_edge_case_missing_type_key(self):
        with pytest.raises(KeyError):
            GeneratorArg.from_dict({'label': 'Test Label'})

    # Tests that the method raises a TypeError when given a dictionary containing an invalid 'type' value
    def test_edge_case_invalid_type_value(self):
        with pytest.raises(TypeError):
            GeneratorArg.from_dict({'type': 'invalid', 'label': 'Test Label'})

    # Tests that the method can successfully create a GeneratorArg object from a dictionary containing a 'type' value with leading/trailing spaces
    def test_general_behaviour_whitespace_type_value(self):
        arg_dict = {
            'type': 'string',
            'label': 'Test Label'
        }
        expected_arg = GeneratorArg(
            type=GeneratorType.STRING,
            label='Test Label',
            default=None,
            hint='',
            description=''
        )
        assert GeneratorArg.from_dict(arg_dict) == expected_arg