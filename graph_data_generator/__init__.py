
import io
import json
import zipfile

from graph_data_generator.logic.generate_zip import generate_zip
from graph_data_generator.logic.generate_csvs import generate_csvs, generate_csvs_from_dictionaries
from graph_data_generator.logic.generate_dictionaries import generate_dictionaries
from graph_data_generator.logic.generate_mappings import mapping_from_json
from graph_data_generator.logic.generate_data_import import generate_data_import_json
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
        dicts = generate_dictionaries(mapping)
        nodes = len(dicts["nodes"])
        rels = len(dicts["relationships"])
        ModuleLogger().info(f'Generated {nodes} nodes and {rels} records')
    except Exception as e:
        ModuleLogger().error(f'Error generating data as dictionaries: {e}')
        raise e

    # Generate csv files from generated data
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