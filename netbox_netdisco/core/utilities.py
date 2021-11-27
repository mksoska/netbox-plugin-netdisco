
def sum_inconsistent(models):
    return sum(1 for model in models if not model.is_consistent)    


def merge_dicts(*args):
    result = {}
    for dict_ in args:
        result.update(dict_)
    return result


def get_orm(expression):
    return expression.replace('.', '__')


class AttributeResolve():
    def __init__(self, netdisco, netbox, attribute_map, attribute_verbose, netdisco_attr_convert, netbox_attr_convert):
        self.netdisco = netdisco
        self.netbox = netbox
        self.attribute_map = attribute_map
        self.attribute_verbose = attribute_verbose
        self.netdisco_attr_convert = netdisco_attr_convert
        self.netbox_attr_convert = netbox_attr_convert

    def getattr_netdisco(self, key):
        unmangled = key.rstrip('_')
        return self._getattr_generic("self.netdisco.", unmangled, self.netdisco_attr_convert.get(key, lambda x: x))

    def getattr_netbox(self, key):
        return self._getattr_generic("self.netbox.", self.attribute_map.get(key), self.netbox_attr_convert.get(key, lambda x: str(x)))

    def _getattr_generic(self, base, expression, convert):
        try:
            if expression:
                value = eval(base + expression)
            if value:
                return convert(value)
        except AttributeError:
            return None
        

    def getattr_verbose(self, key):
        verbose = self.attribute_verbose.get(key)
        return verbose if verbose else key.capitalize()

    def attr_consistent(self, key):
        return self.getattr_netdisco(key) == self.getattr_netbox(key)
