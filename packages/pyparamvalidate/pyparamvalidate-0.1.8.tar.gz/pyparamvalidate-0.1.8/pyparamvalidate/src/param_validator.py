import functools
import inspect


class ParameterValidationError(Exception):

    def __init__(self, func, parameter_name, parameter_value, param_rule_description=None, exception_msg=None):
        self.func_name = func.__name__
        self.parameter_name = parameter_name
        self.parameter_value = parameter_value
        self.param_rule_description = param_rule_description
        self.exception_msg = exception_msg

        super().__init__(self.error_message())

    def error_message(self):
        return (
            f"Parameter '{self.parameter_name}' in function '{self.func_name}' is invalid. "
            f"\t{'Error: ' + self.exception_msg if self.exception_msg else ''}"
            f"\t{'Please refer to: ' + self.param_rule_description if self.param_rule_description else ''}"
        )


class ParameterValidator:
    def __init__(self, param_name, param_rule_description=None):
        self.param_name = param_name
        self.param_rule_description = param_rule_description
        self.validators = []
        self.func_name = None

    def add_validator(self, validator_function, exception_msg=None):
        self.validators.append((validator_function, exception_msg))
        return self

    def is_string(self, exception_msg=None):
        return self.add_validator(lambda value: isinstance(value, str), exception_msg)

    def is_int(self, exception_msg=None):
        return self.add_validator(lambda value: isinstance(value, int), exception_msg)

    def is_positive(self, exception_msg=None):
        return self.add_validator(lambda value: value > 0, exception_msg)

    def is_float(self, exception_msg=None):
        return self.add_validator(lambda value: isinstance(value, float), exception_msg)

    def is_list(self, exception_msg=None):
        return self.add_validator(lambda value: isinstance(value, list), exception_msg)

    def is_dict(self, exception_msg=None):
        return self.add_validator(lambda value: isinstance(value, dict), exception_msg)

    def is_set(self, exception_msg=None):
        return self.add_validator(lambda value: isinstance(value, set), exception_msg)

    def is_tuple(self, exception_msg=None):
        return self.add_validator(lambda value: isinstance(value, tuple), exception_msg)

    def is_not_none(self, exception_msg=None):
        return self.add_validator(lambda value: value is not None, exception_msg)

    def is_not_empty(self, exception_msg=None):
        return self.add_validator(lambda value: bool(value), exception_msg)

    def is_allowed_value(self, allowed_values, exception_msg=None):
        return self.add_validator(lambda value: value in allowed_values, exception_msg)

    def max_length(self, max_length, exception_msg=None):
        return self.add_validator(lambda value: len(value) <= max_length, exception_msg)

    def min_length(self, min_length, exception_msg=None):
        return self.add_validator(lambda value: len(value) >= min_length, exception_msg)

    def is_substring(self, super_string, exception_msg=None):
        return self.add_validator(lambda value: value in super_string, exception_msg)

    def is_subset(self, superset, exception_msg=None):
        return self.add_validator(lambda value: value.issubset(superset), exception_msg)

    def is_sublist(self, super_list, exception_msg=None):
        return self.add_validator(lambda value: set(value).issubset(set(super_list)), exception_msg)

    def contains_substring(self, substring, exception_msg=None):
        return self.add_validator(lambda value: substring in value, exception_msg)

    def contains_subset(self, subset, exception_msg=None):
        return self.add_validator(lambda value: subset.issubset(value), exception_msg)

    def contains_sublist(self, sublist, exception_msg=None):
        return self.add_validator(lambda value: set(sublist).issubset(set(value)), exception_msg)

    def is_file_suffix(self, file_suffix, exception_msg=None):
        return self.add_validator(lambda value: value.endswith(file_suffix), exception_msg)

    def is_method(self, exception_msg=None):
        def method_check(value):
            return callable(value)

        return self.add_validator(method_check, exception_msg)

    def custom_validator(self, validator_function, exception_msg=None):
        return self.add_validator(validator_function, exception_msg)

    def __call__(self, func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)

            if self.param_name in kwargs:
                value = kwargs[self.param_name]
            elif self.param_name in bound_args.arguments:
                value = bound_args.arguments.get(self.param_name)
            else:
                return func(*args, **kwargs)

            for validator, exception_msg in self.validators:
                if not validator(value):
                    raise ParameterValidationError(func, self.param_name, value,
                                                   self.param_rule_description, exception_msg)

            return func(*args, **kwargs)

        return wrapper
