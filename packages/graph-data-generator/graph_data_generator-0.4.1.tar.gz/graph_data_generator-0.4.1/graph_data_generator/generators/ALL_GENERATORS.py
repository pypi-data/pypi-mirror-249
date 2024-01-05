
# Attempts to import by filename when in a package did not work - so importing all the generator files explicitly here. This is not ideal but works for now.

from graph_data_generator.models.generator import generators_from_json

# Regular generators
from graph_data_generator.generators import bool, catch_phrase, city, company_name, country, credit_card_expire, credit_card_number, credit_card_provider, date, email, first_name, float, float_from_list, float_range, hierarchical, int, int_from_list, int_range, isbn_10, isbn_13, job, last_name, lorem_paragraphs, loremtext_sentence, loremtext_words, md5, phone_number, ssn, string_from_csv, string_from_list, string_literal, technical_phrase, uri, uuid

# Functional generators
from graph_data_generator.generators import add_floats, add_ints, add_strings

# Assignment Generators
from graph_data_generator.generators import pure_random, exhaustive_random, hierarchical, exhaustive_random_repeating

# Reference generators
from graph_data_generator.generators import reference

# key name and generator name somewhat duplicitous currently. Keys will remain unchanged, but name add separately to support multi-lingu support (someday) 
# this object can be read externally to reference available generators and data about them.
generators_json = {
    "README":{
        "content": "This is the default list of all generators used by the app. If you add new generators they will be added to this file. The default_generators.json file contains a copy of this from the repo maintainer(s)"
    },
    "add_ints": {
        "args": [
            {
                "default": "",
                "label": "Generator Specifications",
                "type": "String"
            }
        ],
        "code": add_ints,
        "description": "Combines output from a list of other generators into a single integer value",
        "name": "Add Integers",
        "tags": [
            "function",
            "int",
            "integer",
            "integers"
            "generators",
            "sum",
            "combine"
        ],
        "type": "Function"
    },
    "add_floats": {
        "args": [
            {
                "default": "",
                "label": "Generator Specifications",
                "type": "String"
            }
        ],
        "code": add_floats,
        "description": "Combines output from a list of other generators into a single float value",
        "name": "Add Floats",
        "tags": [
            "function",
            "float",
            "numbers",
            "generators",
            "sum",
            "combine"
        ],
        "type": "Function"
    },
    "add_strings": {
        "args": [
            {
                "default": "",
                "label": "Generator Specifications",
                "type": "String"
            }
        ],
        "code": add_strings,
        "description": "Combines output from a list of other generators into a single string",
        "name": "Add Strings",
        "tags": [
            "function",
            "string",
            "generators",
            "aggregate",
            "combine"
        ],
        "type": "Function"
    },
    "bool": {
        "args": [
            {
                "default": 50,
                "label": "Percent chance of true (out of 100)",
                "type": "Integer"
            }
        ],
        "code": bool,
        "description": "Bool generator using the Faker library.",
        "name": "Bool",
        "tags": [
            "bool",
            "boolean"
        ],
        "type": "Bool"
    },
    "catch_phrase": {
        "args": [],
        "code": catch_phrase,
        "description": "Phrase with first letter capitalized. Faker Library",
        "name": "Catch Phrase",
        "tags": [
            "phrase",
            "phrases",
            "catch",
            "project",
            "description"
        ],
        "type": "String"
    },
    "city": {
        "args": [],
        "code": city,
        "description": "City name generator using the Faker library.",
        "name": "City",
        "tags": [
            "city",
            "name"
        ],
        "type": "String"
    },
    "company_name": {
        "args": [],
        "code": company_name,
        "description": "Company name generator using the Faker library.",
        "name": "Company Name",
        "tags": [
            "company",
            "name"
        ],
        "type": "String"
    },
    "country": {
        "args": [],
        "code": country,
        "description": "Country name generator using the Faker library.",
        "name": "Country",
        "tags": [
            "country",
            "from"
        ],
        "type": "String"
    },
    "credit_card_expire": {
        "args": [],
        "code": credit_card_expire,
        "description": "Credit card expirary number using the Faker library.",
        "name": "Credit Card Expire",
        "tags": [
            "credit card",
            "expire"
        ],
        "type": "String"
    },
    "credit_card_number": {
        "args": [],
        "code": credit_card_number,
        "description": "Credit card number using the Faker library.",
        "name": "Credit Card Number",
        "tags": [
            "credit card",
        ],
        "type": "String"
    },
    "credit_card_provider": {
        "args": [],
        "code": credit_card_provider,
        "description": "Credit card provider company using the Faker library.",
        "name": "Credit Card Provider",
        "tags": [
            "credit card",
        ],
        "type": "String"
    },
    "date": {
        "args": [
            {
                "default": "1970-01-01",
                "label": "Oldest Date",
                "type": "Datetime"
            },
            {
                "default": "2022-11-24",
                "label": "Newest Date",
                "type": "Datetime"
            }
        ],
        "code": date,
        "description": "Generate a random date between 2 specified dates. Exclusive of days specified.",
        "name": "Date",
        "tags": [
            "date",
            "datetime",
            "created",
            "updated",
            "at"
        ],
        "type": "Datetime"
    },
    "email": {
        "args": [
            {
                "default": "",
                "label": "Optional Domain (ie: company.com)",
                "type": "String"
            }
        ],
        "code": email,
        "description": "Random email with Faker library.",
        "name": "Email",
        "tags": [
            "email"
        ],
        "type": "String"
    },
    "exhaustive_random": {
        "args": [
            {
                "default": False,
                "label": "Allow circular reference. Source nodes able to reference themselves for this relationship type. Default False.",
                "type": "Boolean"
            }
        ],
        "code": exhaustive_random,
        "description": "Assigns each source node to a random target node, until target node records are exhausted. Further relationship generation will stop when this occurs.",
        "name": "Exhaustive Random",
        "tags": [
            "exhaustive"
        ],
        "type": "Assignment"
    },
    "exhaustive_random_repeating": {
        "args": [
            {
                "default": False,
                "label": "Allow circular reference. Source nodes able to reference themselves for this relationship type. Default False.",
                "type": "Boolean"
            }
        ],
        "code": exhaustive_random_repeating,
        "description": "Assigns each source node to a random target node until target node records are exhausted. When list is exhausted, it will be regenerated to continue until until all source nodes have generated this relationship type.",
        "name": "Exhaustive Random Repeating",
        "tags": [
            "exhaustive",
            "repeating"
        ],
        "type": "Assignment"
    },
    "first_name": {
        "args": [],
        "code": first_name,
        "description": "First name generator using the Faker library",
        "name": "First Name",
        "tags": [
            "first",
            "name"
        ],
        "type": "String"
    },
    "float_from_list": {
        "args": [
            {
                "default": "",
                "label": "List of float values (ie: 1.0, 2.2, 3.3)",
                "type": "String"
            }
        ],
        "code": float_from_list,
        "description": "Randomly selected float from a comma-seperated list of options.",
        "name": "Float from list",
        "tags": [
            "float",
            "list"
        ],
        "type": "Float"
    },
    "float": {
        "args": [
            {
                "default": 0.0,
                "label": "Value",
                "type": "Float"
            }
        ],
        "code": float,
        "description": "Literal float value",
        "name": "Float",
        "tags": [
            "float",
            "decimal",
            "number",
            "num",
            "count",
            "cost",
            "price"
        ],
        "type": "Float"
    },
    "float_range": {
        "args": [
            {
                "default": 0.0,
                "label": "Min",
                "type": "Float"
            },
            {
                "default": 1.0,
                "label": "Max",
                "type": "Float"
            },
            {
                "default": 2,
                "label": "Decimal Places",
                "type": "Integer"
            }
        ],
        "code": float_range,
        "description": "Random float between a range. Inclusive.",
        "name": "Float from range",
        "tags": [
            "float",
            "decimal",
            "number",
            "num",
            "count",
            "cost",
            "price"
        ],
        "type": "Float"
    },
    "hierarchical": {
        "args": [
            {
                "default": False,
                "label": "Allow circular reference. Source nodes can reference themselves for this relationship type. Default False.",
                "type": "Boolean"
            }
        ],
        "code": hierarchical,
        "description": "Assigns each source node to the next node in the generated list. Continues until node records are exhausted.",
        "name": "Hierarchical",
        "tags": [
            "heirarchical",
            "org chart"
        ],
        "type": "Assignment"
    },
    "int_from_list": {
        "args": [
            {
                "default": "",
                "label": "List of integers (ie: 1, 2, 3)",
                "type": "String"
            }
        ],
        "code": int_from_list,
        "description": "Randomly selected int from a comma-seperated list of options. If no list provided, will return 0",
        "name": "Int from list",
        "tags": [
            "int",
            "integer",
            "number",
            "num",
            "count",
            "list",
            "salary",
            "cost"
        ],
        "type": "Integer"
    },
    "int": {
        "args": [
            {
                "default": 1,
                "label": "Value",
                "type": "Integer"
            }
        ],
        "code": int,
        "description": "Constant integer value",
        "name": "Int",
        "tags": [
            "int",
            "integer",
            "num",
            "number",
            "count"
        ],
        "type": "Integer"
    },
    "int_range": {
        "args": [
            {
                "default": 1,
                "label": "Min",
                "type": "Integer"
            },
            {
                "default": 10,
                "label": "Max",
                "type": "Integer"
            }
        ],
        "code": int_range,
        "description": "Random integer from a min and max value argument. Argument values are inclusive.",
        "name": "Int Range",
        "tags": [
            "int",
            "integer",
            "number",
            "num",
            "count"
        ],
        "type": "Integer"
    },
    "isbn_10": {
        "args": [
        ],
        "code": isbn_10,
        "description": "Random International Standard Book Number (ISBN) 10 number using Faker library",
        "name": "ISBN 10",
        "tags": [
            "ISBN",
            "International"
        ],
        "type": "String"
    },
    "isbn_13": {
        "args": [
        ],
        "code": isbn_13,
        "description": "Random International Standard Book Number (ISBN) 13 number using Faker library",
        "name": "ISBN 13",
        "tags": [
            "ISBN",
            "International"
        ],
        "type": "String"
    },
    "job": {
        "args": [],
        "code": job,
        "description": "Random job title using the Faker library.",
        "name": "Job",
        "tags": [
            "job",
            "occupation"
        ],
        "type": "String"
    },
    "last_name": {
        "args": [],
        "code": last_name,
        "description": "Last name generator using the Faker library.",
        "name": "Last Name",
        "tags": [
            "last",
            "name"
        ],
        "type": "String"
    },
    "lorem_words": {
        "args": [
            {
                "default": 1,
                "label": "Minimum Number",
                "type": "Integer"
            },
            {
                "default": 10,
                "label": "Maximum Number",
                "type": "Integer"
            }
        ],
        "code": loremtext_words,
        "description": "String generator using the lorem-text package",
        "name": "Words",
        "tags": [
            "words",
            "lorem",
            "text",
            "description"
        ],
        "type": "String"
    },
    "lorem_paragraphs": {
        "args": [
            {
                "default": 1,
                "label": "Minimum Number",
                "type": "Integer"
            },
            {
                "default": 10,
                "label": "Maximum Number",
                "type": "Integer"
            }
        ],
        "code": lorem_paragraphs,
        "description": "String generator using the lorem-text package",
        "name": "Paragraphs",
        "tags": [
            "string",
            "lorem",
            "ipsum",
            "paragraph",
            "paragraphs"
        ],
        "type": "String"
    },
    "lorem_sentences": {
        "args": [
            {
                "default": 1,
                "label": "Minimum Number",
                "type": "Integer"
            },
            {
                "default": 10,
                "label": "Maximum Number",
                "type": "Integer"
            }
        ],
        "code": loremtext_sentence,
        "description": "String generator using the lorem-text package",
        "name": "Sentences",
        "tags": [
            "sentence",
            "sentences",
            "lorem",
            "text",
            "description"
        ],
        "type": "String"
    },
    "md5": {
        "args": [
            {
                "default": 33,
                "label": "Limit Character Length",
                "type": "Integer"
            }
        ],
        "code": md5,
        "description": "Random MD5 hash using Faker library. 33 Characters max",
        "name": "MD5",
        "tags": [
            "md5",
            "hash",
            "unique"
        ],
        "type": "String"
    },
    "phone_number": {
        "args": [
        ],
        "code": phone_number,
        "description": "Random phone number using Faker library.",
        "name": "Phone Number",
        "tags": [
            "phone",
            "number"
        ],
        "type": "String"
    },
    "pure_random": {
        "args": [],
        "code": pure_random,
        "description": "Randomly assigns to a target node. Self referencing and orphan nodes possible.",
        "name": "Pure Random",
        "tags": [
            "random"
        ],
        "type": "Assignment"
    },
    # "reference": {
    #     "args": [
    #         {
    #             "default": "",
    #             "label": "Property key name to reference",
    #             "type": "String"
    #         },
    #     ],
    #     "code": reference,
    #     "description": "Copies a value from another property by the property key name.",
    #     "name": "Reference",
    #     "tags": [
    #         "reference",
    #         "pointer",
    #     ],
    #     "type": "Reference"
    # },
    "ssn": {
        "args": [
        ],
        "code": ssn,
        "description": "Social Security Number using Faker library",
        "name": "SSN",
        "tags": [
            "ssn",
            "social",
            "security"
        ],
        "type": "String"
    },
    "string": {
        "args": [
            {
                "default": "",
                "label": "List of words (ie: alpha, brave, charlie)",
                "type": "String"
            }
        ],
        "code": string_literal,
        "description": "Explicit string value",
        "name": "String Literal",
        "tags": [
            "string",
            "word",
            "literal"
        ],
        "type": "String"
    },
    "string_from_list": {
        "args": [
            {
                "default": "",
                "label": "List of words (ie: alpha, brave, charlie)",
                "type": "String"
            }
        ],
        "code": string_from_list,
        "description": "Randomly selected string from a comma-seperated list of options.",
        "name": "String from list",
        "tags": [
            "string",
            "list",
            "word",
            "words",
            "status",
            "type"
        ],
        "type": "String"
    },
    "string_from_csv": {
        "args": [
            {
                "default": "",
                "label": "CSV Filepath",
                "type": "String",
                "hint": "mock_generators/datasets/tech_companies.csv",
                "description":""
            },
            {
                "default": "",
                "label": "Header Column Field",
                "type": "String",
                "hint": "Company Name",
                "description":""
            }
        ],
        "code": string_from_csv,
        "description": "Random string row value from a specified csv file. Be certain field contains string values.",
        "name": "String from CSV",
        "tags": [
            "csv",
            " string",
            " random"
        ],
        "type": "String"
    },
    "technical_phrase": {
        "args": [],
        "code": technical_phrase,
        "description": "Technobabble words all lower-cased. Faker Library",
        "name": "Technical BS Phrase",
        "tags": [
            "phrase",
            "phrases",
            "technical",
            "jargon",
            "task",
            "description"
        ],
        "type": "String"
    },
    "uri": {
        "args": [],
        "code": uri,
        "description": "Random URI with Faker library.",
        "name": "URL",
        "tags": [
            "uri",
            "url"
        ],
        "type": "String"
    },
    "uuid": {
        "args": [
            {
                "default": 37,
                "label": "Limit character length",
                "type": "Integer"
            }
        ],
        "code": uuid,
        "description": "Random UUID 4 hash using Faker library. 37 Characters Max.",
        "name": "UUID",
        "tags": [
            "uuid",
            "hash",
            "unique",
            "uid"
        ],
        "type": "String"
    }
}

generators = generators_from_json(generators_json)