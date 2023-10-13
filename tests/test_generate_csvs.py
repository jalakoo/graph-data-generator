import pytest
from graph_data_generator.models.base_mapping import BaseMapping
from graph_data_generator.models.node_mapping import NodeMapping
from graph_data_generator.models.relationship_mapping import RelationshipMapping
from graph_data_generator.models.property_mapping import PropertyMapping
from graph_data_generator.models.mapping import Mapping
from graph_data_generator.generators.ALL_GENERATORS import generators
from graph_data_generator.logic.generate_csvs import generate_csv

# Ugh - worst tests ever

@pytest.fixture()
def sample_count_generator():
    return generators["int"]

@pytest.fixture()
def sample_assignment_generator():
    return generators["exhaustive_random"]

@pytest.fixture()
def sample_generator():
    return generators["string"]

@pytest.fixture()
def empty_base_mapping():
    return BaseMapping.empty()

@pytest.fixture()
def sample_property_mapping(sample_generator):
    return PropertyMapping(
        pid = "p1",
        name = "testProperty",
        generator = sample_generator,
        args = ["testString"]
    )

@pytest.fixture()
def sample_node_mapping(sample_count_generator, sample_property_mapping):
    return NodeMapping(
        nid = "mockNode",
        position = {"x": 0, "y": 0},
        caption = "MockNode",
        labels = [],
        properties = {"mockNodeProperty":sample_property_mapping},
        key_property= sample_property_mapping,
        count_generator = sample_count_generator,
        count_args= [1]
    )

@pytest.fixture()
def sample_relationship_mapping(sample_count_generator, sample_property_mapping, sample_assignment_generator):
    return RelationshipMapping(
        rid = "mockRelationship",
        type = "MOCK",
        from_node = sample_node_mapping,
        to_node = sample_node_mapping,
        properties = {"mockRelationshipProperty": sample_property_mapping},
        count_generator = sample_count_generator,
        count_args= [1],
        assignment_generator= sample_assignment_generator
    )

# @pytest.fixture()
# def sample_mapping(mock_node_mapping, mock_relationship_mapping):
#     return Mapping(
#         nodes={'n1': mock_node_mapping},
#         relationships={'n1': mock_relationship_mapping}
#     )

class TestGenerateCSVs():
    def test_generate_csv_valid(self, sample_node_mapping):
        csv = generate_csv(sample_node_mapping)
        assert isinstance(csv, str)
        assert csv != ""

    def test_generate_csv_empty(self):
        with pytest.raises(Exception):
            csv = generate_csv(None)

    def test_generate_csv_invalid_mapping(self):
        with pytest.raises(Exception):
            csv = generate_csv("invalid")
