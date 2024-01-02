import re
from pathlib import Path

import yaml

# Regular expression pattern for cleaning up keys
PATTERN = re.compile(r"[^a-zA-Z ]_+")


class YAMLConfigDict:
    """
    Represents a dictionary-like configuration object for YAML configurations.

    This class iterates over a given dictionary and converts it to a YAMLConfigDict.
    Each key in the original dictionary is converted to lowercase and set as a YAMLConfig attribute.
    If the value of a key is a dictionary, it is recursively converted to a YAMLConfigDict and set as a YAMLConfig
    attribute.

    :param config_dict: The input configuration dictionary.
    :type config_dict: dict
    :param depth: The depth to which the conversion should occur. Default is 5.
    :type depth: int
    """

    __slots__ = ["__dict__"]

    def __init__(self, config_dict, depth=5):
        """
        Initializes the YAMLConfigDict.

        :param config_dict: The input configuration dictionary.
        :type config_dict: dict
        :param depth: The depth to which the conversion should occur. Default is 5.
        :type depth: int
        """
        self.__dict__["__dict__"] = {}
        self._parse_yaml(config_dict, depth)

    def _parse_yaml(self, config_dict, depth):
        """
        Recursive method for parsing YAML configuration dictionaries.

        :param config_dict: The input configuration dictionary.
        :type config_dict: dict
        :param depth: The depth to which the conversion should occur.

        """
        for key, value in config_dict.items():
            key = key.replace(" ", "_")
            key = re.sub(PATTERN, "", key)
            if depth > 1 and isinstance(value, dict):
                self.__dict__["__dict__"][key] = YAMLConfigDict(value, depth=depth - 1)
            else:
                self.__dict__["__dict__"][key] = value

    def __setattr__(self, attr, value):
        """
        Set a YAMLConfig attribute with the value of the config_dict.

        :param attr: The attribute name.
        :type attr: str
        :param value: The value to be set.

        """
        if isinstance(value, dict):
            value = YAMLConfigDict(value)
        object.__setattr__(self, attr, value)

    def __getattr__(self, attr):
        """
        Get a YAMLConfig attribute with the value of the config_dict.

        :param attr: The attribute name.

        :return: The value associated with the attribute.

        :raises AttributeError: If the attribute is not found.

        """
        if attr in self.__dict__["__dict__"]:
            return self.__dict__["__dict__"][attr]
        raise AttributeError(f"'YAMLConfigDict' object has no attribute '{attr}'")

    def __getitem__(self, key):
        """
        Get a YAMLConfig attribute with the value of the config_dict.

        :param key: The attribute key.

        :return: The value associated with the key.

        """
        return self.__dict__["__dict__"][key]

    def __dir__(self):
        """
        Returns a list of all the keys in the config_dict.

        :return: A list of attribute names.
        :rtype: List[str]

        """
        return list(self.__dict__["__dict__"].keys())

    def __repr__(self):
        """
        Returns a string representation of the config_dict.

        :return: A string representation of the YAMLConfigDict.
        :rtype: str

        """
        return str(self.__dict__["__dict__"])


class YAMLConfig:
    """
    Represents a configuration object for YAML configurations.

    This class iterates over a given dictionary and converts it to a YAMLConfigDict.
    Each key in the original dictionary is converted to lowercase and set as a YAMLConfig attribute.
    If the value of a key is a dictionary, it is recursively converted to a YAMLConfigDict and set as a YAMLConfig
    attribute.

    :param filepath: The path to the YAML configuration file.
    :type filepath: Path
    :param depth: The depth to which the conversion should occur. Default is 5.
    :type depth: int
    """

    __slots__ = ["config"]

    def __init__(self, filepath: Path, depth=5):
        """
        Initializes the YAMLConfig.

        :param filepath: The path to the YAML configuration file.
        :type filepath: Path
        :param depth: The depth to which the conversion should occur. Default is 5.
        :type depth: int
        """
        self.config = YAMLConfigDict({})
        with open(filepath, "r") as f:
            config_dict = yaml.safe_load(f)
            for key, value in config_dict.items():
                key = key.replace(" ", "_")
                key = re.sub(PATTERN, "", key)
                if depth > 1 and isinstance(value, dict):
                    setattr(
                        self.config,
                        key,
                        YAMLConfigDict(value, depth=depth - 1),
                    )
                else:
                    setattr(self.config, key, value)

    def __getattr__(self, attr):
        """
        Get a YAMLConfig attribute with the value of the config_dict.

        :param attr: The attribute name.

        :return: The value associated with the attribute.

        :raises AttributeError: If the attribute is not found.

        """
        try:
            return getattr(self.config, attr)
        except AttributeError as e:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{attr}'"
            ) from e

    def __dir__(self):
        """
        Returns a list of all the keys in the config_dict.

        :return: A list of attribute names.
        :rtype: List[str]

        """
        return list(self.config.__dict__["__dict__"].keys())

    def __repr__(self):
        """
        Returns a string representation of the config_dict.

        :return: A string representation of the YAMLConfig.
        :rtype: str

        """
        return str(self.config)
