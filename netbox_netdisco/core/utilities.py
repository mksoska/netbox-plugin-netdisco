
def is_consistent(attribute_map, netdisco_model, netbox_model):
    # Maybe lowercase if attribute is a string
    for key in attribute_map:
        netdisco = netdisco_model
        for attr in key.split('__'):
            netdisco = getattr(netdisco, attr)
        
        netbox = netbox_model
        for attr in attribute_map[key].split('__'):
            netbox = getattr(netbox, attr)

        if netdisco != netbox:
            return False
    return True


def sum_consistent(models, consistent=True):
    return sum(1 for model in models if model.is_consistent == consistent)    




