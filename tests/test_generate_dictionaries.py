import pytest
from graph_data_generator.logic.generate_dictionaries import generate_dictionaries 
from graph_data_generator.models.mapping import Mapping

# Test generate_dictionaries

class TestGenerateDictionaries:
        
    def test_generate_dictionaries_happy_path(self, sample_node_mapping, sample_relationship_mapping):
        # Arrange
        nodes = {'n1': sample_node_mapping}    
        relationships = {'r1': sample_relationship_mapping}
        mapping = Mapping(nodes, relationships)
        
        # Act
        result = generate_dictionaries(mapping)
        
        # Assert
        assert isinstance(result, dict)
        assert 'nodes' in result.keys()
        assert 'relationships' in result.keys()
        node_results = result['nodes']
        rels_results = result['relationships']
        assert node_results.keys() == result['nodes'].keys()
        assert rels_results.keys() == result['relationships'].keys(), f'Unexpected keys from generated result: {result}'

    def test_generate_dictionaries_missing_nodes_fails(self, sample_relationship_mapping):
        # Arrange
        # TODO: Add mock data to test
        relationships = {'r1': sample_relationship_mapping}
        mapping = Mapping({}, relationships)
        
        # Act + Assert
        with pytest.raises(Exception):
            result = generate_dictionaries(mapping)

