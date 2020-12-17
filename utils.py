def get_or_none(model, **kwargs):
    """
    Returns model object if exists else None
    """
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None