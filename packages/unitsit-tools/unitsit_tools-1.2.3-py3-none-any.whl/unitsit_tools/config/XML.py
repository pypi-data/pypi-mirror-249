from collections import namedtuple
from pathlib import Path
from xml.etree.ElementTree import fromstring, Element, parse


class XMLConfig:
    """
    Represents an XML configuration object.

    This class parses an XML file and creates a configuration object with attributes based on the XML structure.
    The depth parameter controls how deep the parsing should go.
    """

    @classmethod
    def parse_from_xml_string(cls, xml_string: str, depth: int = 10):
        """
        Parses an XML string and creates an XMLConfig object.

        :param xml_string: The XML string to parse.
        :type xml_string: str
        :param depth: The depth to which the parsing should occur. Default is 10.
        :type depth: int

        :return: An instance of XMLConfig.
        :rtype: XMLConfig
        """
        root = fromstring(xml_string)
        return cls(root, depth)

    def __init__(self, source, depth: int = 10):
        """
        Initializes the XMLConfig.

        :param source: Either the path to the XML configuration file (Path object) or the XML Element.
        :type source: Union[Path, Element]
        :param depth: The depth to which the parsing should occur. Default is 10.
        :type depth: int

        :raises ValueError: If the source type is invalid. Use Path or Element.
        """
        if isinstance(source, Path):
            self.tree = parse(source)
            self.root = self.tree.getroot()
        elif isinstance(source, Element):
            self.root = source
        else:
            raise ValueError("Invalid source type. Use Path or Element.")

        self.filename = getattr(source, "name", None)
        self.depth = depth
        self.config = self._parse(self.root, depth)

    def __getattr__(self, attr: str):
        """
        Gets an attribute from the XMLConfig.

        :param attr: The attribute name.

        :return: The value associated with the attribute.

        :raises AttributeError: If the attribute is not found.
        """
        try:
            return getattr(self.config, attr)
        except AttributeError as e:
            raise AttributeError(str(e)) from e

    def _parse(self, elem, depth: int):
        """
        Recursively parses XML elements and creates a named tuple representing the XML structure.

        :param elem: The XML element to parse.
        :type elem: Element
        :param depth: The depth to which the parsing should occur.
        :type depth: int

        :return: A named tuple representing the XML structure.
        :rtype: NamedTuple
        """
        if depth == 0 or not list(elem):
            return elem.text.strip()
        else:
            return namedtuple(elem.tag, [child.tag for child in elem])(
                *[self._parse(child, depth - 1) for child in elem]
            )
