from graph_data_generator.logger import ModuleLogger
import json


def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

    
def update_cache(origin: any, choice: any):
    global sequential_cache

    json_origin = json.dumps(origin, sort_keys=True)
    json_choice = json.dumps(choice, sort_keys=True)

    if json_origin in sequential_cache.keys():
        # Existing record
        existing_list = sequential_cache[json_origin]
    else:
        # New record
        existing_list = []

    # Update cache
    existing_list.append(json_choice)
    sequential_cache.update(json_origin=existing_list)

# Do not change function name or arguments
def generate(
    args: list[any]
    ) -> tuple[dict, list[dict]]:

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
    _ = args[3]

    # Error catch
    if len(choices) == 0:
        return (None, [])
    
    # Select next target
    choice = choices[0]

    # Prevent circular references
    if can_circular_reference is False:

        # Check for self reference
        while choice == origin:
            choices.remove(choice)

            if len(choices) == 0:
                return (None, [])
            
            choice = choices[0]


    choices.remove(choice)
    return (choice, choices)