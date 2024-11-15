"""
This module contains classes that represent different types of HTML elements
dependent on whether they contain more HTML elements within them.

HTMLNode is an abstract class that has two children classes: LeafNode (for 
elements that do not have nested elements), and ParentNode (elements containing
nested elements).
"""

class HTMLNode:
    """
    Represents elements (with their contents) in a HTML document tree to render
    itself to HTML.
    """
    
    def __init__(
        self, tag: str = None,
        value: str = None,
        children: list["HTMLNode"] = None,
        props: dict[str, str] = None 
    ) -> None:
        """
        Instantiates a HTMLNode.

        :param tag: The HTML tag name of an element.
        :param value: The value of the HTML tag.
        :param children: Children of this HTMLNode.
        :param props: The key-value pairs attributes (and their values) of the HTML tag.
        """
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    def to_html(self) -> str:
        """
        Renders the HTML elements.

        :return: A string that holds the HTML to render the element.
        """
        raise NotImplementedError()
    
    def props_to_html(self) -> str:
        """
        Creates a string of the combined tag attributes.

        :return: A concatenated string of the attributes.
        """
        if self.props is None:
            return ""

        attributes = ""
        for k, v in self.props.items():
            if attributes:
                attributes += " "
            
            attributes += f"{k}=\"{v}\""
            
        return attributes
    
    def __repr__(self) -> str:
        """
        Generates a string representation of the HTMLNode.

        :return: The HTMLNode's string representation.
        """
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    """
    Represents elements with no other HTML tags within it; a HTMLNode without
    any children.
    """
    
    def __init__(self, tag: str, value: str, props: dict[str, str] = None) -> None:
        """
        Instantiates a LeafNode for a HTML element.
        
        :param tag: The HTML tag of the LeafNode.
        :param value: The value held within the LeafNode.
        :param props: Attribute information for the LeafNode tag.
        """
        super().__init__(tag=tag, value=value, props=props)
        
    def to_html(self) -> str:
        """
        Generates a string containing the HTML to render the element.
        
        :return: The HTML representation for the node.
        :raise ValueError: When there is no value, there is a ValueError.
        """
        if self.value is None:
            raise ValueError("Elements without children must have a value")
        
        if self.tag is None:
            return self.value
        
        tag_attr = "" if self.props is None else f" {self.props_to_html()}"
        
        return f"<{self.tag}{tag_attr}>{self.value}</{self.tag}>"
    
    def __repr__(self) -> str:
        """
        Returns the string representation for a LeafNode.

        :return: The LeafNode string representation.
        """
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    

class ParentNode(HTMLNode):
    """
    Represents elements that contain nested elements.
    """
    
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str, str] = None) -> None:
        """
        Instantiates a ParentNode.

        :param tag: The tag of the HTML element.
        :param children: A list of HTML elements nested within the ParentNode.
        :param props: Key-value pairs for attributes (with their values) for a HTML tag.
        """
        super().__init__(tag=tag, children=children, props=props)
        
    def to_html(self) -> str:
        """
        Converts a the ParentNode (along with its children) into HTML.
        The resulting string will be a single line (not pretty printed).

        :return: The string holding the rendered HTML.
        """
        if self.tag is None:
            raise ValueError("This node has no tag!")
        elif not self.children:
            raise ValueError("The ParentNode must have children.")
        
        html: str = f"<{self.tag}{'' if self.props is None else f' {self.props_to_html()}'}>"
        
        for child in self.children:
            html += child.to_html()

        html += f"</{self.tag}>"
        
        return html
    
    def __repr__(self) -> str:
        """
        Returns a string representation for a ParentNode.

        :return: ParentNode string representation.
        """
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
