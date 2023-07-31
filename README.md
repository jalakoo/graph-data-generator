# Graph Data Generator
Package for generating interconnected mock data from .json graph data models.

## JSON Spec
Is the same specification used by the [arrows.app](https://arrows.app) which is a GUI for generating graph data models. The .json spec has 2 required keys, `nodes` and `relationships`:
```
{
    "nodes":[],
    "relationships: []
}
```
Each must contain an array (or list) of dictionary objects with formats dependent on the key type:

**Nodes** must have the following property keys and value types:
```
{
    "id": str,
    "position": {
    "x": float,
    "y": float
    },
    "caption": string,
    "labels": list[str],
    "properties": dict[str:str],
    "style": {}
}

Example:
{
    "id": "n0",
    "position": {
    "x": -306.93969052033395,
    "y": 271.3634778613202
    },
    "caption": "Person",
    "labels": [],
    "properties": {
        "email": "test@email.com",
        "salary_usd": "3000.00",
        "first_name": "Jane",
        "last_name": "Doe"
    },
    "style": {}
}
```

**Relationships** must have the following keys and value types:
```
    {
      "id": str,
      "type": str,
      "style": dict,
      "properties": dict[str,str],
      "fromId": str,
      "toId": str
    }

Example:
    {
      "id": "n0",
      "type": "WORKS_AT",
      "style": {},
      "properties": {
        "start_epoch":"1672904355",
        "end_epoch":"1688542755"
      },
      "fromId": "n0",
      "toId": "n1"
    }
```

## Installation
`pip install graph-data-generator`

To use in a project:
`import graph_data_generator as gdg`

To generate a .zip file and return as bytes, pass a json object as an arg:
`bytes_file = gdg.generate_zip(json_object)`

## Package Usage
Build locally:
`poetry build`

To use in another poetry project:
`import graph_data_generator as gdg`

