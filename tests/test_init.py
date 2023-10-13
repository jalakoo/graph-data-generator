# Test the high level package functions

import pytest
from graph_data_generator import generate_dicts_only, generate_csvs_only

@pytest.fixture
def sample_input():
    return {
        "nodes": [
            {
                "id": "n1",
                "caption":"Person",
                "properties": {
                    "name": "string"
                }
            },
            {
                "id": "n2",
                "caption":"Company",
                "properties": {
                    "name": "string"
                }
            }
        ],
        "relationships": [
            {
                "id":"n0",
                "fromId":"n1",
                "toId":"n2",
                "properties":{
                }
            }
        ]
    }

@pytest.fixture 
def sample_input_no_nodes():
    return {
        "relationships": []
    }

class TestGenerateDicts:
    def test_generate_dicts_valid(self, sample_input):
        output = generate_dicts_only(sample_input)
        assert isinstance(output, dict)
        assert 'nodes' in output
        assert isinstance(output['nodes'], dict), f'Expected a dictionary of node records. Instead got {output["nodes"]}'
        assert 'relationships' in output
        assert isinstance(output['relationships'], dict)

    def test_generate_dicts_invalid_input(self):
        with pytest.raises(Exception):
            output = generate_dicts_only("invalid")

    def test_generate_dicts_missing_nodes(self, sample_input_no_nodes):
        with pytest.raises(Exception):
            output = generate_dicts_only(sample_input_no_nodes) 

class TestGenerateCSVs:
    def test_generate_csvs_valid(self, sample_input):
        output = generate_csvs_only(sample_input)
        assert isinstance(output, list)
        assert len(output) > 0
        for filename, csv in output:
            assert isinstance(filename, str)
            assert isinstance(csv, str)

    def test_generate_csvs_invalid_input(self):
        with pytest.raises(Exception):
            output = generate_csvs_only("invalid input")

    def test_generate_csvs_empty_input(self):
        with pytest.raises(Exception):
            output = generate_csvs_only({})
