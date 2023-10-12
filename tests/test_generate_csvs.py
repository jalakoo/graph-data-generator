import pytest
from graph_data_generator.models.base_mapping import BaseMapping
from graph_data_generator.models.node_mapping import NodeMapping
from graph_data_generator.models.relationship_mapping import RelationshipMapping
from graph_data_generator.models.property_mapping import PropertyMapping
from graph_data_generator.logic.generate_csvs import generate_mapping_csv

# @pytest.fixture()
# def mock_empty_base_mapping():
#     return BaseMapping.empty()

# @pytest.fixture()
# def mock_property_mapping(sample_generator):
#     return PropertyMapping(
#         pid = "testProperty",
#         generator_name = "testGnerator",
#         generator = sample_generator,
#         generator_args = ["testString"]
#     )

# @pytest.fixture()
# def mock_node_mapping(mock_count_generator, mock_property_mapping):
#     return NodeMapping(
#         nid = "mockNode",
#         position = {"x": 0, "y": 0},
#         caption = "MockNode",
#         labels = [],
#         properties = {"mockNodeProperty":mock_property_mapping},
#         count_generator = mock_count_generator,
#         count_args= [1]
#     )

# @pytest.fixture()
# def mock_relationship_mapping(mock_count_generator, mock_property_mapping):
#     return RelationshipMapping(
#         rid = "mockRelationship",
#         type = "MOCK",
#         from_node = mock_node_mapping,
#         to_node = mock_node_mapping,
#         properties = {"mockRelationshipProperty": mock_property_mapping},
#         count_generator = mock_count_generator,
#         count_args= [1]
#     )

class TestGenerateCSVs():
    def test_empty_mapping(self):
        mapping = [NodeMapping.empty()]
        result = generate_mapping_csv(mapping)
        assert result == '\r\n\r\n', f'result received: {result}'

    def test_node_mapping(self, mock_node_mapping):
        mapping = [mock_node_mapping]
        result = generate_mapping_csv(mapping)
        assert result == '\r\n\r\n', f'result received: {result}'
