import pytest

from graph_data_generator.generators.ALL_GENERATORS import generators
from graph_data_generator.logic.generate_csvs import generate_csv

class TestGenerateCSVs():
    def test_generate_csv_valid_node(self, sample_node_mapping):
        csv = generate_csv(sample_node_mapping)
        assert isinstance(csv, str)
        assert csv != ""

    def test_generate_csv_valid_relationship(self, sample_relationship_mapping):
        csv = generate_csv(sample_relationship_mapping)
        assert isinstance(csv, str)
        assert csv != ""

    def test_generate_csv_empty(self):
        with pytest.raises(Exception):
            csv = generate_csv(None)

    def test_generate_csv_invalid_mapping(self):
        with pytest.raises(Exception):
            csv = generate_csv("invalid")
