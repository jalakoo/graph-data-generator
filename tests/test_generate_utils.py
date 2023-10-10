# tests/test_generate_utils.py
import pytest
from graph_data_generator.logic.generate_utils import property_contains_pointer_designator, preprocess_nodes, preprocess_relationships

class TestPropertyContainsPointerDesignator:
    def test_property_contains_pointer_designator_true(self):
        obj = {'prop1': '@node1'}
        assert property_contains_pointer_designator(obj)

    def test_property_contains_pointer_designator_false(self):
        obj = {'prop1': 'value1'}
        assert not property_contains_pointer_designator(obj)

    def test_property_contains_pointer_designator_escaped(self):
        obj = {'prop1': '\\@value1'}    # Would pass a non-pointer string of value @value1
        obj2 = {'prop1': '@\\@value1'}  # Would pass as pointer value @value1
        obj3 = {'prop1': '\\@@value1'}  # Would pass as pointer value @value1
        obj4 = {'prop1': '@@value1'}    # Would pass as pointer value @value1
        assert not property_contains_pointer_designator(obj)
        assert property_contains_pointer_designator(obj2)
        assert property_contains_pointer_designator(obj3)
        assert property_contains_pointer_designator(obj4)

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
            {'id': 2, 'caption':'', 'labels':[], 'properties': {'prop2': '@node1'}},
            {'id': 3, 'caption':'', 'labels':[], 'properties': {'prop3': 'value3'}}
        ]
        expected = [
            {'id': 1, 'caption':'', 'labels':[], 'properties': {'prop1': 'value1'}},
            {'id': 3, 'caption':'', 'labels':[], 'properties': {'prop3': 'value3'}},
            {'id': 2, 'caption':'', 'labels':[], 'properties': {'prop2': '@node1'}}
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
            {'id': 2, 'type':'', 'fromId':'', 'toId':'', 'properties': {'prop2': '@node1'}},
            {'id': 3, 'type':'', 'fromId':'', 'toId':'', 'properties': {'prop3': 'value3'}}
        ]
        expected = [
            {'id': 1, 'type':'', 'fromId':'', 'toId':'', 'properties': {'prop1': 'value1'}},
            {'id': 3, 'type':'', 'fromId':'', 'toId':'', 'properties': {'prop3': 'value3'}},
            {'id': 2, 'type':'', 'fromId':'', 'toId':'', 'properties': {'prop2': '@node1'}}
        ]
        output = preprocess_relationships(input_data)
        print(f'output: {output}')
        assert output == expected