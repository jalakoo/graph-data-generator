from graph_data_generator.models.mapping import Mapping
import logging
import io 
import csv
import json
import zipfile
from graph_data_generator.models.data_import import DataImporterJson
from graph_data_generator.models.generator import Generator
from graph_data_generator.models.base_mapping import BaseMapping


def generate_csvs(mappings: dict[str, BaseMapping]) -> str:
    for m_id, mapping in mappings:
        # Generate values from mappings
        values : list[dict] = mapping.generate_values()
        
        # Generate csv from values
        if values is None or values == []:
            logging.warning(f'No values generated for {mapping}')
            continue
    
        # Each node dataset will need it's own CSV file
        fieldnames = values[0].keys()
        m_buffer = io.StringIO()
        m_writer = csv.DictWriter(m_buffer, fieldnames=fieldnames)
        m_writer.writeheader()

        for row in values:
            try:
                m_writer.writerow(row)
            except Exception as e:
                return None, f'Mapping generation failed for {m_id}: ERROR: {e}'
        return m_buffer.getvalue()

def generate_zip(
        mapping: Mapping,
        )->tuple[io.BytesIO, str]:

    # Simple preprocess check
    if len(mapping.nodes) == 0:
        return None, f'No nodes to process from mapping: {mapping}'
    if len(mapping.relationships) == 0:
        return None, f'No relationships found from mapping: {mapping}.'

    # Prep zip file to write data to
    in_memory_data = io.BytesIO()
    in_memory_zip = zipfile.ZipFile(
        in_memory_data, "w", zipfile.ZIP_DEFLATED, False)
    in_memory_zip.debug = 3 

    # Process nodes
    for nid, node in mapping.nodes.items():
        # Generate values from mappings
        values : list[dict] = node.generate_values()
        
        # Generate csv from values
        if values is None or values == []:
            logging.warning(f'No values generated for node {node.caption}')
            continue
    
        # Each node dataset will need it's own CSV file
        fieldnames = values[0].keys()
        nodes_buffer = io.StringIO()
        nodes_writer = csv.DictWriter(nodes_buffer, fieldnames=fieldnames)
        nodes_writer.writeheader()

        for row in values:
            try:
                nodes_writer.writerow(row)
            except Exception as e:
                return None, f'Node {node.caption} generation failed: {e}'
        in_memory_zip.writestr(f"{node.filename()}.csv", nodes_buffer.getvalue())
    

    for rid, rel in mapping.relationships.items():
        # Generate values from mappings
        values : list[dict] = rel.generate_values()

        # Generate csv from values
        if values is None or values == []:
            logging.warning(f'No values generated for relationship {rel.type}')
            continue
        fieldnames = values[0].keys()
        rels_buffer = io.StringIO()
        writer = csv.DictWriter(rels_buffer, fieldnames=fieldnames)
        writer.writeheader()
        for row in values:
            writer.writerow(row)
        in_memory_zip.writestr(f"{rel.filename()}.csv", rels_buffer.getvalue())


    # generate data-importer.json
    dij = DataImporterJson()
    nodes = mapping.nodes
    dij.add_nodes(nodes)
    relationships = mapping.relationships
    dij.add_relationships(relationships)
    dij_dict = dij.to_dict()

    try:
        di_dump = json.dumps(dij_dict)
        in_memory_zip.writestr("neo4j_importer_model.json", di_dump)
        
    except Exception as e:
        return None, f'Error adding nodes and relationships for data-importer json: predump: {dij_dict}: \n\nError: {e}'

    return in_memory_data, None