from random import shuffle
import random
from graph_data_generator.logger import ModuleLogger
import json

# This will only work for one source node cycle
exhaustive_random_cache = {}

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

def origin_already_referenced(origin: any, choice: any) -> bool:
    global exhaustive_random_cache

    json_origin = json.dumps(origin, sort_keys=True)
    json_choice = json.dumps(choice, sort_keys=True)
    for cache_key, cache_values in enumerate(exhaustive_random_cache.items()):
        if json_origin in cache_values:
            # Current choice would create a circular reference
            if json_choice == cache_key:
                return True
    return False
    
def update_cache(origin: any, choice: any):
    global exhaustive_random_cache

    json_origin = json.dumps(origin, sort_keys=True)
    json_choice = json.dumps(choice, sort_keys=True)

    if json_origin in exhaustive_random_cache.keys():
        # Existing record
        existing_list = exhaustive_random_cache[json_origin]
    else:
        # New record
        existing_list = []

    # Update cache
    existing_list.append(json_choice)
    exhaustive_random_cache.update(json_origin=existing_list)

# Do not change function name or arguments
def generate(
    args: list[any]
    ) -> tuple[dict, list[dict]]:

    global exhaustive_random_cache

    if isinstance(args, list) == False:
        return (None, [])
    
    # Assignment Args
    options = args[0]

    try:
        can_circular_reference = str2bool(options[1])
    except:
        can_circular_reference = False

    # Origin node
    origin = args[1]

    # Target nodes
    choices = args[2]

    # Original choices
    original_choices = args[3]

    # start cycle
    if len(choices) == len(original_choices):
        # Reset cache at start of cycle
        exhaustive_random_cache = {}

    # End cycle
    if len(choices) == 0:
        return (None, [])

    # Randomly select target
    shuffle(choices)
    choice = random.choice(choices)

    # Prevent circular references
    if can_circular_reference is False:

        # First check for self reference
        while choice == origin:
            choices.remove(choice)

            if len(choices) == 0:
                return (None, [])
            
            choice = choices[0]

        # Using a cache to determine which nodes have selected which others
        circular_reference = True
        while circular_reference is True:

            circular_reference = origin_already_referenced(origin, choice)

            if circular_reference == True:
                # Remove current choice from options
                choices.remove(choice)

                # Exhausted options, exit
                if len(choices) == 0:
                    return (None, [])
                
                choice = choices[0]

        update_cache(origin, choice)

    choices.remove(choice)
    return (choice, choices)