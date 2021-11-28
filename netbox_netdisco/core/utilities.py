
def sum_inconsistent(models):
    return sum(1 for model in models if not model.is_consistent)    


def merge_dicts(*args):
    result = {}
    for dict_ in args:
        result.update(dict_)
    return result


def get_orm(orm_map, model_netdisco, queryset):
    query = {orm_map[key]: getattr(model_netdisco, key) for key in orm_map} if orm_map else None
    return queryset.filter(**query).first() if query else None


class AttributeResolve():
    def __init__(self, netdisco, netbox, attribute_map, netdisco_attr_convert, netbox_attr_convert, verbose_name):
        self.netdisco = netdisco
        self.netbox = netbox
        self.attribute_map = attribute_map
        self.netdisco_attr_convert = netdisco_attr_convert
        self.netbox_attr_convert = netbox_attr_convert
        self.verbose_name = verbose_name

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
        verbose = self.verbose_name.get(key)
        return verbose if verbose else key.capitalize()

    def attr_consistent(self, key):
        return self.getattr_netdisco(key) == self.getattr_netbox(key)
