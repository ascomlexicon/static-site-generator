from enum import Enum

class TextType(Enum):
    """
    Holds the different types of inline text formatting within a Markdown
    document.
    """

    NORMAL: str = "normal"
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
