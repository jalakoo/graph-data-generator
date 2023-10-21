import pytest
from graph_data_generator.logic.generate_nodes import generate_a_node_record, generate_node_records, generate_nodes

class TestGenerateANodeRecord:
    # Smoke tests - not testing generators here
    def test_generate_a_node_record_normal(self):
        input = {
            'properties': {
                'name': 'string',
                'age': 'int'
            }
        }

        output = generate_a_node_record(input)

        assert 'name' in output
        assert 'age' in output
        assert len(output) == 3

    def test_generate_a_node_record_no_properties(self):
        input = {}

        output = generate_a_node_record(input)

        assert '_uid' in output

    def test_generate_a_node_record_empty_properties(self):
        input = {
            'properties': {}
        }

        output = generate_a_node_record(input)

        assert '_uid' in output

class TestGenerateNodeRecords:
    def test_generate_node_records_count(self):
        input = {
            'properties': {
                'name': 'string', 
                'COUNT': '3'
            }
        }
        output = generate_node_records(input)

        assert len(output) == 3

    def test_generate_node_records_count_range(self):
        input = {
            'properties': {
                'name': 'string', 
                'COUNT': '0-3'
            }
        }
        output = generate_node_records(input)

        assert len(output) >= 0 and len(output) <= 3, f'Expected count between 0-3, instead returned: {len(output)}'

    def test_generate_node_records_count_list(self):
        input = {
            'properties': {
                'name': 'string', 
                'COUNT': '[1,3]'
            }
        }
        output = generate_node_records(input)

        assert len(output) == 1 or len(output) == 3, f'Expected count of 1 or 3, instead returned: {len(output)}'


    def test_generate_node_records_no_count(self):
        input = {
            'properties': {
                'name': 'string'
            }
        }
        output = generate_node_records(input)

        assert len(output) >= 1 and len(output) <= 100, f'Expected default count between 1-100, instead returned: {len(output)}'

    def test_generate_node_records_invalid_count(self):
        # Unexpected values for the COUNT keyword will default to a random int generator
        input = {
            'properties': {
                'name': 'string',
                'COUNT': 'invalid' 
            }
        }
        output = generate_node_records(input)

        assert len(output) >= 1 and len(output) <= 100, f'Expected default count between 1-100, instead returned: {len(output)}'


@pytest.fixture
def input_nodes():
    return [
        {
            "id": "n1",
            "position": {
                "x": 100, 
                "y": 100
            },
            "caption": "Person",
            "labels": [],
            "properties": {
                "name": "John",
                "age": 30,
                "COUNT": 3
            }
        },
        {
           "id": "n2",
           "position": {
               "x": 200,
               "y": 200  
           },
           "caption": "Company",
           "labels": [],
           "properties": {
               "name": "Acme Co",
               "employees": 100,
               "COUNT": 1
           }
        }
    ]

@pytest.fixture    
def input_nodes_missing_id():
    return [
        {
            "position": {
                "x": 100,
                "y": 100
            },
            "caption": "Person",
            "labels": [],
            "properties": {
                "name": "John",
                "age": 30
            }
        },
        {
            "id": "n2",
            "position": {
                "x": 200,
                "y": 200
            },
            "caption": "Company",
            "labels": [],
            "properties": {
                "name": "Acme Co",
                "employees": 100
            }
        }
    ]

class TestGenerateNodes:
    def test_generate_nodes_output_format(self, input_nodes):
        output = generate_nodes(input_nodes)
        assert isinstance(output, dict)
        assert 'n1' in output, f'Node id n1 missing from output: {output}'
        assert 'n2' in output, f'Node id n2 missing from output: {output}'
        assert len(output['n1']) == 3, f'n1 expected to produce 3 records, instead produced: {len(output["n1"])}'
        assert len(output['n2']) == 1, f'n2 expected to produce 1 record, instead produced: {len(output["n2"])}'
        for key, value in output.items():
            assert isinstance(key, str)
            assert isinstance(value, list)
            assert len(value) > 0

    def test_generate_nodes_missing_id(self, input_nodes_missing_id):
        output = generate_nodes(input_nodes_missing_id)
        assert len(output) == 1