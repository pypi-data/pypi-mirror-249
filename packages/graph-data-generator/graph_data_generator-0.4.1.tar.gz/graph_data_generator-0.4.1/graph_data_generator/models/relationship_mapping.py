
from graph_data_generator.models.node_mapping import NodeMapping
from graph_data_generator.models.property_mapping import PropertyMapping
from graph_data_generator.models.generator import Generator
from graph_data_generator.logger import ModuleLogger
import sys
from copy import deepcopy
from graph_data_generator.utils.list_utils import clean_list
from graph_data_generator.models.base_mapping import BaseMapping

class RelationshipMapping(BaseMapping):

    @staticmethod
    def empty():
        return RelationshipMapping(
            rid = "",
            type = "",
            from_node = None,
            to_node = None,
            properties = {},
            count_generator = None,
            count_args = [],
            filter_generator = None,
            filter_args = [],
            assignment_generator = None,
            assignment_args = [],
            filename = None
        )

    def __init__(
        self, 
        rid: str,
        type: str,
        properties: dict[str, PropertyMapping],
        from_node : NodeMapping,
        to_node : NodeMapping,
        # For determining count of relationships to generate
        count_generator: Generator,
        # For determining how to assign relationships -> to nodes
        assignment_generator: Generator,
        assignment_args: list[any] = [],
        count_args: list[any] = [],
        # TODO: Make below non-optional
        # For filtering from nodes
        filter_generator: Generator = None,
        filter_args: list[any] = [],
        filename: str = None
        ):
        self.rid = rid
        self.type = type
        self.from_node = from_node
        self.to_node = to_node
        self.properties = properties
        self.count_generator = count_generator
        self.count_args = clean_list(count_args)
        self._generated_values = None
        self.filter_generator = filter_generator
        self.filter_generator_args = clean_list(filter_args)
        self.assignment_generator = assignment_generator
        self.assignment_args = clean_list(assignment_args)
        self._filename = filename

    def __str__(self):
        return f"RelationshipMapping(rid={self.rid}, type={self.type}, from_node={self.from_node}, to_node={self.to_node}, properties={self.properties}, count_generator={self.count_generator}, count_args={self.count_args})"

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        return {
            "rid": self.rid,
            "type": self.type,
            "from_node": self.from_node.to_dict() if self.from_node is not None else None,
            "to_node": self.to_node.to_dict() if self.to_node is not None else None,
            "properties": {key: property.to_dict() for (key,property) in self.properties.items()},
            "count_generator": self.count_generator.to_dict() if self.count_generator is not None else None,
            "count_args": self.count_args
            # TODO: Add filter_generator, filter_args, assignment_generator, assignment_args
        }

    def filename(self):
        if self._filename is not None:
            return self._filename
        # default
        from_node_name = self.from_node.caption.lower()
        to_node_name = self.to_node.caption.lower()
        return f"{from_node_name}_{self.type.lower()}_{to_node_name}_{self.rid.lower()}"

    # TODO: Verify unique keys are respected during generation

    def ready_to_generate(self):
        if self.type is None:
            return False
        if self.from_node is None:
            return False
        if self.to_node is None:
            return False
        if self.count_generator is None:
            return False
        if self.assignment_generator is None:
            return False
        return True

    def generate_values(self)-> list[dict]:

        # Sample return list:
        # [
        #  {
        #    "<from_node_key_property_name>": "n1_abc",
        #    "<to_node_key_property_name>": "n2_abc",
        #    "since": "2020-01-01"
        #   }
        # ]


        # Store generated relationships to return
        all_results = []

        # TODO: Run filter generator here to determine which source nodes to process

        # Make a copy of the generated list
        values = self.to_node.generated_values()[:]
        original_values = self.to_node.generated_values()[:]

        # Iterate through every generated source node
        for value_dict in self.from_node.generated_values():
            # dict of property names and generated values

            # Decide on how many of these relationships to generate
            count = 0
            try:
                count = self.count_generator.generate(self.count_args)
                ModuleLogger().debug(f'{self.from_node.caption} node: {self.type} relationship count: {count}')
            except:
                # Generator not found or other code error
                raise Exception(f"Relationship mapping could not generate a number of relationships to continue generation process, error: {str(sys.exc_info()[0])}")

            # Validate something to process for this source node
            if value_dict.keys() is None or len(value_dict.keys()) == 0:
                # Data importer requires at least one property-value
                raise Exception(f"No properties found for NodeMapping: {self.from_node}")

            # Get the key property name and value for the source node record
            from_node_key_property_name = self.from_node.key_property.name
            from_node_key_property_value = value_dict.get(from_node_key_property_name, None)
            if from_node_key_property_value is None:
                raise Exception(f"Key property '{from_node_key_property_name}' not found in node: {value_dict}")

            # If count is zero - no relationship to generate for the current source node

            # Generate a new relationship for each count
            for i in range(count):
                # Select a random target node

                # if values is None or len(values) == 0:
                #     # No values to run
                #     continue

                # Extract results. Values will be passed back through the next iteration in case the generator returns a modified list

                ModuleLogger().debug(f"Relationship: {self} Assignement args: {self.assignment_args}")

                composite_values = [self.assignment_args, value_dict, values, original_values]

                # TODO: Why are values not changing after this call
                to_node_value_dict, new_values = self.assignment_generator.generate(composite_values)
                
                # Assignment Generator hit an end
                if to_node_value_dict is None:
                    ModuleLogger().debug(f'End of assignment generator reached: {self.assignment_generator} for relationship: {self}')
                    continue

                # Get key property name and value for target record
                to_node_key_property_name = self.to_node.key_property.name
                # TODO: Adding an ASSIGNMENT key breaks here - Why?
                to_node_key_property_value = to_node_value_dict[to_node_key_property_name]

                values = new_values

                # Generate the relationship
                result = {
                    f'_from_{from_node_key_property_name}': from_node_key_property_value,
                    f'_to_{to_node_key_property_name}': to_node_key_property_value
                }


                # TODO: Sort properties so reference generators are last

                # Generate relationships properties
                for property_name, property_mapping in self.properties.items():
                    result[property_name] = property_mapping.generate_values()[0]

                # Add the relationship to the list
                all_results.append(result)

        # Store results for reference
        self._generated_values = all_results
        return self._generated_values
        
    def generated_values(self):
        if self._generated_values is None:
            self.generate_values()
        return self._generated_values