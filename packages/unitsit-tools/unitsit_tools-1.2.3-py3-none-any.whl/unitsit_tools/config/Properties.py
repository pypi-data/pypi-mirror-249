import re
from pathlib import Path


class PropertiesConfigDict:
    """
    A helper class for nested configurations.

    :param config_dict: The dictionary to convert to a ConfigDict.
    :type config_dict: dict
    :param depth: The depth limit for nested configurations.
    :type depth: int

    Attributes:
        __dict__ (dict): A dictionary containing the converted configuration.

    """

    __slots__ = ["__dict__"]

    def __init__(self, config_dict: dict, depth: int = 5):
        """
        Initializes the ConfigDict.

        :param config_dict: The dictionary to convert to a ConfigDict.
        :type config_dict: dict
        :param depth: The depth limit for nested configurations.
        :type depth: int

        """
        self.__dict__["__dict__"] = {}
        self._parse_properties(config_dict, depth)

    def _parse_properties(self, config_dict: dict, depth: int):
        for key, value in config_dict.items():
            key = re.sub(r"[^a-zA-Z0-9_]+", "", key)
            key = key.replace(" ", "_").replace("-", "_").rstrip("_")
            if depth > 1 and isinstance(value, dict):
                self.__dict__["__dict__"][key] = PropertiesConfigDict(
                    value, depth=depth - 1
                )
            else:
                self.__dict__["__dict__"][key] = value

    def __setattr__(self, attr: str, value):
        """
        Sets an attribute in the ConfigDict.

        :param attr: The attribute name.
        :type attr: str
        :param value: The value to set for the attribute.

        """
        if isinstance(value, dict):
            value = PropertiesConfigDict(value)
        object.__setattr__(self, attr, value)

    def __getattr__(self, attr: str):
        """
        Gets a property of the configuration.

        :param attr: The attribute name.

        :return: The value associated with the attribute.

        :raises AttributeError: If the attribute is not found in the configuration.

        """
        if attr in self.__dict__["__dict__"]:
            return self.__dict__["__dict__"][attr]
        raise AttributeError(f"'PropertiesConfigDict' object has no attribute '{attr}'")

    def __getitem__(self, key: str):
        """
        Gets a property of the configuration using indexing.

        :param key: The key to retrieve from the configuration.

        :return: The value associated with the key.

        :raises KeyError: If the key is not found in the configuration.

        """
        return self.__dict__["__dict__"][key]

    def __dir__(self):
        """
        Returns a list of all keys in the ConfigDict.

        :return: A list of attribute names.
        :rtype: list

        """
        return list(self.__dict__["__dict__"].keys())

    def __repr__(self):
        """
        Returns a string representation of the ConfigDict.

        :return: A string representation of attribute names.
        :rtype: str

        """
        return str(list(self.__dict__["__dict__"]))


class PropertiesConfig:
    """
    Reads and parses a configuration file in the properties format.

    :param filepath: The path to the properties configuration file.
    :type filepath: Path
    :param depth: The depth limit for nested configurations.
    :type depth: int

    Attributes:
        config (PropertiesConfigDict): The configuration data stored as a dictionary.

    :raises FileNotFoundError: If the specified file does not exist.
    :raises ValueError: If there is an issue parsing the configuration.

    """

    __slots__ = ["config"]

    def __init__(self, filepath: Path, depth: int = 5):
        """
        Initializes the PropertiesConfig.

        :param filepath: The path to the properties configuration file.
        :type filepath: Path
        :param depth: The depth limit for nested configurations.
        :type depth: int

        :raises FileNotFoundError: If the specified file does not exist.
        :raises ValueError: If there is an issue parsing the configuration.

        """
        self.config = PropertiesConfigDict({})
        properties: dict = {}
        with open(filepath, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                key_value_match = re.match(r"^\s*([^=\s]+)\s*=\s*(.*)$", line)
                if key_value_match:
                    key, value = map(str.strip, key_value_match.groups())
                    keys = (
                        key.replace(" ", "_").replace("-", "_").rstrip("_").split(".")
                    )
                    current_dict = properties

                    for k in keys[:-1]:
                        if "[" in k:
                            match = re.match(r"(.+)\[(\d+)]", k)
                            if not match:
                                continue
                            list_key, index = match.groups()
                            index = int(index)
                            current_dict = current_dict.setdefault(
                                list_key, [{}] * (index + 1)
                            )
                            current_dict = current_dict[index]
                        else:
                            current_dict = current_dict.setdefault(k, {})

                    if keys[-1].startswith("'") and keys[-1].endswith("'"):
                        current_dict[keys[-1][1:-1]] = value
                    else:
                        current_dict[keys[-1]] = value

        if not properties:
            raise ValueError("The provided file does not contain valid properties.")

        self.config = PropertiesConfigDict(properties, depth=depth)

    def __getattr__(self, attr: str):
        """
        Gets a property of the configuration.

        :param attr: The attribute name.

        :return: The value associated with the attribute.

        :raises AttributeError: If the attribute is not found in the configuration.

        """
        try:
            return getattr(self.config, attr)
        except AttributeError as e:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{attr}'"
            ) from e

    def __getitem__(self, key: str):
        """
        Gets a property of the configuration using indexing.

        :param key: The key to retrieve from the configuration.

        :return: The value associated with the key.

        :raises KeyError: If the key is not found in the configuration.

        """
        return self.config[key]

    def __dir__(self):
        """
        Returns a list of all keys in the configuration.

        :return: A list of attribute names.
        :rtype: list

        """
        return list(self.__dict__.keys())

    def __repr__(self):
        """
        Returns a string representation of the configuration.

        :return: A string representation of attribute names.
        :rtype: str

        """
        return str(self.config.__dict__)
