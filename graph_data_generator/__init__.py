
import io
import json
import zipfile

from graph_data_generator.logic.generate_zip import generate_zip
from graph_data_generator.logic.generate_csvs import generate_csvs
from graph_data_generator.logic.generate_mappings import mapping_from_json
from graph_data_generator.logic.generate_nodes import generate_nodes
from graph_data_generator.logic.generate_relationships import generate_relationships
from graph_data_generator.logic.generate_data_import import generate_data_import_json
from graph_data_generator.logic.generate_utils import convert_dicts_to_csv
from graph_data_generator.models.mapping import Mapping

# Here also to expose for external use
from graph_data_generator.models.generator import Generator, generators_from_json
from graph_data_generator.models.generator_arg import GeneratorArg
from graph_data_generator.models.generator_type import GeneratorType
from graph_data_generator.generators.ALL_GENERATORS import generators
from graph_data_generator.logger import ModuleLogger

VERSION = "0.3.0"

logger = ModuleLogger()
logger.is_enabled = False
  
def start_logging():
    logger = ModuleLogger()
    logger.is_enabled = True
    logger.info("Graph-Data-Generator logging enabled")

def stop_logging():
    ModuleLogger().info(f'Discontinuing logging')
    ModuleLogger().is_enabled = False

# def generate_data_importer_only(input: str|dict) -> str:
#     """Generates a .json file for use by Data Importer w/ no accompanying .csv data.

#     Args:
#         input: Stringified JSON object or dictionary of configuration information

#     Returns:
#         A stringified .json file
#     """
#     raise Exception('unimplemented')

def generate_dicts_only(input: str|dict) -> dict:
    """Generates a dictionary of nodes and relationships records. Uses a non-mapping process to directly generate mock data.

    Args:
        input: Stringified JSON object or dictionary of configuration information

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

def generate_csvs_only(input: str | dict) -> list[(str, list[str])]:
    """Generates a list of tuples containing (filename, csv string). Uses a non-mapping process to directly generate mock data.

    Args:
        json_source: Source stringified JSON representation of a graph data model

    Returns:
        A list of tuples containing (filename, stringified csv)
    """
    
    # Generate dictionary of records first
    all_records = generate_dicts_only(input)
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

def generate_mapping(input: str|dict)-> Mapping:

    # If json_object is a string, load and convert into a dict object
    if isinstance(input, str) is True:
        try:
            input = json.loads(input)
        except Exception as e:
            raise Exception(f'input string not a valid JSON format: {e}')    
    
    # Convert configuration to an intermediary mapping file
    return mapping_from_json(
        input, 
        generators
    )

def generate(
    json_source : str | dict,
    output_format : str = 'bytes',
    enable_logging : bool = False
) -> io.BytesIO:
    """
    Generates a zip file of data based on the provided JSON object.

    Args:
        json_source (any): A stringified JSON or dict object containing the mapping of nodes and relationships to generate.
        output_format (str, optional): The format of the output. Defaults to 'bytes' which can be added directly to a flask make_response() call. Otther options are 'string'.
    
    Returns:
        An io.BytesIO file
    """

    if enable_logging:
        start_logging()

    # Convert config to a mapping file
    mapping = generate_mapping(json_source)

    # Generate data
    try:
        csvs = generate_csvs(mapping)
        ModuleLogger().info(f'Generated {len(csvs)} csv files')
    except Exception as e:
        ModuleLogger().error(f'Error generating csvs: {e}')
        raise e

    # Generate data import json
    try:
        json = generate_data_import_json(mapping)
        ModuleLogger().info(f'Generated data import json')
    except Exception as e:
        ModuleLogger().error(f'Error generating data import json: {e}')
        raise e

    # Add data import json with csvs for zip file
    csvs["neo4j_importer_model.json"] = json

    try:
        # Package into zip file
        bytes = generate_zip(csvs)
        ModuleLogger().info(f'Generated zip file')
    except Exception as e:
        ModuleLogger().error(f'Error generating zip file: {e}')
        raise e

    # Return based on file output type
    if output_format == 'string':
        data_bytes = bytes.getvalue()
        result = data_bytes.decode('utf-8')
    else:
        bytes.seek(0)
        result = bytes.getvalue()

    return result