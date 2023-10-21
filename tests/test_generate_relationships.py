# Existing imports
from graph_data_generator.logic.generate_relationships import generate_relationship_properties
from graph_data_generator.logic.generate_relationships import generate_relationship_records
from graph_data_generator.logic.generate_relationships import generate_relationships

import pytest


@pytest.fixture
def sample_properties():
    return {
        "name": {"string": []},
        "age": {"int": [25, 35]}
    }

class TestGenerateRelationshipProperties:
    def test_generate_relationship_properties_normal(self, sample_properties):
        output = generate_relationship_properties(sample_properties)

        assert '_uid' in output
        assert 'name' in output
        assert output['name'] == ''

    def test_generate_relationship_properties_no_input(self):
        output = generate_relationship_properties({})

        assert '_uid' in output

    def test_generate_relationship_properties_invalid_input(self):
        with pytest.raises(Exception):
            output = generate_relationship_properties('invalid')

@pytest.fixture
def sample_nodes():
    return {
        'n1': [
            {'name': 'Alice', '_uid':'01'},
            {'name': 'Bob', '_uid': '02'}
        ],
        'n2': [
            {'name': 'Acme Co', '_uid':'03'}
        ]
    }

@pytest.fixture
def sample_rel_input():
    return {
        'id': 'r1',
        'type': 'EMPLOYED_BY',
        'fromId': 'n2', 
        'toId': 'n1',
        'properties': {
            'COUNT': 2
        },
    }

@pytest.fixture
def sample_nodes_missing():
    return {
        'n2': [
            {'name': 'Acme Co', '_uid':'01'}
        ]
    }

@pytest.fixture
def sample_nodes_invalid():
    return {
        'n1': 'invalid',
        'n2': [
            {'name': 'Acme Co', '_uid':'01'}
        ]
    }

class TestGenerateRelationshipRecords:

    def test_generate_relationship_records_count(self, sample_nodes, sample_rel_input):
        output = generate_relationship_records(sample_rel_input, sample_nodes)
    
        assert len(output) == 2 

    def test_generate_relationship_records_missing_nodes(self, sample_rel_input, sample_nodes_missing):
        with pytest.raises(Exception):
            output = generate_relationship_records(sample_rel_input, sample_nodes_missing)

    def test_generate_relationship_records_invalid_nodes(self, sample_rel_input, sample_nodes_invalid):
        with pytest.raises(Exception):
            output = generate_relationship_records(sample_rel_input, sample_nodes_invalid) 

@pytest.fixture
def sample_input():
    return [
        {
            "id": "r1",
            "fromId": "n1",
            "toId": "n2",
            "type": "RELATED",
            "properties": {
                "since": "2022-01-01",
                "COUNT": 3 
            }
        }
    ]

# @pytest.fixture 
# def sample_nodes():
#     return {
#         "n1": [
#             {"name": "Alice"},
#             {"name": "Bob"}
#         ],
#         "n2": [
#             {"name": "Acme Co."},
#             {"name": "Stark Industries"}
#         ]
#     }

# @pytest.fixture
# def sample_nodes_missing():
#     return {
#         "n1": [
#             {"name": "Alice"},
#             {"name": "Bob"}
#         ]
#     }

# class TestGenerateRelationships:

#     def test_generate_relationships_output_format(self, sample_input, sample_nodes):
#         output = generate_relationships(sample_input, sample_nodes)
        
#         assert isinstance(output, dict)
#         assert 'r1' in output
#         assert isinstance(output['r1'], list)

#     def test_generate_relationships_invalid_input(self, sample_nodes):
#         with pytest.raises(Exception):
#             output = generate_relationships('invalid', sample_nodes)

#     def test_generate_relationships_missing_nodes(self, sample_input, sample_nodes_missing):
#         with pytest.raises(Exception):
#             output = generate_relationships(sample_input, sample_nodes_missing)