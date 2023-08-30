from faker import Faker
import time
fake = Faker()


# Do not change function name or arguments
def generate(args: list[any]):
    fake.seed_instance(time.time_ns())
    result = fake.unique.last_name()
    return result