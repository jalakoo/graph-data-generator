from graph_data_generator.models.base_mapping import BaseMapping
from graph_data_generator.models.mapping import Mapping
from graph_data_generator.logger import ModuleLogger
import io 
import csv

def generate_csv(element: BaseMapping) -> str:
    """Returns a csv data for generated data from a subclass of a BaseMapping object

    Args:
        element: A subclass of BaseMapping representing a node or relationship mapping

    Returns:
        Stringified csv data
    """    

    if isinstance(element, BaseMapping) == False:
        raise Exception(f'BaseMapping subclass expected. Got {element}')
    
    values : list[dict] = element.generated_values()
    
    # Generate csv from values
    if values is None or values == []:
        ModuleLogger().warning(f'No values generated for element {element}')

    fieldnames = values[0].keys()
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fieldnames)
    writer.writeheader()

    for row in values:
        try:
            writer.writerow(row)
        except Exception as e:
            raise Exception(f'Failed to write row: {row}: ERROR: {e}')
    return buffer.getvalue()
    
def generate_csvs(mapping: Mapping) -> dict[str, str]:
    """Returns a dictionary of filename : csv data string

    Args:
        properties: Mapping object

    Returns:
        A dictionary of {filenames : csv strings}
    """   
    if mapping.did_generate_values() == False:
        mapping.generate_values()
    
    output = {}

    for nodeMapping in mapping.nodes.values():
        values = generate_csv(nodeMapping)
        output[nodeMapping.filename()] = values
    
    for relMapping in mapping.relationships.values():
        values = generate_csv(relMapping)
        output[relMapping.filename()] = values

    return output
