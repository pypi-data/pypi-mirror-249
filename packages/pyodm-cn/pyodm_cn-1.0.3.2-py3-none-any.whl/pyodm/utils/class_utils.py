from pyodm.model.definition import Attribute, OneElement, ManyElements
from pyodm.utils.dict_utils import DictUtils


class ClassUtils:

    @staticmethod
    def filter(clazz, lambda_function) -> dict:
        return DictUtils.filter(vars(clazz), lambda_function)

        # return {key: value for key, value in vars(clazz).items() if lambda_function(key, value)}

    @staticmethod
    def attributes_name(clazz) -> list[str]:
        return list(ClassUtils.filter(clazz, lambda key, value: isinstance(value, Attribute)).keys())


    @staticmethod
    def elements_name(clazz) -> list[str]:
        def condition(key, value):
            return isinstance(value, OneElement) or isinstance(value, ManyElements)

        return list(ClassUtils.filter(clazz, condition).keys())

    @staticmethod
    def get(entity, key: str):
        return entity.__dict__.get(key)
