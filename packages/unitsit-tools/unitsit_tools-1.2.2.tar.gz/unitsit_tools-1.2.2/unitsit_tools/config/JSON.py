import json
import re
from pathlib import Path

# Regex to get only all alphanumeric and underscore characters
PATTERN = re.compile(r"[^a-zA-Z0-9 ]_+")


class JSONConfigDict:
    """
    Represents a dictionary-like configuration object for JSON configurations.

    This class iterates over a given dictionary and converts it to a JSONConfigDict.
    Each key in the original dictionary is converted to lowercase and set as a JSONConfig attribute.
    If the value of a key is a dictionary, it is recursively converted to a
    JSONConfigDict and set as a JSONConfig attribute.

    :param config_dict: The input configuration dictionary.
    :type config_dict: dict
    :param depth: The depth to which the conversion should occur. Default is 5.
    :type depth: int
    """

    __slots__ = ["__dict__"]

    def __init__(self, config_dict: dict, depth: int = 5):
        """
        Initialize the JSONConfigDict.

        :param config_dict: The input configuration dictionary.
        :type config_dict: dict
        :param depth: The depth to which the conversion should occur. Default is 5.
        :type depth: int
        """
        for key, value in config_dict.items():
            if depth > 1 and isinstance(value, dict):
                key = re.sub(PATTERN, "", key)
                self.__setattr__(
                    key.replace(" ", "_"),
                    JSONConfigDict(value, depth=depth - 1),
                )
            else:
                key = re.sub(PATTERN, "", key)
                self.__setattr__(key.replace(" ", "_"), value)

    def __setattr__(self, attr: str, value):
        """
        Set a JSONConfig attribute with the value of the config_dict.

        :param attr: The attribute name.
        :type attr: str
        :param value: The value to set for the attribute.
        """
        if isinstance(value, dict):
            value = JSONConfigDict(value)
        object.__setattr__(self, attr, value)

    def __dir__(self):
        """
        Return a list of all the keys in the config_dict.

        :return: A list of attribute names.
        :rtype: list
        """
        return list(self.__dict__.keys())

    def __repr__(self):
        """
        Return a string representation of the config_dict.

        :return: A string representation of attribute names.
        :rtype: str
        """
        return str(list(self.__dict__.keys()))


class JSONConfig:
    """
    Represents a configuration object for JSON configurations.

    This class iterates over a given dictionary and converts it to a JSONConfigDict.
    Each key in the original dictionary is converted to lowercase and set as a JSONConfig attribute.
    If the value of a key is a dictionary, it is recursively converted to a
    SONConfigDict and set as a JSONConfig attribute.

    :param filepath: The path to the JSON configuration file.
    :type filepath: Path
    :param depth: The depth to which the conversion should occur. Default is 5.
    :type depth: int
    """

    __slots__ = ["config", "__dict__"]

    def __init__(self, filepath: Path, depth: int = 5):
        """
        Initialize the JSONConfig.

        :param filepath: The path to the JSON configuration file.
        :type filepath: Path
        :param depth: The depth to which the conversion should occur. Default is 5.
        :type depth: int
        """
        self.config = {}
        with open(filepath, "r") as f:
            config_dict = json.load(f)
            for key, value in config_dict.items():
                if depth > 1 and isinstance(value, dict):
                    key = re.sub(PATTERN, "", key)
                    setattr(
                        self,
                        key.replace(" ", "_"),
                        JSONConfigDict(value, depth=depth - 1),
                    )
                else:
                    key = re.sub(PATTERN, "", key)
                    setattr(self, key.replace(" ", "_"), value)
                self.config[key] = getattr(self, key.replace(" ", "_"))

    def __getattr__(self, attr: str):
        """
        Get a JSONConfig attribute with the value of the config_dict.

        :param attr: The attribute name.
        :type attr: str

        :return: The value associated with the attribute.
        :rtype: Any

        :raises AttributeError: If the attribute is not found in the configuration.
        """
        try:
            return self.config[attr]
        except KeyError as e:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{attr}'"
            ) from e

    def __getitem__(self, key: str):
        """
        Get a JSONConfig attribute with the value of the config_dict.

        :param key: The key to retrieve from the configuration.
        :type key: str

        :return: The value associated with the key.
        :rtype: Any

        :raises KeyError: If the key is not found in the configuration.
        """
        return self.config[key]

    def __dir__(self):
        """
        Return a list of all the keys in the config_dict.

        :return: A list of attribute names.
        :rtype: list
        """
        return list(self.__dict__.keys())

    def __repr__(self):
        """
        Return a string representation of the config_dict.

        :return: A string representation of attribute names.
        :rtype: str
        """
        return str(list(self.__dict__.keys()))
