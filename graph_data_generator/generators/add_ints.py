

def generate(args: list[any]):
    """
    Generate a sum of outputs from number generators.

    Args:
    args (list[any]): A list of generator specification to run and whose results to sum.

    Returns:
    int: Sum of outputs from specified number generators
    """
    result = 0
    for num in args:
        result += int(num)
    return result