
import io
import json
import logging

from graph_data_generator.logic.generate_zip import generate_zip
from graph_data_generator.logic.generate_mapping import mapping_from_json
from graph_data_generator.models.generator import generators_from_json, Generator
from graph_data_generator.models.generator_arg import GeneratorArg
from graph_data_generator.models.generator_type import GeneratorType
from graph_data_generator.config import generators_json

VERSION = "0.1.0"

def setup_logging():
    logger = logging.getLogger(__name__)
    FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(format=FORMAT)
    logger.setLevel(logging.DEBUG)

generators = generators_from_json(generators_json)

def generate(
    json_source : any,
    output_format : str = 'bytes',
    enable_logging : bool = False
) -> io.BytesIO:
    """
    Generates a zip file of data based on the provided JSON object.

    Args:
        json_source (any): A stringified JSON or dict object containing the mapping of nodes and relationships to generate.
        output_format (str, optional): The format of the output. Defaults to 'bytes' which can be added directly to a flask make_response() call. Otther options are 'string'.
    """
    # Validate json

    # jsonschema package did not work with pytest
    # from jsonschema import validate
    # try:
    #     validate(instance=json_object, schema=arrows_json_schema)
    # except jsonschema.exceptions.ValidationError as e:
    #     raise Exception("Invalid JSON object provided.")
    # except jsonschema.exceptions.SchemaError as e:
    #     raise Exception("Base JSON schema invalid. Contact developer")
    # except Exception as e:
    #     raise Exception(f"Unknown error validating JSON object. {e} Contact developer")

    # TODO: Replace with a enum for output_format or arg for a logger object
    if enable_logging is True:
        setup_logging()

    # If json_object is a string, load and convert into a dict object
    if isinstance(json_source, str) is True:
        try:
            json_source = json.loads(json_source)
        except Exception as e:
            raise Exception(f'json_source string not a valid JSON format: {e}')
    
    # TODO: Check the dict key-value format matches what we're expecting
    
    # Create mapping file
    mapping, error_msg = mapping_from_json(
        json_source, 
        generators
    )
    if mapping is None:
        raise Exception(error_msg)
    if mapping.is_empty():
        raise Exception(f"No nodes or relationships generated. Check input file")

    # Generate output and return as bytes of a zip file
    bytes, error_msg = generate_zip(
        mapping
    )
    if bytes is None:
        raise Exception(error_msg)

    if output_format == 'string':
        data_bytes = bytes.getvalue()
        result = data_bytes.decode('utf-8')
    else:
        bytes.seek(0)
        result = bytes.getvalue()

    return result