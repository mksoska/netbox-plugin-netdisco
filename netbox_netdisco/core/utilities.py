
def is_consistent(model):
    # Maybe lowercase if attribute is a string
    for key in model.attribute_map:
        netdisco = model.netdisco
        for attr in key.split('__'):
            netdisco = getattr(netdisco, attr)
        
        netbox = model.netbox
        for attr in model.attribute_map[key].split('__'):
            netbox = getattr(netbox, attr)

        if netdisco != netbox:
            return False
    return True


def sum_consistent(models, consistent=True):
    return sum(1 for model in models if model.is_consistent == consistent)    




