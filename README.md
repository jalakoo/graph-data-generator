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

**Properties** of either nodes or relationships can be used to further define the type of data generated.

The following keywords are reserved:
| Keyword  |  Description  |  Example Value |
|----------|---------------|----------|
| COUNT | Specifies the number of this node or relationship type to generate | 3 |

***COUNT***
The COUNT keyword can take the following optional value formats:

| Type | Example  |  Output Description |
|------| ---------|---------------|
| Int |  2 | Would generate two of the nodes / relationships this was a property for |
| Range | 0-10 | Would randomly generate a number between 0 (No node or relationship) and 10 |
| Random from List | [3,5,6] | Would randomly generate three, five, or six nodes / relationships |

All other node / relationship property keys will be passed along to generated records. Values will be passed along as strings unless they match 1 of several formats:

***GENERATOR SPECIFICATIONS***
Generator specifications are stringified JSON dictionaries that have only a single key that takes a single list as an arg, looking like:
```
{ "generator_name": [] }
```
The `generator_name` must be one of the existing unique generator names included in the package's `generators/` folder. If this format is detected but a matching generator can not be found, then the entire string will be written as the property value.

The list value is the arguments list for the generator. The expected value types and number are dependent on the specified generator. The `generators/ALL_GENERATORS.py` file contains a `generators_json` file that list all the available generators, their type, and what arguments (if any) each expect.

***CONVENIENCE KEYWORDS***
The following keywords, regardless of casing, will map to pre-built generators as shorthands:
| Keyword | Output Description  |
| ------ | ---------|
| bool | Random True or False value |
| boolean | (Same as above)
| date | Random date between 1970-01-01 and today |
| datetime | (Same as above) |
| int | Random integer between 1 and 100 |
| integer | (Same as above) |
| float | Random two decimal float value between 1.00 and 100.00 |
| string | Between 1 and 3 random lorem words |


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

