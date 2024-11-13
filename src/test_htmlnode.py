import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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
    
    def test_instances(self) -> None:
        """
        Tests if the `__repr__` method returns the correct string represenation.
        """
        node_no_props: LeafNode = LeafNode("p", "Hello World")
        node_with_prop: LeafNode = LeafNode("p", "Hello World", {"style": "styles.css"})

        self.assertEqual(repr(node_no_props), "LeafNode(p, Hello World, None)")
        self.assertEqual(repr(node_with_prop), "LeafNode(p, Hello World, {'style': 'styles.css'})")
    
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


class TestParentNode(unittest.TestCase):
    """
    Unit tests for ParentNode
    """
    
    def test_instances(self) -> None:
        """
        Checks to see if the `__repr__` dunder method produces the correct string.
        """
        node_none_children: ParentNode = ParentNode("a", None)
        node_empty_children: ParentNode = ParentNode("a", [])
        node_leaf_children: ParentNode = ParentNode("a", [LeafNode("b", "C1"), LeafNode("p", "C2")])
        node_parent_children: ParentNode = ParentNode("a", [node_leaf_children, ParentNode("b", [LeafNode("p", "C3")])])

        self.assertEqual(repr(node_none_children), "ParentNode(a, None, None)")
        self.assertEqual(repr(node_empty_children), "ParentNode(a, [], None)")
        self.assertEqual(
            repr(node_leaf_children), "ParentNode(a, [LeafNode(b, C1, None), LeafNode(p, C2, None)], None)"
        )
        self.assertEqual(
            repr(node_parent_children),
            "ParentNode(a, [ParentNode(a, [LeafNode(b, C1, None), LeafNode(p, C2, None)], None), ParentNode(b, [LeafNode(p, C3, None)], None)], None)"
        )
        
    def test_to_html_exceptions(self) -> None:
        """
        Test to check the different exceptions for the `to_html` method.
        """
        node_no_tag: ParentNode = ParentNode(None, [LeafNode(None, "value")])
        node_no_children: ParentNode = ParentNode("a", None)
        node_empty_children: ParentNode = ParentNode("a", [])
        
        # Test for error messages
        with self.assertRaises(ValueError) as e_no_tag:
            node_no_tag.to_html()
        self.assertEqual(str(e_no_tag.exception), "This node has no tag!")
        
        with self.assertRaises(ValueError) as e_no_children:
            node_no_children.to_html()
        self.assertEqual(str(e_no_children.exception), "The ParentNode must have children.")

        with self.assertRaises(ValueError) as e_empty_children:
            node_empty_children.to_html()
        self.assertEqual(str(e_empty_children.exception), "The ParentNode must have children.")

    def test_to_html_cases(self) -> None:
        """
        A unit test to check different edge cases for the `to_html` method.
        """
        node_leaf_children: ParentNode = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ]
        )
        node_parent_children: ParentNode = ParentNode(
            "p",
            [
                LeafNode(None, "I really like "),
                ParentNode("b", [LeafNode("i", "bold-italic")]),
                LeafNode(None, " text.")
            ]
        )
        node_props: ParentNode = ParentNode(
            "a",
            [
                LeafNode(None, "The "),
                ParentNode("i", [ParentNode("b", [LeafNode(None, "Google")], {"style": "styles.css"})]),
                LeafNode(None, " Homepage")
            ],
            {
                "href": "www.google.com"
            }
        )
        
        self.assertEqual(
            node_leaf_children.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )
        self.assertEqual(
            node_leaf_children.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )
        self.assertEqual(
            node_parent_children.to_html(), "<p>I really like <b><i>bold-italic</i></b> text.</p>"
        )
        self.assertEqual(
            node_props.to_html(),
            "<a href=\"www.google.com\">The <i><b style=\"styles.css\">Google</b></i> Homepage</a>"
        )
 