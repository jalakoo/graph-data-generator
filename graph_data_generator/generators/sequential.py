from graph_data_generator.logger import ModuleLogger
import json

sequential_cache = {}

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

def origin_already_referenced(origin: any, choice: any) -> bool:
    global sequential_cache

    json_origin = json.dumps(origin, sort_keys=True)
    json_choice = json.dumps(choice, sort_keys=True)
    for cache_key, cache_values in enumerate(sequential_cache.items()):
        if json_origin in cache_values:
            # Current choice would create a circular reference
            if json_choice == cache_key:
                return True
    return False
    
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

    global sequential_cache

    if isinstance(args, list) == False:
        return (None, [])
    
    # Assignment Args
    options = args[0]

    ModuleLogger().info(f'sequential args received: {options}')

    try:
        can_repeat = str2bool(options[0])
        can_circular_reference = str2bool(options[1])
    except:
        can_repeat = True
        can_circular_reference = True

    ModuleLogger().info(f'sequential args processed: can repeat:{can_repeat}, can circular reference: {can_circular_reference}')

    # Origin node
    origin = args[1]

    # Target nodes
    choices = args[2]

    # Original choices
    original_choices = args[3]

    # End cycle
    if len(choices) == 0:
        if can_repeat == False:
            # End further relationship generation
            return (None, [])
        else:
            # Copy original back into temp queue
            choices = original_choices[:]

    # Select target
    choice = choices[0]

    # Prevent circular references
    if can_circular_reference is False:

        # First check for self reference
        while choice == origin:
            choices.remove(choice)

            if len(choices) == 0:
                return (None, [])
            
            choice = choices[0]

        # Using a cache to determine which nodes have selected which others
        if len(choices) == len(original_choices):
            # Reset cache at start of cycle
            sequential_cache = {}
        else:
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