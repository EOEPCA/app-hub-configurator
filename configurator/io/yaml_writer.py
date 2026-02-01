from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString
from ruamel.yaml.representer import SafeRepresenter
from configurator.models import Config


def literalize_multiline_values(obj):
    """
    Recursively wrap multiline *values* as LiteralScalarString.
    NEVER touch dict keys.
    """
    if isinstance(obj, list):
        return [literalize_multiline_values(i) for i in obj]

    if isinstance(obj, dict):
        return {k: literalize_multiline_values(v) for k, v in obj.items()}

    if isinstance(obj, str) and "\n" in obj:
        return LiteralScalarString(obj)

    return obj


def write_yaml(config: Config, output: str) -> None:
    yaml_writer = YAML(typ="safe", pure=True)
    yaml_writer.default_flow_style = False
    # set the line width to a large value to avoid unwanted line breaks
    yaml_writer.width = 4096

    yaml_writer.representer.add_representer(
        LiteralScalarString,
        SafeRepresenter.represent_str,
    )

    # Dump FIRST
    data = config.model_dump(exclude_none=True, mode="json")

    # THEN wrap multiline strings
    data = literalize_multiline_values(data)

    with open(output, "w") as f:
        yaml_writer.dump(data, f)
