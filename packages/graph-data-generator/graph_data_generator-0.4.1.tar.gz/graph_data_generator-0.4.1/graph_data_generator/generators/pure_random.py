import random
# Do not change function name or arguments
def generate(
    args: list[any]
    ) -> tuple[dict, list[dict]]:
    
    if isinstance(args, list) == False:
        return (None, [])
    if len(args) == 0:
        return (None, [])
    
    # Options
    _ = args[0]

    # Origin node
    _ = args[1]

    # Target nodes
    choices = args[2]

    result = random.choice(choices)
    return (result, choices)