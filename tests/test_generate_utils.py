# tests/test_generate_utils.py
import pytest
from graph_data_generator.logic.generate_utils import property_contains_reference_generator, preprocess_nodes, preprocess_relationships, convert_dict_to_csv, reference_generator_names_only

# class TestPropertyContainsPointerDesignator:
#     def test_property_contains_pointer_designator_true(self):
#         obj = {'prop1': '@node1'}
#         assert property_contains_pointer_designator(obj)

#     def test_property_contains_pointer_designator_false(self):
#         obj = {'prop1': 'value1'}
#         assert not property_contains_pointer_designator(obj)

#     def test_property_contains_pointer_designator_escaped(self):
#         obj = {'prop1': '\\@value1'}    # Would pass a non-pointer string of value @value1
#         obj2 = {'prop1': '@\\@value1'}  # Would pass as pointer value @value1
#         obj3 = {'prop1': '\\@@value1'}  # Would pass as pointer value @value1
#         obj4 = {'prop1': '@@value1'}    # Would pass as pointer value @value1
#         assert not property_contains_pointer_designator(obj)
#         assert property_contains_pointer_designator(obj2)
#         assert property_contains_pointer_designator(obj3)
#         assert property_contains_pointer_designator(obj4)

class TestReferenceGeneratorsOnly:
    # Currently only a single 'reference' reference generator available

    def test_property_contains_reference_generator_true(self):
        # Configuration property values should all be strings
        obj = "{\"reference\": [\"\"]}"
        assert property_contains_reference_generator(obj), f'"reference" not found in reference generator names list: {reference_generator_names_only}'

    def test_property_contains_reference_generator_false(self):
        obj = "{\"add_floats\": [\"a_value\"]}"
        assert not property_contains_reference_generator(obj)

    def test_property_contains_reference_generator_invalid_json(self):
        obj = "{\"add_floats\"}"
        assert not property_contains_reference_generator(obj)

    def test_property_contains_reference_generator_invalid_objecct(self):
        obj = {"add_floats"}
        assert not property_contains_reference_generator(obj)

    def test_property_contains_reference_generator_multiple_keys(self):
        obj = "{\"reference\": [\"a_value\"], \"other\": [\"b_value\"]}"
        assert not property_contains_reference_generator(obj)

    def test_property_contains_reference_generator_wrong_key(self):
        obj = "{\"chicken\": [\"egg\"]}"
        assert not property_contains_reference_generator(obj)

class TestPreprocessNodes:
    def test_preprocess_drops_nodes_missing_properties(self):
        # All values from arrows json are automatically returned as strings
        # Including numbers here in case non-strings are otherwise introduced
        input_data = [{'id': 1, 'caption':"test", "labels":[]}, {'id': 2, 'caption':'test', 'labels':[],'properties': {}}]
        expected = [{'id': 2, 'caption':'test', 'labels':[],'properties': {}}]
        output = preprocess_nodes(input_data)
        assert output == expected, f'output: {output}'

    def test_preprocess_drops_nodes_missing_id(self):
        # All values from arrows json are automatically returned as strings
        # Including numbers here in case non-strings are otherwise introduced
        input_data = [{'caption':"test", "labels":[]}, {'id': 2, 'caption':'test', 'labels':[],'properties': {}}]
        expected = [{'id': 2, 'caption':'test', 'labels':[],'properties': {}}]
        output = preprocess_nodes(input_data)
        assert output == expected, f'output: {output}'

    def test_preprocess_drops_nodes_missing_caption(self):
        # All values from arrows json are automatically returned as strings
        # Including numbers here in case non-strings are otherwise introduced
        input_data = [{'id': 1, "labels":[], 'properties':{}}, {'id': 2, 'caption':'test', 'labels':[],'properties': {}}]
        expected = [{'id': 2, 'caption':'test', 'labels':[],'properties': {}}]
        output = preprocess_nodes(input_data)
        assert output == expected, f'output: {output}'

    def test_preprocess_drops_nodes_missing_labels(self):
        # All values from arrows json are automatically returned as strings
        # Including numbers here in case non-strings are otherwise introduced
        input_data = [{'id': 1, 'caption':"test", "properties":{}}, {'id': 2, 'caption':'test', 'labels':[],'properties': {}}]
        expected = [{'id': 2, 'caption':'test', 'labels':[],'properties': {}}]
        output = preprocess_nodes(input_data)
        assert output == expected, f'output: {output}'

    def test_preprocess_nodes_sorts_by_pointer_designator(self):
        input_data = [
            {'id': 1, 'caption':'', 'labels':[], 'properties': {'prop1': 'value1'}},
            {'id': 2, 'caption':'', 'labels':[], 'properties': {'prop2': '{\"reference\": [\"\"]}'}},
            {'id': 3, 'caption':'', 'labels':[], 'properties': {'prop3': 'value3'}}
        ]
        expected = [
            {'id': 1, 'caption':'', 'labels':[], 'properties': {'prop1': 'value1'}},
            {'id': 3, 'caption':'', 'labels':[], 'properties': {'prop3': 'value3'}},
            {'id': 2, 'caption':'', 'labels':[], 'properties': {'prop2': '{\"reference\": [\"\"]}'}}
        ]
        output = preprocess_nodes(input_data)
        print(f'output: {output}')
        assert output == expected

class TestPreprocssRelationships:
    def test_preprocess_drops_relationships_missing_properties(self):
        # All values from arrows json are automatically returned as strings
        # Including numbers here in case non-strings are otherwise introduced
        input_data = [{'id': 1, 'fromId':'', 'toId':'', 'type':"test"}, {'id': 2, 'type':'test', 'toId':'', 'fromId':'','properties': {}}]
        expected = [{'id': 2, 'type':'test', 'toId':'', 'fromId':'','properties': {}}]
        output = preprocess_relationships(input_data)
        assert output == expected, f'output: {output}'

    def test_preprocess_drops_relationships_missing_id(self):
        # All values from arrows json are automatically returned as strings
        # Including numbers here in case non-strings are otherwise introduced
        input_data = [{'fromId':'', 'toId':'', 'type':"test", 'properties':{}}, {'id': 2, 'type':'test', 'toId':'', 'fromId':'','properties': {}}]
        expected = [{'id': 2, 'type':'test', 'toId':'', 'fromId':'','properties': {}}]
        output = preprocess_relationships(input_data)
        assert output == expected, f'output: {output}'

    def test_preprocess_drops_relationships_missing_type(self):
        # All values from arrows json are automatically returned as strings
        # Including numbers here in case non-strings are otherwise introduced
        input_data = [{'id':"test", 'fromId':'', 'toId':'', 'properties':{}}, {'id': 2, 'type':'test', 'toId':'', 'fromId':'','properties': {}}]
        expected = [{'id': 2, 'type':'test', 'toId':'', 'fromId':'','properties': {}}]
        output = preprocess_relationships(input_data)
        assert output == expected, f'output: {output}'

    def test_preprocess_drops_relationships_missing_fromId(self):
        # All values from arrows json are automatically returned as strings
        # Including numbers here in case non-strings are otherwise introduced
        input_data = [{'id':1, 'toId':'', 'type':"test", 'properties':{}}, {'id': 2, 'type':'test', 'toId':'', 'fromId':'','properties': {}}]
        expected = [{'id': 2, 'type':'test', 'toId':'', 'fromId':'','properties': {}}]
        output = preprocess_relationships(input_data)
        assert output == expected, f'output: {output}'

    def test_preprocess_drops_relationships_missing_toId(self):
        # All values from arrows json are automatically returned as strings
        # Including numbers here in case non-strings are otherwise introduced
        input_data = [{'id':'', 'fromId':'', 'type':"test", 'properties':{}}, {'id': 2, 'type':'test', 'toId':'', 'fromId':'','properties': {}}]
        expected = [{'id': 2, 'type':'test', 'toId':'', 'fromId':'','properties': {}}]
        output = preprocess_relationships(input_data)
        assert output == expected, f'output: {output}'

    def test_preprocess_relationships_sorts_by_pointer_designator(self):
        input_data = [
            {'id': 1, 'type':'', 'fromId':'', 'toId':'', 'properties': {'prop1': 'value1'}},
            {'id': 2, 'type':'', 'fromId':'', 'toId':'', 'properties': {'prop2': '{\"reference\": [\"\"]}'}},
            {'id': 3, 'type':'', 'fromId':'', 'toId':'', 'properties': {'prop3': 'value3'}}
        ]
        expected = [
            {'id': 1, 'type':'', 'fromId':'', 'toId':'', 'properties': {'prop1': 'value1'}},
            {'id': 3, 'type':'', 'fromId':'', 'toId':'', 'properties': {'prop3': 'value3'}},
            {'id': 2, 'type':'', 'fromId':'', 'toId':'', 'properties': {'prop2': '{\"reference\": [\"\"]}'}}
        ]
        output = preprocess_relationships(input_data)
        print(f'output: {output}')
        assert output == expected

class TestConvertDictToCSV:
    @pytest.fixture
    def sample_dict(self):
        return [
            {'id': 1, 'name': 'John Doe'},
            {'id': 2, 'name': 'Jane'},
            {'id': 3, 'name': 'Jane, Doe'}
        ]

    def test_convert_dict_to_csv_returns_tuple(self, sample_dict):
        result = convert_dict_to_csv('test.csv', sample_dict)
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_convert_dict_to_csv_filename(self, sample_dict):
        filename = 'mydata.csv'
        result = convert_dict_to_csv(filename, sample_dict)
        assert result[0] == filename

    def test_convert_dict_to_csv_contents(self, sample_dict):
        result = convert_dict_to_csv('test.csv', sample_dict)
        contents = result[1]
        assert 'id,name' in contents
        assert '1,John Doe' in contents
        assert '2,Jane' in contents
        assert '3,"Jane, Doe"' in contents, f'Contents: {contents}'

    def test_convert_dict_to_csv_bad_data(self):
        with pytest.raises(Exception):
            convert_dict_to_csv('test.csv', None)