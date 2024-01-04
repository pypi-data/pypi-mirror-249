pyparamvalidate 是一个简单易用的函数参数验证器。它提供了各种内置验证器，支持自定义验证规则，有助于 python
开发人员轻松进行函数参数验证，提高代码的健壮性和可维护性。

# 安装

```bash
pip install pyparamvalidate
```

如果安装过程中提示 `Failed to build numpy` 错误：
> Failed to build numpy
>
> ERROR: Could not build wheels for numpy, which is required to install pyproject.toml-based projects

请先手动安装 numpy 库:

```
pip install numpy
```

# 使用示例

## 示例 1：无规则描述

```python
from pyparamvalidate import ParameterValidator, ParameterValidationError


@ParameterValidator("name").is_string().is_not_empty()
@ParameterValidator("age").is_int().is_positive()
@ParameterValidator("gender").is_allowed_value(["male", "female"])
@ParameterValidator("description").is_string().is_not_empty()
def example_function(name, age, gender='male', **kwargs):
    description = kwargs.get("description")
    return name, age, gender, description


result = example_function(name="John", age=25, gender="male", description="A person")
print(result)  # output: ('John', 25, 'male', 'A person')

try:
    example_function(name=123, age=25, gender="male", description="A person")
except ParameterValidationError as e:
    print(e)  # output: Parameter 'name' in function 'example_function' is invalid.
```

## 示例 2：在 ParameterValidator 实例化中描述规则

```python
from pyparamvalidate import ParameterValidator, ParameterValidationError


@ParameterValidator("name", param_rule_description="Name must be a string").is_string().is_not_empty()
@ParameterValidator("age", param_rule_description="Age must be a positive integer").is_int().is_positive()
@ParameterValidator("gender", param_rule_description="Gender must be either 'male' or 'female'").is_allowed_value(
    ["male", "female"])
@ParameterValidator("description", param_rule_description="Description must be a string").is_string().is_not_empty()
def example_function(name, age, gender='male', **kwargs):
    description = kwargs.get("description")
    return name, age, gender, description


result = example_function(name="John", age=25, gender="male", description="A person")
print(result)  # output: ('John', 25, 'male', 'A person')

try:
    example_function(name=123, age=25, gender="male", description="A person")
except ParameterValidationError as e:
    print(
        e)  # output: Parameter 'name' in function 'example_function' is invalid. 		Please refer to: Name must be a string
```

## 示例 3：在 验证器 中描述规则

```python
from pyparamvalidate import ParameterValidator, ParameterValidationError


@ParameterValidator("name").is_string("Name must be a string").is_not_empty("Name cannot be empty")
@ParameterValidator("age").is_int("Age must be an integer").is_positive("Age must be a positive number")
@ParameterValidator("gender").is_allowed_value(["male", "female"], "Gender must be either 'male' or 'female'")
@ParameterValidator("description").is_string("Description must be a string").is_not_empty(
    "Description cannot be empty")
def example_function(name, age, gender='male', **kwargs):
    description = kwargs.get("description")
    return name, age, gender, description


result = example_function(name="John", age=25, gender="male", description="A person")
print(result)  # output: ('John', 25, 'male', 'A person')

try:
    example_function(name=123, age=25, gender="male", description="A person")
except ParameterValidationError as e:
    print(e)  # Parameter 'name' in function 'example_function' is invalid. 	Error: Name must be a string
```

# 可用的验证器

- `is_string`：检查参数是否为字符串。
- `is_int`：检查参数是否为整数。
- `is_positive`：检查参数是否为正数。
- `is_float`：检查参数是否为浮点数。
- `is_list`：检查参数是否为列表。
- `is_dict`：检查参数是否为字典。
- `is_set`：检查参数是否为集合。
- `is_tuple`：检查参数是否为元组。
- `is_not_none`：检查参数是否不为None。
- `is_not_empty`：检查参数是否不为空（对于字符串、列表、字典、集合等）。
- `is_allowed_value`：检查参数是否在指定的允许值范围内。
- `max_length`：检查参数的长度是否不超过指定的最大值。
- `min_length`：检查参数的长度是否不小于指定的最小值。
- `is_substring`：检查参数是否为指定字符串的子串。
- `is_subset`：检查参数是否为指定集合的子集。
- `is_sublist`：检查参数是否为指定列表的子列表。
- `contains_substring`：检查参数是否包含指定字符串。
- `contains_subset`：检查参数是否包含指定集合。
- `contains_sublist`：检查参数是否包含指定列表。
- `is_file`：检查参数是否为有效的文件；
- `is_dir`：检查参数是否为有效的目录；
- `is_file_suffix`：检查参数是否以指定文件后缀结尾。
- `is_similar_dict`：检查参数是否与指定字典相似，如果key值相同，value类型相同，则判定为True，支持比对嵌套字典。
- `is_method`：检查参数是否为可调用的方法（函数）。

除了以上内置验证器外，还可以使用 `custom_validator` 方法添加自定义验证器。

# 自定义验证器

```python
from pyparamvalidate import ParameterValidator


def custom_check(value):
    return value % 2 == 0


@ParameterValidator("param").custom_validator(custom_check, "Value must be an even number")
def example_function(param):
    return param
```

## 更多使用方法

```python
from pyparamvalidate.tests import test_param_validator
```

`test_param_validator` 是 `ParameterValidator` 的测试文件，可点击 `test_param_validator` 参考更多使用方法。

## 许可证

本项目采用 MIT 许可证授权。

```
Copyright (c) 2018 The Python Packaging Authority

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```