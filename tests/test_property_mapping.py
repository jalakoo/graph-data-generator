
# Generated by CodiumAI
from graph_data_generator.models.generator import Generator
from graph_data_generator.models.property_mapping import PropertyMapping

import pytest

class TestPropertyMapping:
    # Tests that a PropertyMapping object can be created with all parameters
    def test_create_property_mapping_with_all_parameters(self):
        generator = Generator.empty()
        args = [1, 2, 3]
        mapping = PropertyMapping(
            pid='prop1',
            name='Property 1',
            generator=generator,
            args=args
        )
        assert mapping.pid == 'prop1'
        assert mapping.name == 'Property 1'
        assert mapping.generator == generator
        assert mapping.args == args

    # Tests that a PropertyMapping object can be created with default values
    def test_create_property_mapping_with_default_values(self):
        mapping = PropertyMapping.empty()
        assert mapping.pid is None
        assert mapping.name is None
        assert mapping.generator is None
        assert mapping.args is None

    # Tests that an exception is raised when generating a value with no generator
    def test_generate_value_with_no_generator(self):
        mapping = PropertyMapping.empty()
        with pytest.raises(Exception) as e:
            mapping.generate_values()[0]
        assert str(e.value) == 'Property Mapping is missing a generator property. Property name: None'

    # Tests that an exception is raised when generating a value with args that are not a list
    def test_generate_value_with_args_not_list(self):
        generator = Generator.empty()
        mapping = PropertyMapping(
            pid='prop1',
            name='Property 1',
            generator=generator,
            args='invalid'
        )
        with pytest.raises(Exception) as e:
            mapping.generate_value()[0]
        assert str(e.value) == 'Property Mapping Args is not a list. Property name: Property 1'


    # Tests that the ready_to_generate method returns True when all required properties are set
    def test_ready_to_generate(self):
        mapping = PropertyMapping(
            pid='prop1',
            name='Property 1',
            generator=None
        )
        assert mapping.ready_to_generate() == False

        mapping.generator = Generator.empty()
        assert mapping.ready_to_generate() == True