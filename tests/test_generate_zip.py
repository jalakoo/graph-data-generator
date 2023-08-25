import pytest

from graph_data_generator.models.mapping import Mapping
from graph_data_generator.models.node_mapping import NodeMapping
from graph_data_generator.models.relationship_mapping import RelationshipMapping
from graph_data_generator.logic.generate_zip import generate_csvs, generate_zip
from graph_data_generator.models.generator import Generator, GeneratorType

class mockIntGenerator:
    def generate(args: list[any]):
        value = args[0]
        return value


class TestGenerateZip:

    # Tests that generate_zip function generates a zip file with empty nodes and relationships data
    def test_generate_zip_with_empty_nodes_and_relationships_data(self):
        mapping = Mapping()

        result, error = generate_zip(mapping)

        assert result is None
        assert error is not None

def random_assignment_gen(
    args: list[any]
    ) -> tuple[dict, list[dict]]:
    # Duplicate of exhaustive random assignment generator
    from random import shuffle

    node_values = args
    shuffle(node_values)
    choice = node_values.pop(0)
    return (choice, node_values)



def count_gen():
    return Generator(
        "testCountGenerator",
        type= GeneratorType.INT,
        description="A test count generator",
        code = mockIntGenerator,
        args=[],
        tags=["test"]
    )

@pytest.fixture
def sample_simple_mapping():

    node1 = NodeMapping(
        nid="testNode1",
        position={
            "x": 0,
            "y": 0
        },
        caption = "Test Node 1",
        labels= [],
        properties={},
        count_generator=mockIntGenerator,
        count_args=[1],
        key_property=None
    )
    node2 = NodeMapping(
        nid="testNode2",
        position={
            "x": 0,
            "y": 0
        },
        caption = "Test Node 2",
        labels= [],
        properties={},
        count_generator=mockIntGenerator,
        count_args=[1],
        key_property=None
    )
    rel1 = RelationshipMapping(
        rid="testRelationship",
        type="TEST_REL",
        from_node=node1,
        to_node=node2,
        properties={

        },
        count_generator=count_gen,
        count_args=[1],
        assignment_generator=random_assignment_gen(args=[node1, node2])
    )
    return Mapping(
        nodes={
            "node1":node1,
            "node2":node2
        },
        relationships={
            "rel1":rel1
        }
    )

class TestGenerateCSVs:



    def test_empty_nodes_mapping(self):
        result = generate_csvs(Mapping.empty().nodes)
        assert result is None

    def test_empty_relationships_mapping(self):
        result = generate_csvs(Mapping.empty().relationships)
        assert result is None

    def test_simple_mapping(self, sample_simple_mapping):
        nodes = generate_csvs(sample_simple_mapping.nodes.items())
        assert len(nodes) == 2, f"Expected 2 node CSVs, got {len(nodes)}. nodes output: {nodes}"

    