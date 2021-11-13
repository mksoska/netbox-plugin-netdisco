def cast(cls, super, model):
        if isinstance(model, super):
                model.__class__ = cls
        return model

def list_cast(cls, models):
        return [cls(model) for model in models]