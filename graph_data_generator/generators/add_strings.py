

from graph_data_generator.logger import ModuleLogger

def generate(args: list[any]):
    """
    Aggregates outputs from other generators.

    Args:
    args (list[any]): A list of generator outputs to aggregate.

    Returns:
    string: Aggregate string output from specified generators
    """
    # Prior generators must have run, we're only aggregating outputs
    result = ""
    for output in args:
        result = f"{result}{output}"
    ModuleLogger().info(f'Aggregate result: {result}')
    return result
