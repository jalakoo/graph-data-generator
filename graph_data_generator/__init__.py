
import io
import json
import zipfile

from graph_data_generator.logic.generate_zip import generate_zip
from graph_data_generator.logic.generate_mapping import mapping_from_json
from graph_data_generator.logic.generate_nodes import generate_nodes
from graph_data_generator.logic.generate_relationships import generate_relationships
from graph_data_generator.logic.generate_utils import convert_dicts_to_csv

# Here also to expose for external use
from graph_data_generator.models.generator import Generator, generators_from_json
from graph_data_generator.models.generator_arg import GeneratorArg
from graph_data_generator.models.generator_type import GeneratorType
from graph_data_generator.generators.ALL_GENERATORS import generators
from graph_data_generator.logger import ModuleLogger

VERSION = "0.3.0"

logger = ModuleLogger()
logger.is_enabled = False
  
def enable_logger():
    logger = ModuleLogger()
    logger.is_enabled = True
    logger.info("Graph-Data-Generator logging enabled")

# TODO: labels are stripped in return - add back in or add to key somehow
def generate_dicts(input: str|dict) -> dict:
    """Generates a dictionary of nodes and relationships records.

    Args:
        input: Stringified JSON object or dictionary of configuration information
        enable_logging: Whether to pass logging info to shared default Python logging module

    Returns:
        A dictionary with generated nodes and relationship records
    """
    
    # Convert json string to dict
    if isinstance(input, str):
        try:
            input = json.loads(input)
        except Exception as e:
            message = f'{e}. Checking validity of input configuration file'
            raise Exception(message)
        
    # Confirm we have a dict
    if isinstance(input, dict) == False:
        message = f'Expecting a string or dictionary as an input file. Instead got {input}'
        raise Exception(message)

    # Check dict has minimum data
    nodes = input.get('nodes', None)
    if nodes is None:
        message = f'"nodes" key required from input file: {input}'
        raise Exception(message)
    
    # Generate node records
    node_dicts = generate_nodes(nodes)
    output = {'nodes': node_dicts}

    # Optionally generate relationship records
    rels = input.get('relationships', None)
    if rels is not None:
        rel_dicts = generate_relationships(rels, node_dicts)
        output['relationships'] = rel_dicts
    
    return output

def generate_csvs(input: str | dict) -> list[(str, list[str])]:
    """Generates a list of tuples containing (filename, csv string).

    Args:
        json_source: Source stringified JSON representation of a graph data model
        enable_logging: Enables logging to console

    Returns:
        A list of tuples containing (filename, stringified csv)
    """
    
    # Generate dictionary of records first
    all_records = generate_dicts(input)
    all_nodes = all_records.get('nodes', None)
    all_relationships = all_records.get('relationships', None)
            
    if all_nodes is None:
        raise Exception(f'No nodes generated for input: {input}')

    ModuleLogger().debug(f'records generated for nodes: {all_nodes.keys()}')
    ModuleLogger().debug(f'records generated for relationships: {all_relationships.keys()}')

    output = []
    for nid, nodes in all_nodes.items():
        caption = nodes[0]['_labels'][0]
        output.append(convert_dicts_to_csv(f'{caption}_{nid}.csv', nodes))

    for rid, rels in all_relationships.items():
        type = rels[0]['_type']
        output.append(convert_dicts_to_csv(f'{type}_{rid}.csv', rels))

    return output

    
def generate_zip(
    input: str | dict,
    filename: str = "mock_data"
) -> io.BytesIO:
    
    """Generates a zip file containing a series of .csv files and an optional .log file.

    Args:
        input: Source stringified JSON representation of a graph data model
        filename: Optional filename for .zip file. Defaults to "mock_data.zip"

    Returns:
        A zip file of .csvs and a .json data-importer compatible file
    """
    
    in_memory_data = io.BytesIO()
    in_memory_zip = zipfile.ZipFile(
        in_memory_data, "w", zipfile.ZIP_DEFLATED, False)
    in_memory_zip.debug = 3 

    csvs = generate_csvs(input)
    ModuleLogger().debug(f'csvs files generated: {len(csvs)}')

    for filename, records in csvs:
        in_memory_zip.writestr(filename, records)

    # TODO: Add in data-importer .json file

    return in_memory_data

def generate(
    json_source : any,
    output_format : str = 'bytes',
    enable_logging : bool = False
) -> io.BytesIO:
    if enable_logging:
        enable_logger()
    return generate_zip(json_source)

# DEPRECATING this original method
# TODO update to call the generate_zip method instead
# def generate(
#     json_source : any,
#     output_format : str = 'bytes',
#     enable_logging : bool = False
# ) -> io.BytesIO:
#     """
#     Generates a zip file of data based on the provided JSON object.

#     Args:
#         json_source (any): A stringified JSON or dict object containing the mapping of nodes and relationships to generate.
#         output_format (str, optional): The format of the output. Defaults to 'bytes' which can be added directly to a flask make_response() call. Otther options are 'string'.
#     """
#     # Validate json

#     # jsonschema package did not work with pytest
#     # from jsonschema import validate
#     # try:
#     #     validate(instance=json_object, schema=arrows_json_schema)
#     # except jsonschema.exceptions.ValidationError as e:
#     #     raise Exception("Invalid JSON object provided.")
#     # except jsonschema.exceptions.SchemaError as e:
#     #     raise Exception("Base JSON schema invalid. Contact developer")
#     # except Exception as e:
#     #     raise Exception(f"Unknown error validating JSON object. {e} Contact developer")

#     # TODO: Replace with a enum for output_format or arg for a logger object
#     if enable_logging is True:
#         logger = ModuleLogger()
#         logger.is_enabled = True
#         logger.info(f'Logging enabled')

#     # If json_object is a string, load and convert into a dict object
#     if isinstance(json_source, str) is True:
#         try:
#             json_source = json.loads(json_source)
#         except Exception as e:
#             raise Exception(f'json_source string not a valid JSON format: {e}')
    
#     # TODO: Check the dict key-value format matches what we're expecting
    
    
#     # Create mapping file
#     mapping, error_msg = mapping_from_json(
#         json_source, 
#         generators
#     )
#     if mapping is None:
#         raise Exception(error_msg)
#     if mapping.is_empty():
#         raise Exception(f"No nodes or relationships generated. Check input file")

#     # Generate output and return as bytes of a zip file
#     bytes, error_msg = generate_zip(
#         mapping
#     )
#     if bytes is None:
#         raise Exception(error_msg)
#     if error_msg is not None:
#         ModuleLogger().error(error_msg)

#     if output_format == 'string':
#         data_bytes = bytes.getvalue()
#         result = data_bytes.decode('utf-8')
#     else:
#         bytes.seek(0)
#         result = bytes.getvalue()

#     return result