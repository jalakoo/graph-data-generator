from random import shuffle

# Do not change function name or arguments
def generate(
    args: list[any]
    ) -> tuple[dict, list[dict]]:

    if isinstance(args, list) == False:
        return (None, [])
    
    node_values = args[0]
    if len(node_values) == 0:
        original = args[1]
        node_values = original[:]

    shuffle(node_values)
    choice = node_values.pop(0)
    return (choice, node_values)