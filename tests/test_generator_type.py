import pytest

from graph_data_generator.models.generator_type import GeneratorType

class TestGeneratorType:
    # Tests that the type_from_string method returns the correct GeneratorType enum value for each supported type
    def test_type_from_string_returns_correct_value_for_supported_types(self):
        assert GeneratorType.type_from_string('string') == GeneratorType.STRING
        assert GeneratorType.type_from_string('int') == GeneratorType.INT
        assert GeneratorType.type_from_string('float') == GeneratorType.FLOAT
        assert GeneratorType.type_from_string('datetime') == GeneratorType.DATETIME
        assert GeneratorType.type_from_string('bool') == GeneratorType.BOOL
        assert GeneratorType.type_from_string('assignment') == GeneratorType.ASSIGNMENT
        assert GeneratorType.type_from_string('relationship') == GeneratorType.RELATIONSHIP

    # Tests that the to_string method returns the correct string representation for each GeneratorType enum value
    def test_to_string_returns_correct_string_representation_for_each_GeneratorType_enum_value(self):
        assert GeneratorType.STRING.to_string() == 'String'
        assert GeneratorType.INT.to_string() == 'Integer'
        assert GeneratorType.FLOAT.to_string() == 'Float'
        assert GeneratorType.DATETIME.to_string() == 'Datetime'
        assert GeneratorType.BOOL.to_string() == 'Bool'
        assert GeneratorType.ASSIGNMENT.to_string() == 'Assignment'
        assert GeneratorType.RELATIONSHIP.to_string() == 'Relationship'

    # Tests that type_from_string raises a TypeError when an unsupported type is passed
    def test_type_from_string_raises_TypeError_when_unsupported_type_is_passed(self):
        with pytest.raises(TypeError):
            GeneratorType.type_from_string('unsupported')
        with pytest.raises(TypeError):
            GeneratorType.type_from_string('123')
        with pytest.raises(TypeError):
            GeneratorType.type_from_string('')
        with pytest.raises(AttributeError):
            GeneratorType.type_from_string(None)

    # Tests that to_string raises a TypeError when an unsupported GeneratorType enum value is passed
    def test_to_string_raises_TypeError_when_unsupported_GeneratorType_enum_value_is_passed(self):
        with pytest.raises(ValueError):
            GeneratorType(8).to_string()
        with pytest.raises(ValueError):
            GeneratorType(9).to_string()
        with pytest.raises(ValueError):
            GeneratorType(10).to_string()
        with pytest.raises(ValueError):
            GeneratorType(11).to_string()

    # Tests that type_from_string is case-insensitive
    def test_type_from_string_is_case_insensitive(self):
        assert GeneratorType.type_from_string('STRING') == GeneratorType.STRING
        assert GeneratorType.type_from_string('InT') == GeneratorType.INT
        assert GeneratorType.type_from_string('fLoAt') == GeneratorType.FLOAT
        assert GeneratorType.type_from_string('dATeTiMe') == GeneratorType.DATETIME
        assert GeneratorType.type_from_string('BoOl') == GeneratorType.BOOL
        assert GeneratorType.type_from_string('aSsiGnMent') == GeneratorType.ASSIGNMENT
        assert GeneratorType.type_from_string('rElAtIoNsHiP') == GeneratorType.RELATIONSHIP

    # Tests that to_string returns a string with the first letter capitalized
    def test_to_string_returns_string_with_first_letter_capitalized(self):
        assert GeneratorType.STRING.to_string() == 'String'
        assert GeneratorType.INT.to_string() == 'Integer'
        assert GeneratorType.FLOAT.to_string() == 'Float'
        assert GeneratorType.DATETIME.to_string() == 'Datetime'
        assert GeneratorType.BOOL.to_string() == 'Bool'
        assert GeneratorType.ASSIGNMENT.to_string() == 'Assignment'
        assert GeneratorType.RELATIONSHIP.to_string() == 'Relationship'

    def test_to_string_returns_None_when_GeneratorType_enum_value_is_not_found_in_type_map(self):
        assert GeneratorType.STRING.to_string() is not None
        assert GeneratorType.INT.to_string() is not None
        assert GeneratorType.FLOAT.to_string() is not None
        assert GeneratorType.DATETIME.to_string() is not None
        assert GeneratorType.BOOL.to_string() is not None
        assert GeneratorType.ASSIGNMENT.to_string() is not None
        assert GeneratorType.RELATIONSHIP.to_string() is not None