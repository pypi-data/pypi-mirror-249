import re
from pathlib import Path

import toml

PATTERN = re.compile(r"[^a-zA-Z ]_+")


class TOMLConfigDict:
    """
    Represents a dictionary-like configuration object for TOML configurations.

    :param config_dict: The input configuration dictionary.
    :type config_dict: dict
    :param depth: The depth to which the conversion should occur. Default is 5.
    :type depth: int
    """

    __slots__ = ["__dict__"]

    def __init__(self, config_dict: dict, depth: int = 5):
        """
        Initializes the TOMLConfigDict.

        :param config_dict: The input configuration dictionary.
        :type config_dict: dict
        :param depth: The depth to which the conversion should occur. Default is 5.
        :type depth: int
        """
        self.__dict__["__dict__"] = {}
        self._parse_toml(config_dict, depth)

    def _parse_toml(self, config_dict: dict, depth: int):
        """
        Parses the TOML configuration dictionary and converts it to TOMLConfigDict.

        :param config_dict: The input configuration dictionary.
        :type config_dict: dict
        :param depth: The depth to which the conversion should occur.
        :type depth: int
        """
        for key, value in config_dict.items():
            key = key.replace(" ", "_").replace("-", "_").rstrip("_")
            key = re.sub(PATTERN, "", key)
            if depth > 1 and isinstance(value, dict):
                self.__dict__["__dict__"][key] = TOMLConfigDict(value, depth=depth - 1)
            else:
                self.__dict__["__dict__"][key] = value

    def __setattr__(self, attr: str, value):
        """
        Sets a TOMLConfig attribute with the given value.

        :param attr: The attribute name.
        :type attr: str
        :param value: The value to set for the attribute.
        """
        if isinstance(value, dict):
            value = TOMLConfigDict(value)
        object.__setattr__(self, attr, value)

    def __getattr__(self, attr: str):
        """
        Gets a TOMLConfig attribute with the given name.

        :param attr: The attribute name.

        :return: The value associated with the attribute.

        :raises AttributeError: If the attribute is not found.
        """
        if attr in self.__dict__["__dict__"]:
            return self.__dict__["__dict__"][attr]
        raise AttributeError(f"'TOMLConfigDict' object has no attribute '{attr}'")

    def __getitem__(self, key):
        """
        Gets a TOMLConfig attribute with the given key.

        :param key: The key to retrieve.

        :return: The value associated with the key.

        :raises KeyError: If the key is not found.
        """
        return self.__dict__["__dict__"][key]

    def __dir__(self):
        """
        Returns a list of all keys in the TOMLConfigDict.

        :return: A list of attribute names.
        :rtype: list
        """
        return list(self.__dict__["__dict__"].keys())

    def __repr__(self):
        """
        Returns a string representation of the TOMLConfigDict.

        :return: A string representation of attribute names.
        :rtype: str
        """
        return str(self.__dict__["__dict__"])


class TOMLConfig:
    """
    Represents a configuration object for TOML configurations.

    :param filepath: The path to the TOML configuration file.
    :type filepath: Path
    :param depth: The depth to which the conversion should occur. Default is 5.
    :type depth: int
    """

    __slots__ = ["config"]

    def __init__(self, filepath: Path, depth: int = 5):
        """
        Initializes the TOMLConfig.

        :param filepath: The path to the TOML configuration file.
        :type filepath: Path
        :param depth: The depth to which the conversion should occur. Default is 5.
        :type depth: int
        """
        self.config = TOMLConfigDict({})
        with open(filepath, "r") as f:
            config_dict = toml.load(f)
            for key, value in config_dict.items():
                key = key.replace(" ", "_")
                key = re.sub(PATTERN, "", key)
                if depth > 1 and isinstance(value, dict):
                    setattr(
                        self.config,
                        key,
                        TOMLConfigDict(value, depth=depth - 1),
                    )
                else:
                    setattr(self.config, key, value)

    def __getattr__(self, attr: str):
        """
        Gets a TOMLConfig attribute with the given name.

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

    def __getitem__(self, key: str):
        """
        Gets a TOMLConfig attribute with the given key.

        :param key: The key to retrieve.

        :return: The value associated with the key.

        :raises KeyError: If the key is not found.
        """
        return self.config[key]

    def __dir__(self):
        """
        Returns a list of all keys in the TOMLConfig.

        :return: A list of attribute names.
        :rtype: list
        """
        return list(self.config.__dict__["__dict__"].keys())

    def __repr__(self):
        """
        Returns a string representation of the TOMLConfig.

        :return: A string representation of attribute names.
        :rtype: str
        """
        return str(self.config)
