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
