import re

def property_contains_pointer_designator(obj: dict) -> bool:
    # Does a dictionary from a properties list contain a special param pointer prefix?
    # TODO: How to properly search for non-escaped @ symbols
    # return any('@' in value and '@@' not in value for value in obj.values() if isinstance(value, str))
    pattern = r'(?<!\\)@'
    # unescaped_at_symbols = re.findall(pattern, s)
    # return bool(unescaped_at_symbols)
    return any(bool(re.findall(pattern,value)) for value in obj.values() if isinstance(value, str))

def preprocess_nodes(json: list[dict]) -> list[dict]:
    # Filter out dicts without required keys
    # Sample dict list
    #   [
    #     {
    #       "id": "n0",
    #       "caption": "Person",
    #       "labels": [],
    #       "properties": {
    #         "name": "string",
    #         "COUNT": "3"
    #       }
    #     }
    #   ]

    filtered_list = [obj for obj in json if 'properties' in obj and 'id' in obj and 'caption' in obj and 'labels' in obj]
    filtered_list.sort(key=lambda x: property_contains_pointer_designator(x['properties'])) 
    return filtered_list

def preprocess_relationships(json: list[dict]) -> list[dict]:
    # Filter out dicts without required keys
    # Sample dict list
    # [
    #     {
    #     "id": "n3",
    #     "fromId": "n4",
    #     "toId": "n1",
    #     "type": "IN",
    #     "properties": {
    #         "Distance": "km"
    #     }
    #     }
    # ]

    filtered_list = [obj for obj in json if 'properties' in obj and 'id' in obj and 'fromId' in obj and 'toId' in obj and 'type'in obj]
    filtered_list.sort(key=lambda x: property_contains_pointer_designator(x['properties'])) 
    return filtered_list