import pytest

from graph_data_generator.models.mapping import Mapping
from graph_data_generator.models.node_mapping import NodeMapping
from graph_data_generator.models.relationship_mapping import RelationshipMapping
from graph_data_generator import generate_zip

class TestGenerateZip:

    # Tests that generate_zip function generates a zip file with empty nodes and relationships data
    def test_generate_zip_with_empty_nodes_and_relationships_data(self):
        mapping = Mapping()

        result, error = generate_zip(mapping)

        assert result is None
        assert error is not None