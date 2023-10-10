# New stateless process for creating Node data

from graph_data_generator.logic.generate_utils import preprocess



def nodes_csvs_from(json: list[dict]) -> str:
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
    # Purge objects 
    cleaned_sorted_raw_nodes = preprocess(json)