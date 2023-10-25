import random
# Do not change function name or arguments
def generate(
    args: list[any]
    ) -> tuple[dict, list[dict]]:
    
    if isinstance(args, list) == False:
        return (None, [])
    if len(args) == 0:
        return (None, [])
    choices = args[0]
    result = random.choice(choices)
    return (result, args)