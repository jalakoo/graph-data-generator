import pytest

from graph_data_generator.models.generator import generators_from_json
from graph_data_generator.config import generators_json

@pytest.fixture(scope="module")
def sample_generators():
    return generators_from_json(generators_json)