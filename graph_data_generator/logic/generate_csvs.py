from graph_data_generator.models.base_mapping import BaseMapping
from graph_data_generator.logger import ModuleLogger
import io 
import csv

def generate_mapping_csv(elements: [BaseMapping]) -> str:
    for element in elements:
        values : list[dict] = element.generate_values()
        
        # Generate csv from values
        if values is None or values == []:
            ModuleLogger().warning(f'No values generated for element {element}')
            continue

        # Each node dataset will need it's own CSV file
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
    
