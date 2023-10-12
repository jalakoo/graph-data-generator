# New stateless process for creating Node data

from graph_data_generator.logic.generate_utils import preprocess_nodes


def nodes_dicts_from(json: list[dict]) -> dict:

    #   Sample input
    #   [
    #     {
    #       "id": "n0",
    #       "position": {
    #         "x": -154.38476542608726,
    #         "y": 210.7077534174155
    #       },
    #       "caption": "Person",
    #       "labels": [],
    #       "properties": {
    #         "name": "string",
    #         "COUNT": "3"
    #       },
    #       "style": {}
    #     }
    #   ]

   # Purge improperly formatted objects and sort nodes using parameterized properties last
    cleaned_sorted_raw_nodes = preprocess_nodes(json)

    # Using a dict as we generate nodes
    nodes_dicts = {}
