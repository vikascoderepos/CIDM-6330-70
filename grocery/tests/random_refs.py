import uuid


def random_suffix():
    return uuid.uuid4().hex[:6]


def random_sku(name=""):
    return f"sku-{name}-{random_suffix()}"


def random_productref(name=""):
    return f"product-{name}-{random_suffix()}"


def random_itemid(name=""):
    return f"item-{name}-{random_suffix()}"