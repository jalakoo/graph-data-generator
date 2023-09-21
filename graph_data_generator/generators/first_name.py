from faker import Faker
from graph_data_generator.logger import ModuleLogger

fake = Faker()

# Do not change function name or arguments
def generate(args: list[any]):
    result = fake.first_name()
    return result