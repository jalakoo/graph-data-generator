from random import shuffle
import random
from graph_data_generator.logger import ModuleLogger
import json

exhaustive_random_cache = {}

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

    
# Do not change function name or arguments
def generate(
    args: list[any]
    ) -> tuple[dict, list[dict]]:

    global exhaustive_random_cache

    if isinstance(args, list) == False:
        return (None, [])
    
    # Assignment Args
    options = args[0]

    ModuleLogger().info(f'exhaustive_random args received: {options}')

    try:
        can_repeat = str2bool(options[0])
        # can_self_reference = str2bool(options[1])
        can_circular_reference = str2bool(options[1])
    except:
        can_repeat = True
        # can_self_reference = True
        can_circular_reference = True

    ModuleLogger().info(f'exhaustive_random args processed: can repeat:{can_repeat}, can circular reference: {can_circular_reference}')

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

    # Randomly select target
    shuffle(choices)
    choice = random.choice(choices)

   # Prevent self assignment
    # if can_self_reference is False:
    #     while choice == origin:
    #         choices.remove(choice)

    #         if len(choices) == 0:
    #             return (None, [])
            
    #         choice = random.choice(choices)

    # Prevent circular references
    if can_circular_reference is False:
        # Prevent a node from relating to a node that is already related to it. Good for creating hierarchies

        # Using a cache to determine which nodes have selected which others
        if len(choices) == len(original_choices):
            # Reset cache at start of cycle
            exhaustive_random_cache = {}
        else:
            # Cache already in use

            # Convert choices to json so we can do comparisons
            json_origin = json.dumps(origin, sort_keys=True)
            json_choice = ""

            circular_reference = True
            while circular_reference is True:

                circular_reference = False

                # Update json_choice for each cycle
                json_choice = json.dumps(choice, sort_keys=True)

                # Origin already associated as a target node for a prior node?
                for cache_key, cache_values in enumerate(exhaustive_random_cache.items()):
                    if json_origin in cache_values:
                        # Current choice would create a circular reference
                        if json_choice == cache_key:
                            circular_reference = True

                # Direct self referencing
                if json_origin == json_choice:
                    circular_reference = True

                if circular_reference is True:
                    # Remove current choice from options
                    choices.remove(choice)

                    # Exhausted options, exit
                    if len(choices) == 0:
                        return (None, [])
                    
                    choice = random.choice(choices)


            # Record choice selection in cache

            # Gives an unexpected KeyError
            # exhaustive_random_cache[json_origin] == json_choice

            if json_origin in exhaustive_random_cache.keys():
                # Existing record
                existing_list = exhaustive_random_cache[json_origin]
            else:
                # New record
                existing_list = []

            # Update cache
            existing_list.append(json_choice)
            exhaustive_random_cache.update(json_origin=existing_list)

    choices.remove(choice)
    return (choice, choices)