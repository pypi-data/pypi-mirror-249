from pathlib import Path
from typing import Union
import pytest
from pydantic import ValidationError


from roxbot.config import Config

yaml_file = Path(__file__).resolve().parent / "files" / "config.yml"


class MyConfig(Config):
    """example config class"""

    param_a: str = "foo"
    param_b: int = 42
    param_string: str = "default"
    param_float: float = 0.0
    param_bool: bool = False
    param_null: Union[None, str] = None
    # note: Pydantic internally handles default mutable types properly by creating
    #  a new instance of the mutable for each model instance. No need to use default_factory
    param_list: list = []
    param_dict: dict = {}


def test_creation():
    cfg = MyConfig()

    assert cfg.param_a == "foo"
    assert cfg.param_b == 42
    assert cfg.param_string == "default"
    assert cfg.param_float == 0.0
    assert cfg.param_bool is False
    assert cfg.param_null is None
    assert not cfg.param_list
    assert not cfg.param_dict


def test_mutables():
    """assigning mutable object as defaults should be handled correctly with default_factory"""
    cfg1 = MyConfig()
    cfg2 = MyConfig()

    cfg1.param_list.append(1)
    cfg2.param_list.append(2)

    assert cfg1.param_list == [1]
    assert cfg2.param_list == [2]


def test_from_yaml():
    cfg = MyConfig()
    cfg.from_yaml(yaml_file)

    assert cfg.param_a == "foo"
    assert cfg.param_b == 120
    assert cfg.param_string == "example string"
    assert cfg.param_float == 3.14
    assert cfg.param_bool is True
    assert cfg.param_null is None
    assert cfg.param_list == [1, 2, 3]
    assert cfg.param_dict == {"key1": "value1", "key2": "value2"}


def test_parameter_assign():
    with pytest.raises(ValidationError):
        MyConfig(param_bool=42)

    # test update of existing parameter
    cfg = MyConfig(param_a="bar")
    assert cfg.param_a == "bar"

    # test update of existing parameter with invalid value
    with pytest.raises(ValidationError):
        setattr(cfg, "param_a", 32)

    # direct assigning string instead of int should fail
    with pytest.raises(ValidationError):
        cfg.param_b = "bar"


def test_invalid_yaml_data():
    invalid_yaml_file = Path(__file__).resolve().parent / "files" / "invalid_config.yml"

    with pytest.raises(ValidationError):
        cfg = MyConfig()
        cfg.from_yaml(invalid_yaml_file)
