from typing import List, Dict, Any
# Builds mapping file from specially formatted arrows.app JSON file

import json
from graph_data_generator.models.mapping import Mapping
from graph_data_generator.models.node_mapping import NodeMapping
from graph_data_generator.models.relationship_mapping import RelationshipMapping
from graph_data_generator.models.property_mapping import PropertyMapping
from graph_data_generator.models.generator import Generator, GeneratorType
from graph_data_generator.logic.generate_values import generator_for_raw_property, assignment_generator_for
from graph_data_generator.logger import ModuleLogger

def propertymappings_for_raw_properties(
    raw_properties: dict[str, str], 
    generators: dict[str, Generator]
    ) -> dict[str, PropertyMapping]:
    """
    Generates a list of PropertyMapping objects for each raw property in a node or relationship. 

    Raw properties are passed in as a dict with keys as property names and values as generator configs. Example:
    {
        "name": "{\"company_name\":[]}",
        "uuid": "{\"uuid\":[8]}",
        "COUNT": "{\"int\":[1]}"
    }, 
    
    Parameters:
        raw_properties (dict): Raw property definitions from node or relationship
        generators (dict): All available generator objects. [name : Generator] 

    Returns:
        dict: PropertyMapping objects keyed by property name 
    """

    property_mappings = {}
    
    if generators is None or len(generators) == 0:
        raise Exception(f'generate_mapping.py: propertymappings_for_raw_properties: No generators assignment received.')

    raw_keys = raw_properties.keys()

    # Assign uuid if not key property assignment was made
    if "{key}" not in raw_keys and "KEY" not in raw_keys:
        raw_properties["KEY"] = "_uid"
        raw_properties["_uid"] = f'{{"uuid":[]}}'

    # Cycle through all properties and convert to a property mapping
    for key, value in raw_properties.items():

        # Skip any keys with { } (brackets) as these are special legacy cases for defining count/assignment/filter generators
        if key.startswith('{') and key.endswith('}'):
            continue

        # Skip special keywords
        if key == "COUNT" or key == "KEY" or key == "ASSIGNMENT":
            continue

        try:
            generator, args = generator_for_raw_property(value, generators)
            if generator is None:
                # Treat as literal string
                generator, args = generator_for_raw_property(f"{{string:[{value}]}}", generators)
            if generator is None:
                # Targeted and fallback generator could not be found.
                ModuleLogger().warning(f'generate_mapping.py: propertymappings_for_raw_properties: could not find generator for key: {key}, property_value: {value}')
                continue

            # pid = str(uuid.uuid4())[:8]
            pid = key
            property_mapping = PropertyMapping(
                pid = pid,
                name=key,
                generator=generator,
                args=args
            )
            property_mappings[pid] = property_mapping
        except Exception as e:
            ModuleLogger().warning(f'generate_mapping.py: propertymappings_for_raw_properties: could not create property mapping for key: {key}, property_value: {value}: ERROR: {e}')
            continue
    return property_mappings

def node_mappings_from(
    node_dicts: list,
    generators: dict[str, Generator]
    ) -> dict[str, NodeMapping]:
    """
        Converts node data from Arrows JSON format into NodeMapping objects.

        Performs validation on required fields and handles default values if missing. Example node_dict:
        {
            "id": "n1",
            "position": {
                "x": 284.5,
                "y": -204
            },
            "caption": "Company",
            "labels": [],
            "properties": {
                "name": "{\"company_name\":[]}",
                "uuid": "{\"uuid\":[8]}}",
                "COUNT": "{{"int\":[1]}"
            },
            "style": {}
        }

        Parameters:
            node_dicts (list): List of node data dicts from Arrows JSON 
            generators (dict): Available generator objects

        Returns:
            dict: NodeMapping objects keyed by node id
    """

    # Prepare a dict to store mappings.
    node_mappings = {}

    # Process each incoming node data
    for node_dict in node_dicts:

        if isinstance(node_dict, dict) is False:
            raise Exception(f"Node data is not a dict: {node_dict}")

        # Incoming data validation
        position = node_dict.get("position", None)
        if position is None:
            ModuleLogger().warning(f"Node properties is missing position key from: {node_dict}: Skipping {node_dict}")
            continue

        caption = node_dict.get("caption", None)
        if caption is None:
            ModuleLogger().warning(f"Node properties is missing caption key from: {node_dict}: Skipping {node_dict}")
            continue

        # Check for optional properties dict
        properties = node_dict.get("properties", {})
        # Always add a _uid property to node properties
        properties["_uid"] = "{\"uuid\":[]}"

        # Create property mappings for properties
        try: 
            property_mappings = propertymappings_for_raw_properties(properties, generators)
        except Exception as e:
            ModuleLogger().warning(f"Could not create property mappings for node: {node_dict}: {e}")
            continue

        # Determine count generator to use
        count_generator_config = properties.get("COUNT", None)

        # Gross
        # TODO: Cleanup

        # Count literal
        if count_generator_config is not None:
            literal = "".join(["{", '\"int\"', ":", "[",f'{count_generator_config}', "]", "}"])
            count_generator_config = literal
        if count_generator_config is None:
            count_generator_config = properties.get("{count}", None)
            # Legacy count linteral
            if count_generator_config is not None:
                literal = "".join(["{", '\"int\"', ":", "[",f'{count_generator_config}', "]", "}"])
                count_generator_config = literal
            if count_generator_config is None:
                # Default to a random int range
                count_generator_config = '{"int_range": [1,10]}'

        # Get proper generators for count generator
        try:
            count_generator, count_args = generator_for_raw_property(count_generator_config, generators)
        except Exception as e:
            ModuleLogger().warning(f"Could not find count generator for node: {node_dict}: {e}")
            continue

        # Get string name for key property. Value should be an unformatted string
        key = properties.get("KEY", None)
        if key is None:
            key = properties.get("{key}", None)
            if key is None:
                key = "_uid"
                ModuleLogger().debug(f"node properties is missing KEY or {{key}}: Assigning self generated _uid")

        # Assign correct property mapping as key property
        key_property = next((v for k,v in property_mappings.items() if v.name == key), None)
        if key_property is None:
            ModuleLogger().warning(f"Key property mapping not found for node: {node_dict} - key name: {key}. Skipping node.")
            continue

        # ModuleLogger().debug(f'Creating node mapping with caption: {caption}. Propery Mappings: {property_mappings.items()}')

        # Create node mapping
        node_mapping = NodeMapping(
            nid = node_dict["id"],
            labels = node_dict["labels"],
            properties = property_mappings,
            count_generator=count_generator,
            count_args=count_args,
            key_property=key_property,
            position = position,
            caption=caption
        )
        node_mappings[node_mapping.nid] = node_mapping
    return node_mappings

def relationshipmappings_from(
    relationship_dicts: List[Dict[str, Any]],
    nodes: Dict[str, NodeMapping],
    generators: Dict[str, Generator]
    ) -> Dict[str, RelationshipMapping]:
    """
    Converts relationship data from Arrows JSON format into RelationshipMapping objects. Example:
    {
        "id": "n0",
        "fromId": "n1",
        "toId": "n0",
        "type": "EMPLOYS",
        "properties": {
          "COUNT": "{\"int\":[10]}",
          "ASSIGNMENT": "{\"exhaustive_random\":[]}"
        },
        "style": {}
      },

    Performs validation on required fields.

    Parameters:
        relationship_dicts (list): List of relationship data dicts from Arrows JSON
        nodes (dict): NodeMapping objects 
        generators (dict): Available generator objects

    Returns: 
        A dictionary of { relationship id : list[RelationshipMapping objects]}
    """

    relationshipmappings = {}
    if relationship_dicts is None:
        ModuleLogger().debug(f'No relationship data to process')
        relationship_dicts = []

    if isinstance(relationship_dicts, list) is False:
        ModuleLogger().debug(f'Expected relationship_dicts to be a list of dictionaries, got {relationship_dicts}')
        relationship_dicts = []

    for relationship_dict in relationship_dicts:
        # Check for required data in raw node dict from arrows.app json

        if "id" not in relationship_dict:
            raise Exception(f"Relationship properties is missing 'id' key from: {relationship_dict}")

        if "type" not in relationship_dict:
            raise Exception(f"Relationship properties is missing 'type' key from: {relationship_dict}")

        if "fromId" not in relationship_dict:
            raise Exception(f"Relationship properties is missing 'fromId' key from: {relationship_dict}")

        if "toId" not in relationship_dict:
            raise Exception(f"Relationship properties is missing 'toId' key from: {relationship_dict}")

        # Check for required properties dict
        properties = relationship_dict.get("properties", {})

        # Determine count generator to use
        # TODO: Support COUNT key type
        count_generator_config = properties.get("COUNT", None)
        if count_generator_config is None:
            # Legacy keyword
            count_generator_config = properties.get("{count}", None)
            if count_generator_config is None:
                count_generator_config = '{"int_range": [1,3]}'
                ModuleLogger().debug(f"{relationship_dict} relationship properties is missing COUNT or '{{count}}' key from properties: {properties}: Using default int_range generator")

        assignment_generator_config = properties.get("ASSIGNMENT", None)
        if assignment_generator_config is None:
            # Legacy keyword
            assignment_generator_config = properties.get("{assignment}", None)
            # If missing, use ExhaustiveRandom
            if assignment_generator_config is None:
                assignment_generator_config = "{\"exhaustive_random_repeating\":[\"False\"]}"

        # Get proper generators for count generator
        try:
            count_generator, count_args = generator_for_raw_property(count_generator_config, generators)
        except Exception as e:
            raise Exception(f"Could not find count generator for relationship: {relationship_dict}: COUNT CONFIG: {count_generator_config}: ERROR: {e}")

        # Get proper generator for assignment generator
        # TODO: Explicitly assigned generators always causes an error
        try:
            assignment_generator, assignment_args = assignment_generator_for(assignment_generator_config, generators)
        except Exception as e:
            raise Exception(f"Could not get assignment generator for relationship: {relationship_dict}: {e}")
        
        # Create property mappings for properties
        try:
            property_mappings = propertymappings_for_raw_properties(properties, generators)
        except Exception as e:
            raise Exception(f"Could not create property mappings for relationship: {relationship_dict}: {e}")


        from_node = nodes.get(relationship_dict["fromId"], None)
        if from_node is None:
            raise Exception(f"No node mapping found for relationship: {relationship_dict} - fromId: {relationship_dict['fromId']}. Skipping relationship.")

        to_node = nodes.get(relationship_dict["toId"], None)
        if to_node is None:
            raise Exception(f"No node mapping found for relationship: {relationship_dict} - toId: {relationship_dict['toId']}. Skipping relationship.")

        # Create relationship mapping
        relationship_mapping = RelationshipMapping(
            rid = relationship_dict["id"],
            type = relationship_dict["type"],
            from_node = from_node,
            to_node = to_node ,
            count_generator=count_generator,
            count_args=count_args,
            properties=property_mappings,
            assignment_generator= assignment_generator,
            assignment_args=assignment_args
        )
        relationshipmappings[relationship_mapping.rid] = relationship_mapping

    return relationshipmappings


def mapping_from_json(
    json_config: dict,
    generators: dict[str, Generator]) -> Mapping:
    """
    Generates a Mapping object.

    Parameters:
        json_config (dict) : An ARROWs compatible JSON import/export file
        generators (dict[str, Generator]) : Dict of unique generator names to available generators

    Returns:
        Mapping object : Populated Mapping object
    """
    if isinstance(json_config, dict) is False:
        raise Exception(f"JSON object is not a dict: {json_config}")

    # Extract and process nodes
    node_dicts = json_config.get("nodes", None)
    if node_dicts is None:
        raise Exception(f" No nodes found in JSON file: {json}")
    relationship_dicts = json_config.get("relationships", None)
    if relationship_dicts is None:
        ModuleLogger().info(f"No relationships found in JSON file: {json}")

    # Convert source information to mapping objects
    nodes = node_mappings_from(node_dicts, generators)
    relationships = relationshipmappings_from(relationship_dicts, nodes, generators)

    # Create mapping object
    mapping = Mapping(
        nodes=nodes,
        relationships=relationships
    )

    return mapping