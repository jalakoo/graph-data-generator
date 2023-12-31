# Generated by CodiumAI

from graph_data_generator.models.node_mapping import NodeMapping
from graph_data_generator.models.property_mapping import PropertyMapping
from graph_data_generator.models.generator import Generator

import pytest

class TestNodeMapping:
    # Tests that an empty NodeMapping object is created successfully
    def test_empty_node_mapping_object_created_successfully(self):
        mapping = NodeMapping.empty()
        assert mapping.nid == ""
        assert mapping.position == {"x": 0, "y": 0}
        assert mapping.caption == ""
        assert mapping.labels == []
        assert mapping.properties == {}
        assert mapping.count_generator is None
        assert mapping.count_args == []
        assert mapping.default_count == 1
        assert mapping.key_property is None

    # Tests that a NodeMapping object with all parameters is created successfully
    def test_node_mapping_object_with_all_parameters_created_successfully(self):
        position = {"x": 1, "y": 2}
        labels = ["Label1", "Label2"]
        properties = {"prop1": PropertyMapping.empty(), "prop2": PropertyMapping.empty()}
        count_generator = Generator.empty()
        count_args = [1, 2, 3]
        key_property = PropertyMapping.empty()
        mapping = NodeMapping(
            nid="node1",
            position=position,
            caption="Caption",
            labels=labels,
            properties=properties,
            count_generator=count_generator,
            count_args=count_args,
            key_property=key_property
        )
        assert mapping.nid == "node1"
        assert mapping.position == position
        assert mapping.caption == "Caption"
        assert mapping.labels == labels
        assert mapping.properties == properties
        assert mapping.count_generator == count_generator
        assert mapping.count_args == count_args
        assert mapping.default_count == 1
        assert mapping.key_property == key_property

    # Tests that a NodeMapping object with default values is created successfully
    def test_node_mapping_object_with_default_values_created_successfully(self):
        mapping = NodeMapping.empty()
        assert mapping.nid == ""
        assert mapping.position == {"x": 0, "y": 0}
        assert mapping.caption == ""
        assert mapping.labels == []
        assert mapping.properties == {}
        assert mapping.count_generator is None
        assert mapping.count_args == []
        assert mapping.default_count == 1
        assert mapping.key_property is None

    # Tests that the generate_values() method generates values correctly with a count generator
    def test_generate_values_method_with_count_generator(self):
        position = {"x": 1, "y": 2}
        labels = ["Label1", "Label2"]
        properties = {"prop1": PropertyMapping.empty(), "prop2": PropertyMapping.empty()}
        count_generator = Generator.empty()
        count_args = [1, 2, 3]
        key_property = PropertyMapping.empty()
        mapping = NodeMapping(
            nid="node1",
            position=position,
            caption="Caption",
            labels=labels,
            properties=properties,
            count_generator=count_generator,
            count_args=count_args,
            key_property=key_property
        )
        # TODO: generate values and test


    # Tests that the generate_values() method generates values correctly with no count generator or default count
    def test_generate_values_method_with_no_count_generator_or_default_count(self):
        position = {"x": 1, "y": 2}
        labels = ["Label1", "Label2"]
        properties = {"prop1": PropertyMapping.empty(), "prop2": PropertyMapping.empty()}
        count_generator = None
        count_args = []
        key_property = PropertyMapping.empty()
        mapping = NodeMapping(
            nid="node1",
            position=position,
            caption="Caption",
            labels=labels,
            properties=properties,
            count_generator=count_generator,
            count_args=count_args,
            key_property=key_property
        )
  
        # TODO: Generate values and check actual output


