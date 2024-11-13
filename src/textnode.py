"""
This modules contains classes that represent inline Markdown elements.

The TextType class is an Enum that stores the different Markdown formatting
styles/inline elements.

TextNode is a class that holds information about a chunk of Markdown.

In addition, there is a function to convert a TextNode to a LeafNode called
`text_node_to_html_node`.
"""
from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    """
    Holds the different types of inline text formatting within a Markdown
    document.
    """
    TEXT: str = "text"
    BOLD: str = "bold"
    ITALIC: str = "italic"
    CODE: str = "code"
    LINK: str = "link"
    IMAGE: str = "image"
    
class TextNode:
    """
    Holds information about a block of text within a Markdown document.
    """

    def __init__(self, text: str, text_type: TextType, url: str = None) -> None:
        """
        Instantiates a TextNode object.

        :param text: The text content of the node.
        :param text_type: The formatting style of the text.
        :param url: The URL of a link or image. By default, it is set to None.
        """
        self.text = text
        self.text_type = text_type
        self.url = url
        
    def __eq__(self, other: "TextNode") -> bool:
        """
        Checks the equivalence of two text nodes.

        :param other: The TextNode being compared to.
        :return: A boolean on whether all the properties in both nodes match.
        """
        return (self.text == other.text) and (self.text_type == other.text_type) and (self.url == other.url) 
    
    def __repr__(self) -> str:
        """
        Returns the string representation of the TextNode.
        """
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    """
    Converts a Markdown text node to a HTML node (specifically a LeafNode).

    :param text_node: The TextNode containing Markdown.
    :return: A node representing the HTML of the TextNode.
    :raise: Exception if there the type is not in the TextType Enum.
    """
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"'{text_node.text_type}' is not a valid TextType value.")
