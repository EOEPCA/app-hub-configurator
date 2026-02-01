import yaml


def read_yaml(path):
    return yaml.safe_load(path.read_text())


def get_slugs(config):
    return [p["definition"]["slug"] for p in config["profiles"]]