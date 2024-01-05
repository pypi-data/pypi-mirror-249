import json
import os
from collections.abc import Mapping
from jsonschema import validate
from pyaml_env import parse_config
from yaml import FullLoader, safe_dump
from typing import Optional, Iterator, Any

# from svh_utils.general import get_dir_extension, check_if_file_exist, get_filename
from pathutility import PathUtils as pu


class ConfigMeld(Mapping):
    """
    A class to load and manage configurations from JSON or YAML files.
    """

    def __init__(self, **attrs):
        """
        Initialize ConfigMeld with attributes.

        Args:
            **attrs: Arbitrary keyword arguments representing configuration attributes.
        """
        for attr_name, attr_val in attrs.items():
            if isinstance(attr_val, dict):
                setattr(self, attr_name, self.__class__(**attr_val))
            else:
                setattr(self, attr_name, attr_val)

    def __repr__(self):
        """
        Representation of the ConfigMeld object.
        """
        return str(self.__dict__)

    def __getattr__(self, item: str):
        """
        Get an attribute of the ConfigMeld object.

        Args:
            item (str): The attribute name.

        Returns:
            Any: The attribute value if found.

        Raises:
            AttributeError: If the attribute is not found.
        """
        if item in self.__dict__:
            return self.__dict__[item]
        else:
            raise AttributeError(f'{item} object not found')

    def __iter__(self) -> Iterator:
        """
        Iterate over the ConfigMeld object.

        Returns:
            Iterator: An iterator over the loaded configurations.
        """
        return iter(self.load_config_as_kwargs())

    def __len__(self) -> int:
        """
        Get the length of the ConfigMeld object.

        Returns:
            int: The number of configurations loaded.
        """
        return len(self.load_config_as_kwargs())

    def __getitem__(self, item):
        """
        Get a configuration item from the ConfigMeld object.

        Args:
            item: The item to retrieve.

        Returns:
            Any: The value of the requested item.

        Raises:
            AttributeError: If the item is not found.
        """
        return self.__getattr__(item)

    def get(self, item, default: Optional[Any] = None):
        """
        Get a configuration item from the ConfigMeld object.

        Args:
            item: The item to retrieve.
            default (Optional[Any]): The default value if the item is not found.

        Returns:
            Any: The value of the requested item or the default value.
        """
        try:
            return self.__getitem__(item)
        except AttributeError:
            return default

    @staticmethod
    def _read_file(path: str, **kwargs) -> dict:
        """
        Read configuration data from a file.

        Args:
            path (str): The path to the configuration file.
            **kwargs: Additional keyword arguments.

        Returns:
            dict: The configuration data loaded from the file.

        Raises:
            FileNotFoundError: If the file is not found.
            ValueError: If an unrecognized extension is encountered.
        """
        is_automl_file = lambda p: pu.get_filename(p) in ['MLTable', 'MLmodel']

        if pu.is_file_exists(path):
            ext = pu.get_file_extension(path)
            if ext == '.json':
                return ConfigMeld._read_json(path, **kwargs)
            elif ext == '.yml':
                return ConfigMeld._read_yaml(path, **kwargs)
            elif is_automl_file(path):
                return ConfigMeld._read_yaml(path, **kwargs)
            else:
                raise ValueError(f'Unrecognized {ext} extension')
        else:
            raise FileNotFoundError(f'File {path} not found')

    @staticmethod
    def _read_yaml(path: str, **kwargs) -> dict:
        """
        Read YAML configuration data from a file.

        Args:
            path (str): The path to the YAML configuration file.
            **kwargs: Additional keyword arguments.

        Returns:
            dict: The YAML configuration data loaded from the file.
        """
        return parse_config(path=path, loader=FullLoader, **kwargs)

    @staticmethod
    def _read_json(path: str, **kwargs) -> dict:
        """
        Read JSON configuration data from a file.

        Args:
            path (str): The path to the JSON configuration file.
            **kwargs: Additional keyword arguments.

        Returns:
            dict: The JSON configuration data loaded from the file.
        """
        with open(path, **kwargs) as f:
            json_data = json.load(f)
        return json_data

    @classmethod
    def load_config_from_file(
            cls,
            path: str,
            schema_validator: Optional[str] = None,
            **kwargs
    ) -> 'ConfigMeld':
        """
        Load configuration from a file.

        Args:
            path (str): The path to the configuration file.
            schema_validator (Optional[str]): The path to the schema validator file.
            **kwargs: Additional keyword arguments.

        Returns:
            ConfigMeld: A ConfigMeld instance with loaded configurations.

        Raises:
            FileNotFoundError: If the file is not found.
            ValueError: If an unrecognized extension is encountered.
        """
        config_data = cls._read_file(path, **kwargs)

        if schema_validator is not None:
            schema = cls._read_file(schema_validator)
            validate(config_data, schema)

        return cls(**config_data)

    def load_config_as_environ_vars(self) -> None:
        """
        Load configurations as environment variables.
        """
        for key, value in self.__dict__.items():
            if isinstance(value, ConfigMeld):
                os.environ[key] = str(value.load_config_as_kwargs())
            else:
                os.environ[key] = str(value)

    def load_config_as_string(self) -> str:
        """
        Load configurations as a string.

        Returns:
            str: Configurations represented as a string.
        """
        return safe_dump(self.load_config_as_kwargs())

    def load_config_as_kwargs(self) -> dict:
        """
        Load configurations as keyword arguments.

        Returns:
            dict: Configurations represented as keyword arguments.
        """
        return {
            k: v.load_config_as_kwargs() if isinstance(v, ConfigMeld)
            else v for k, v in self.__dict__.items()
        }

    def generate_schema(self) -> dict:
        """
        Generate a JSON schema based on existing configurations.

        Returns:
            dict: The generated JSON schema.
        """
        schema = {}
        for key, value in self.load_config_as_kwargs().items():
            if isinstance(value, ConfigMeld):
                schema[key] = value.generate_schema()
            elif isinstance(value, list) and value:
                # If it's a non-empty list, create a schema for its elements
                elem = value[0] if len(value) > 0 else None
                if isinstance(elem, ConfigMeld):
                    schema[key] = [elem.generate_schema()]
                else:
                    schema[key] = {
                        "type": "array",
                        "items": {"type": type(elem).__name__}
                    }
            elif isinstance(value, dict):
                # Handle nested dictionaries
                inner_schema = {}
                for k, v in value.items():
                    inner_schema[k] = {"type": type(v).__name__}
                schema[key] = {"type": "object", "properties": inner_schema}
            else:
                schema[key] = {"type": type(value).__name__}
        return schema

    