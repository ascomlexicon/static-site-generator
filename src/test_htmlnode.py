import unittest
from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    """
    Unit tests for HTMLNode
    """
    
    def test_instances(self) -> None:
        """
        Tests to check if the __repr__ dunder method is producing the expected
        output.
        """
        node1: HTMLNode = HTMLNode(tag="h1")
        node2: HTMLNode = HTMLNode(value="Hello")
        node3: HTMLNode = HTMLNode(children=[node1])
        node4: HTMLNode = HTMLNode(props={"href": "www.google.com"})
        
        self.assertEqual(repr(node1), "HTMLNode(h1, None, None, None)")
        self.assertEqual(repr(node2), "HTMLNode(None, Hello, None, None)")
        self.assertEqual(repr(node3), "HTMLNode(None, None, [HTMLNode(h1, None, None, None)], None)")
        self.assertEqual(repr(node4), "HTMLNode(None, None, None, {'href': 'www.google.com'})")
    
    def test_to_html(self) -> None:
        """
        Test to see if the `to_html` method raises an error.
        """
        node: HTMLNode = HTMLNode("a")
        
        self.assertRaises(NotImplementedError,node.to_html)

    def test_props_to_html(self) -> None:
        """
        Tests the different cases of the `props_to_html` method for the
        HTMLNode.
        """
        node_no_props: HTMLNode = HTMLNode()
        node_empty_prop: HTMLNode = HTMLNode(props={})
        node_single_prop: HTMLNode = HTMLNode(props={"href": "www.google.com"})
        node_many_props: HTMLNode = HTMLNode(
            props={
                "href": "www.google.com",
                "target": "_blank",
                "css": "styles.css"
            }
        )
        
        self.assertEqual(node_no_props.props_to_html(), "")
        self.assertEqual(node_empty_prop.props_to_html(), "")
        self.assertEqual(node_single_prop.props_to_html(), "href=\"www.google.com\"")
        self.assertEqual(
            node_many_props.props_to_html(), "href=\"www.google.com\" target=\"_blank\" css=\"styles.css\""
        )

class TestLeafNode(unittest.TestCase):
    """
    Unit tests for LeafNode
    """
    
    def test_to_html(self) -> None:
        """
        Tests for the LeafNode implementation of the `to_html` method.
        """
        node_no_value: LeafNode = LeafNode("h1", None)
        node_no_tag: LeafNode = LeafNode(None, "Hello World")
        node_basic_paragraph: LeafNode = LeafNode("p", "This is a paragraph of text.")
        node_basic_link: LeafNode = LeafNode("a", "Click me!", {"href": "https://www.google.com"})

        self.assertRaises(ValueError,node_no_value.to_html)
        self.assertEqual(node_no_tag.to_html(), "Hello World")
        self.assertEqual(node_basic_paragraph.to_html(), "<p>This is a paragraph of text.</p>")
        self.assertEqual(node_basic_link.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")
