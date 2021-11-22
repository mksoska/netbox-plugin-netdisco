
def sum_consistent(models, consistent=True):
    return sum(1 for model in models if model.is_consistent == consistent)    


def merge_dicts(*args):
    result = {}
    for dict_ in args:
        result.update(dict_)
    return result


class AttributeMap():
    def __init__(self, map_, model):
        self.map_ = map_
        self.model = model
    
    def __call__(self, *args):
        return {self.map_[arg]: getattr(self.model, arg) for arg in args}
