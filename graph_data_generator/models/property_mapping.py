from graph_data_generator.models.generator import Generator
from graph_data_generator.utils.list_utils import clean_list
from graph_data_generator.models.base_mapping import BaseMapping

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

    # def generate_value(self):
    #     if self.generator == None:
    #         raise Exception(f'Property Mapping is missing a generator property. Property name: {self.name}')
    #     if isinstance(self.args, list) == False:
    #         raise Exception(f'Property Mapping Args is not a list. Property name: {self.name}')
    #     result = self.generator.generate(self.args)
    #     return result
    
    def generate_values(self) -> list[dict]:
        if self.generator == None:
            raise Exception(f'Property Mapping is missing a generator property. Property name: {self.name}')
        if isinstance(self.args, list) == False:
            raise Exception(f'Property Mapping Args is not a list. Property name: {self.name}')
        result = self.generator.generate(self.args)
        return [result]

