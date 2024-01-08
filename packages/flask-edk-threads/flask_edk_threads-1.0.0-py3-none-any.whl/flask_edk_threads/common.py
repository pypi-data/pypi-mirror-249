import importlib


def class_parser(class_info: str):
    clazz_info = class_info.split(".")
    return {
        "package": ".".join(clazz_info[0:len(clazz_info) - 1]),
        "class": clazz_info[len(clazz_info) - 1]
    }


def name(element): return element.attrib.get("name")


def criteria(element): return element.attrib.get("criteria")


def strategy(element): return element.attrib.get("strategy")


def new_instance(clazz_desc: str, *args, **kwargs):
    clazz_info = class_parser(clazz_desc)
    module = importlib.import_module(clazz_info.get("package"))
    clazz = getattr(module, clazz_info.get("class"))
    return clazz(*args, **kwargs)
