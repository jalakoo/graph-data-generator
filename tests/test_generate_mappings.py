import pytest
from graph_data_generator.logic import generate_mappings
from graph_data_generator.models.node_mapping import NodeMapping

@pytest.fixture
def sample_node():
    return {
        "id": "n1",
        "position": {
                "x": -198.13187072311678,
                "y": -720.3662225379142
        },
        "caption": "Person",
        "labels": [],
            "properties": {
                "name": '{"first_name":[]}'
            }
    }

@pytest.fixture
def sample_node_missing_position():
    return {
        "id": "n1",
        "caption": "Person",
        "labels": [],
            "properties": {
                "name": '{"first_name":[]}'
            }
    }

class TestPropertyMappings:
    def test_propertymappings_for_raw_properties(self, sample_node, sample_generators):
        mappings = generate_mappings.propertymappings_for_raw_properties(
            sample_node["properties"], 
            sample_generators
        )
        # _uid property always added
        assert len(mappings) == 2
        assert mappings["_uid"].generator.name == "UUID"
        assert mappings["name"].generator.name == "First Name"

class TestNodeMappings:
    def test_nodemappings_from(self, sample_node, sample_generators):
        nodes = generate_mappings.node_mappings_from([sample_node], sample_generators)

        assert len(nodes) == 1
        assert isinstance(list(nodes.values())[0], NodeMapping)

    def test_node_mappings_from_invalid(self):
        with pytest.raises(Exception):
            nodes = generate_mappings.node_mappings_from("invalid", {})

    def test_node_mappings_from_missing_position(self, sample_node_missing_position, sample_generators):
        nodes = generate_mappings.node_mappings_from([sample_node_missing_position], sample_generators)
        
        assert len(nodes) == 0


from graph_data_generator.logic.generate_mappings import relationshipmappings_from

class TestRelationshipMappings:
    # Tests that valid input with all required fields is processed correctly
    def test_valid_input(self, sample_generators):
        relationship_dicts = [
            {
                "id": "r0",
                "fromId": "n0",
                "toId": "n1",
                "type": "KNOWS",
                "properties": {
                    "COUNT": "{\"int\": [5]}"
                },
                "style": {}
            }
        ]
        nodes = {
            "n0": NodeMapping.empty(),
            "n1": NodeMapping.empty()
        }
        result = relationshipmappings_from(relationship_dicts, nodes, sample_generators)
        assert len(result) == 1
        assert "r0" in result
        assert result["r0"].rid == "r0"
        assert result["r0"].type == "KNOWS"
        assert result["r0"].from_node == nodes["n0"]
        assert result["r0"].to_node == nodes["n1"]
        assert result["r0"].count_generator is not None
        assert result["r0"].count_args == [5]
        # NOTE: _uid is always added. COUNT is stripped and reservered for calculating number of relationships to generate (not retained as a data property to pass along)
        assert len(result["r0"].properties) == 1
        assert result["r0"].assignment_generator is not None
        assert result["r0"].assignment_args == []


from graph_data_generator.logic.generate_mappings import mapping_from_json

class TestMappingFromJson:
    def test_happy_path(self, sample_generators):
        json_config = {
            "nodes": [
                {
                    "id": "n1",
                    "position": {
                        "x": 284.5,
                        "y": -204
                    },
                    "caption": "Company",
                    "labels": [],
                    "properties": {
                        "name": "{\"company_name\":[]}",
                        "uuid": "{\"uuid\":[8]}}",
                        "{count}": "{\"int\":[1]}",
                        "{key}": "uuid"
                    },
                    "style": {}
                }
            ],
            "relationships": []
        }
        mapping = mapping_from_json(json_config, sample_generators)
        assert mapping is not None
        assert len(mapping.nodes) == 1, f'Expected 1 node, got {len(mapping.nodes)}'
        assert len(mapping.relationships) == 0, f'Expected 0 relationship, got {len(mapping.relationships)}'

        node = mapping.nodes['n1']
        assert node.nid == 'n1', f'Expected node nid "n1" from: {node.nid}'

    def test_no_nodes(self, sample_generators):
        json_config = {
            "relationships": []
        }
        with pytest.raises(Exception) as error:
            mapping = mapping_from_json(json_config, sample_generators)

    def test_no_relationships(self, sample_generators):
        json_config = {
            "nodes": []
        }
        mapping = mapping_from_json(json_config, sample_generators)
        assert len(mapping.relationships.items()) == 0, f'Expected 0 relationships, got {len(mapping.relationships.items())}'

    def test_missing_position_key(self, sample_generators):
        json_config = {
            "nodes": [
                {
                    "id": "n1",
                    "caption": "Company",
                    "labels": [],
                    "properties": {
                        "name": "{\"company_name\":[]}",
                        "uuid": "{\"uuid\":[8]}}",
                        "{count}": "{\"int\":[1]}",
                        "{key}": "uuid"
                    },
                    "style": {}
                }
            ],
            "relationships": []
        }
        mapping = mapping_from_json(json_config, sample_generators)
        assert len(mapping.nodes) == 0, f'Expected 0 node, got {len(mapping.nodes)}'
        assert len(mapping.relationships) == 0, f'Expected 0 relationship, got {len(mapping.relationships)}'

    def test_missing_caption_key(self, sample_generators):
        json_config = {
            "nodes": [
                {
                    "id": "n1",
                    "position": {
                        "x": 284.5,
                        "y": -204
                    },
                    "labels": [],
                    "properties": {
                        "name": "{\"company_name\":[]}",
                        "uuid": "{\"uuid\":[8]}}",
                        "{count}": "{\"int\":[1]}",
                        "{key}": "uuid"
                    },
                    "style": {}
                }
            ],
            "relationships": []
        }
        mapping = mapping_from_json(json_config, sample_generators)
        assert len(mapping.nodes) == 0, f'Expected 0 node, got {len(mapping.nodes)}'
        assert len(mapping.relationships) == 0, f'Expected 0 relationship, got {len(mapping.relationships)}'

    def test_invalid_json(self, sample_generators):
        json_config = "invalid_json"
        with pytest.raises(Exception) as error:
            mapping = mapping_from_json(json_config, sample_generators)