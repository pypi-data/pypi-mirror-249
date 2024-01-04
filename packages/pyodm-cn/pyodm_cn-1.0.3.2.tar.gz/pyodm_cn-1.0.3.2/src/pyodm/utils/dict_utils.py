class DictUtils:
    @staticmethod
    def filter(collection_dict: dict, lambda_condition):
        return {key: value for key, value in collection_dict.items() if lambda_condition(key, value)}