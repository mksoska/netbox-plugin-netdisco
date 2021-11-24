
def sum_consistent(models, consistent=True):
    return sum(1 for model in models if model.is_consistent == consistent)    


def merge_dicts(*args):
    result = {}
    for dict_ in args:
        result.update(dict_)
    return result


def get_filter(model, attribute_map, *args):
    return {attribute_map[arg]: getattr(model, arg) for arg in args}


class AttributeResolve():
    def __init__(self, netdisco, netbox, attribute_map, attribute_verbose, attribute_convert):
        self.netdisco = netdisco
        self.netbox = netbox
        self.attribute_map = attribute_map
        self.attribute_verbose = attribute_verbose
        self.attribute_convert = attribute_convert

    def getattr_netdisco(self, key):
        convert = self.attribute_convert.get(key, lambda x: x)     
        return convert(getattr(self.netdisco, key, None))

    def getattr_netbox(self, key):
        path = self.attribute_map.get(key)
        if not path:
            return
        dest = self.netbox
        for attr in path.split('__'):
            if not dest:
                return
            dest = getattr(dest, attr, None)
        return dest

    def getattr_verbose(self, key):
        verbose = self.attribute_verbose.get(key)
        return verbose if verbose else key.capitalize()

    def attr_consistent(self, key):
        return self.getattr_netdisco(key) == self.getattr_netbox(key)
