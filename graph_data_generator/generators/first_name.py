from faker import Faker
from datetime import datetime
from time import sleep
from graph_data_generator.logger import ModuleLogger

fake = Faker()

# Do not change function name or arguments
def generate(args: list[any]):
    # Roughly 100 milliseconds wait. Not guaranteed but that's okay, we just want a long enough pause to force any faker cycle.
    sleep(.1)
    # fake.seed_instance(datetime.now().timestamp())
    # fake.random.seed(datetime.now().timestamp())
    result = fake.unique.first_name()
    ModuleLogger().debug(f'first name: {result}')
    return result