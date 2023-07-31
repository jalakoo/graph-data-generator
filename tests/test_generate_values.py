import pytest
from graph_data_generator.logic.generate_values import actual_generator_for_raw_property

class TestActualGenerator:
    def test_valid_json_single_key_value(self, sample_generators):
        property_value = '{"company_name":[]}'
        generator, args = actual_generator_for_raw_property(property_value, sample_generators)
        assert generator is not None
        assert args == []