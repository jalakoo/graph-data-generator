from graph_data_generator.models.generator import Generator, GeneratorType
from graph_data_generator.utils.list_utils import clean_list
from graph_data_generator.models.base_mapping import BaseMapping
from graph_data_generator.logger import ModuleLogger
class PropertyMapping(BaseMapping):

    @staticmethod
    def empty():
        return PropertyMapping(
            pid = None,
            name = None,
            generator = None,
            args = None
        )

    def __init__(
        self, 
        pid: str,
        name: str = None, 
        generator: Generator = None, 
        # Args to pass into generator during running
        args: list[any] = []):
        self.pid = pid
        self.name = name
        self.generator = generator
        self.args = args

    def __str__(self):
        name = self.name if self.name is not None else "<unnamed>"
        generator = self.generator if self.generator is not None else "<no_generator_assigned>"
        return f"PropertyMapping(pid={self.pid}, name={name}, generator={generator}, args={self.args}"
        
    # def __repr__(self):
    #     return self.__str__()

    # def __equ__(self, other):
    #     return self.pid == other.pid

    def to_dict(self):
        return {
            "pid": self.pid,
            "name": self.name,
            "generator": self.generator.to_dict() if self.generator is not None else None,
            "args": clean_list(self.args)
        } 

    def ready_to_generate(self):
        if self.name is None:
            return False
        if self.generator is None:
            return False
        return True
    
    def generate_values(self) -> list[dict]:
        if self.generator == None:
            raise Exception(f'Property Mapping named {self.name} is missing a generator property.')
        if self.generator.type == GeneratorType.FUNCTION and isinstance(self.args, list):
            # Assuming this is a list of tuples - can not check for paramterized generic classes
            ModuleLogger().debug(f'Property mapping with function generator named {self.generator.name} detected. Args: {self.args}')
            # Force any Generator args to generate
            new_args = []
            for gen_arg in self.args:
                if isinstance(gen_arg, tuple) == False:
                    # Not a tuple of (Generator, arg). Process as is
                    new_args.append(gen_arg)
                    continue
                gen = gen_arg[0]
                if isinstance(gen, Generator) == False:
                    # Not a tuple of (Generator, args) or already ran
                    new_args.append(gen_arg)
                    continue
                ModuleLogger().debug(f'Processing tuple gen_arg: {gen_arg}...')
                output = gen.generate(gen_arg[1])
                new_args.append(output)
            self.args = new_args
            # ModuleLogger().debug(f'Generated args: {self.args}')
        result = self.generator.generate(self.args)
        # ModuleLogger().debug(f'Generated values: {result}')
        return [result]

