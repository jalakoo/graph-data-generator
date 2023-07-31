import io
import pytest
from graph_data_generator import generate


valid_json_config = {
            "nodes": [
                {
                    "id": "n0",
                    "position": {
                        "x": 0.0,
                        "y": 0.0
                    },
                    "caption": "test_node_a",
                    "labels": [],
                    "properties": {
                        "property_key": "property_value",
                    }
                },
                {
                    "id": "n1",
                    "position": {
                        "x": 0.0,
                        "y": 0.0
                    },
                    "caption": "test_node_b",
                    "labels": [],
                    "properties": {
                        "property_key": "property_value",
                    }
                },
            ], 
            "relationships": [
                {
                    "id": "n0",
                    "fromId": "n0",
                    "toId": "n1",
                    "type": "test_relationship",
                    "properties": {
                        "property_key": "property_value",
                    }
                }
            ]
        }

invalid_json_config = {
   "chicken":[],
   "egg" :{}
}

def test_generate_bytes():
   result = generate(valid_json_config)
   assert isinstance(result, (bytes, bytearray))

def test_generate_invalid_format():
   with pytest.raises(Exception):
       generate(invalid_json_config)