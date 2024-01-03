import pytest

from pyparamvalidate import ParameterValidator, ParameterValidationError


def test_is_string_validator():
    @ParameterValidator("param").is_string("Value must be a string")
    def example_function(param):
        return param

    assert example_function(param="test") == "test"

    with pytest.raises(ParameterValidationError) as exc_info:
        example_function(param=123)
    assert "Value must be a string" in str(exc_info.value)


def test_is_int_validator():
    @ParameterValidator("param").is_int("Value must be an integer")
    def example_function(param):
        return param

    assert example_function(param=123) == 123

    with pytest.raises(ParameterValidationError) as exc_info:
        example_function(param="test")
    assert "Value must be an integer" in str(exc_info.value)


def test_is_positive_validator():
    @ParameterValidator("param").is_positive("Value must be positive")
    def example_function(param):
        return param

    assert example_function(param=5) == 5

    with pytest.raises(ParameterValidationError) as exc_info:
        example_function(param=-3)
    assert "Value must be positive" in str(exc_info.value)


def test_is_float_validator():
    @ParameterValidator("param").is_float("Value must be a float")
    def example_function(param):
        return param

    assert example_function(param=3.14) == 3.14

    with pytest.raises(ParameterValidationError) as exc_info:
        example_function(param="test")
    assert "Value must be a float" in str(exc_info.value)


def test_is_list_validator():
    @ParameterValidator("param").is_list("Value must be a list")
    def example_function(param):
        return param

    assert example_function(param=[1, 2, 3]) == [1, 2, 3]

    with pytest.raises(ParameterValidationError) as exc_info:
        example_function(param="test")
    assert "Value must be a list" in str(exc_info.value)


def test_is_dict_validator():
    @ParameterValidator("param").is_dict("Value must be a dictionary")
    def example_function(param):
        return param

    assert example_function(param={"key": "value"}) == {"key": "value"}

    with pytest.raises(ParameterValidationError) as exc_info:
        example_function(param=[1, 2, 3])
    assert "Value must be a dictionary" in str(exc_info.value)


def test_is_set_validator():
    @ParameterValidator("param").is_set("Value must be a set")
    def example_function(param):
        return param

    assert example_function(param={1, 2, 3}) == {1, 2, 3}

    with pytest.raises(ParameterValidationError) as exc_info:
        example_function(param="test")
    assert "Value must be a set" in str(exc_info.value)


def test_is_tuple_validator():
    @ParameterValidator("param").is_tuple("Value must be a tuple")
    def example_function(param):
        return param

    assert example_function(param=(1, 2, 3)) == (1, 2, 3)

    with pytest.raises(ParameterValidationError) as exc_info:
        example_function(param="test")
    assert "Value must be a tuple" in str(exc_info.value)


def test_is_not_none_validator():
    @ParameterValidator("param").is_not_none("Value must not be None")
    def example_function(param):
        return param

    assert example_function(param="test") == "test"

    with pytest.raises(ParameterValidationError) as exc_info:
        example_function(param=None)
    assert "Value must not be None" in str(exc_info.value)


def test_is_not_empty_validator():
    @ParameterValidator("param").is_not_empty("Value must not be empty")
    def example_function(param):
        return param

    assert example_function(param="test") == "test"

    with pytest.raises(ParameterValidationError) as exc_info:
        example_function(param="")
    assert "Value must not be empty" in str(exc_info.value)


def test_max_length_validator():
    @ParameterValidator("param").max_length(5, "Value must have max length of 5")
    def example_function(param):
        return param

    assert example_function(param="test") == "test"

    with pytest.raises(ParameterValidationError) as exc_info:
        example_function(param="toolongtext")
    assert "Value must have max length of 5" in str(exc_info.value)


def test_min_length_validator():
    @ParameterValidator("param").min_length(5, "Value must have min length of 5")
    def example_function(param):
        return param

    assert example_function(param="toolongtext") == "toolongtext"

    with pytest.raises(ParameterValidationError) as exc_info:
        example_function(param="test")
    assert "Value must have min length of 5" in str(exc_info.value)


def test_is_substring_validator():
    @ParameterValidator("param").is_substring("superstring", "Value must be a substring")
    def example_function(param):
        return param

    assert example_function(param="string") == "string"

    with pytest.raises(ParameterValidationError) as exc_info:
        example_function(param="test")
    assert "Value must be a substring" in str(exc_info.value)


def test_is_subset_validator():
    @ParameterValidator("param").is_subset({1, 2, 3}, "Value must be a subset")
    def example_function(param):
        return param

    assert example_function(param={1, 2}) == {1, 2}

    with pytest.raises(ParameterValidationError) as exc_info:
        example_function(param={4, 5})
    assert "Value must be a subset" in str(exc_info.value)


def test_is_sublist_validator():
    @ParameterValidator("param").is_sublist([1, 2, 3], "Value must be a sub-list")
    def example_function(param):
        return param

    assert example_function(param=[1, 2]) == [1, 2]

    with pytest.raises(ParameterValidationError) as exc_info:
        example_function(param=[1, 2, 3, 4, 5])
    assert "Value must be a sub-list" in str(exc_info.value)


def test_contains_substring_validator():
    @ParameterValidator("param").contains_substring("substring", "Value must contain substring")
    def example_function(param):
        return param

    assert example_function(param="This is a substring") == "This is a substring"

    with pytest.raises(ParameterValidationError) as exc_info:
        example_function(param="test")
    assert "Value must contain substring" in str(exc_info.value)


def test_contains_subset_validator():
    @ParameterValidator("param").contains_subset({1, 2, 3}, "Value must contain a subset")
    def example_function(param):
        return param

    assert example_function(param={1, 2, 3, 4, 5}) == {1, 2, 3, 4, 5}

    with pytest.raises(ParameterValidationError) as exc_info:
        example_function(param={4, 5})
    assert "Value must contain a subset" in str(exc_info.value)


def test_contains_sublist_validator():
    @ParameterValidator("param").contains_sublist([1, 2, 3], "Value must contain a sub-list")
    def example_function(param):
        return param

    assert example_function(param=[1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]

    with pytest.raises(ParameterValidationError) as exc_info:
        example_function(param=[4, 5])
    assert "Value must contain a sub-list" in str(exc_info.value)


def test_is_file_suffix_validator():
    @ParameterValidator("param").is_file_suffix(".txt", "Value must have .txt suffix")
    def example_function(param):
        return param

    assert example_function(param="example.txt") == "example.txt"

    with pytest.raises(ParameterValidationError) as exc_info:
        example_function(param="example.jpg")
    assert "Value must have .txt suffix" in str(exc_info.value)


def test_is_method_validator():
    def method():
        ...

    @ParameterValidator("param").is_method("Value must be a callable method")
    def example_function(param):
        return param

    assert example_function(param=method)

    with pytest.raises(ParameterValidationError) as exc_info:
        example_function(param="not a method")
    assert "Value must be a callable method" in str(exc_info.value)


def test_custom_validator():
    def custom_check(value):
        return value % 2 == 0

    @ParameterValidator("param").custom_validator(custom_check, "Value must be an even number")
    def example_function(param):
        return param

    assert example_function(param=4) == 4

    with pytest.raises(ParameterValidationError) as exc_info:
        example_function(param=5)
    assert "Value must be an even number" in str(exc_info.value)


def test_multiple_custom_validators():
    def custom_check_1(value):
        return value % 2 == 0

    def custom_check_2(value):
        return value > 0

    @ParameterValidator("param").custom_validator(custom_check_1, "Value must be an even number").custom_validator(
        custom_check_2, "Value must be a positive number")
    def example_function(param):
        return param

    assert example_function(param=4) == 4

    with pytest.raises(ParameterValidationError) as exc_info:
        example_function(param=5)
    assert "Value must be an even number" in str(exc_info.value)

    with pytest.raises(ParameterValidationError) as exc_info:
        example_function(param=-2)
    assert "Value must be a positive number" in str(exc_info.value)


def test_complex_validator():
    @ParameterValidator("name").is_string("Name must be a string").is_not_empty("Name cannot be empty")
    @ParameterValidator("age").is_int("Age must be an integer").is_positive("Age must be a positive number")
    @ParameterValidator("gender").is_allowed_value(["male", "female"], "Gender must be either 'male' or 'female'")
    @ParameterValidator("description").is_string("Description must be a string").is_not_empty(
        "Description cannot be empty")
    def example_function(name, age, gender='male', **kwargs):
        description = kwargs.get("description")
        return name, age, gender, description

    # 正向测试用例
    result = example_function(name="John", age=25, gender="male", description="A person")
    assert result == ("John", 25, "male", "A person")

    # 反向测试用例：测试 name 不是字符串的情况
    with pytest.raises(ParameterValidationError) as exc_info:
        example_function(name=123, age=25, gender="male", description="A person")
    assert "Name must be a string" in str(exc_info.value)

    # 反向测试用例：测试 age 不是正整数的情况
    with pytest.raises(ParameterValidationError) as exc_info:
        example_function(name="John", age="25", gender="male", description="A person")
    assert "Age must be an integer" in str(exc_info.value)

    # 反向测试用例：测试 gender 不是预定义值的情况
    with pytest.raises(ParameterValidationError) as exc_info:
        example_function(name="John", age=25, gender="other", description="A person")
    assert "Gender must be either 'male' or 'female'" in str(exc_info.value)

    # 反向测试用例：测试 description 不是字符串的情况
    with pytest.raises(ParameterValidationError) as exc_info:
        example_function(name="John", age=25, gender="male", description=123)
    assert "Description must be a string" in str(exc_info.value)

    # 反向测试用例：测试 description 是空字符串的情况
    with pytest.raises(ParameterValidationError) as exc_info:
        example_function(name="John", age=25, gender="male", description="")
    assert "Description cannot be empty" in str(exc_info.value)
