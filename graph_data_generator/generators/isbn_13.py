from faker import Faker

fake = Faker()

# Do not change function name or arguments
def generate(args: list[any]):
    result = fake.isbn13()
    return result