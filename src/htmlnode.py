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
