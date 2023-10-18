
from graph_data_generator.models.mapping import Mapping
from graph_data_generator.models.base_mapping import BaseMapping
from graph_data_generator.logger import ModuleLogger


def generate_dictionaries(mapping: Mapping):

    # TODO: Add an arg that identifies calling node/relationship to prevent circular references
    def data_callback(tid: str, calling_id:str = None)-> any:
        nonlocal mapping

        # Split dot path into a list of string keys
        # Should be a node or relationship name.property
        path = tid.split(".")

        if len(path) != 2:
            # Invalid path designation. 1 key is not enought, more than 2 is an invalid path
            return None

        # Check nodes first for a match
        for nodeMapping in mapping.nodes.values():
            if nodeMapping.caption == path[0]:
                # Found a match.
                # TODO: Could potentially get stuck in a loop if 2 reference generators reference each other
                data = nodeMapping.generated_data(data_callback)

        # Get target node or relationship

    output = {}

    for nodeMapping in mapping.nodes.values():
        values : list[dict] = nodeMapping.generated_values()
        key = f'{nodeMapping.caption}'
        output['nodes'][key] = values
    
    for relMapping in mapping.relationships.values():
        values : list[dict] = relMapping.generated_values()
        key = f'{relMapping.type}'
        output['relationships'][key] = values

    return output