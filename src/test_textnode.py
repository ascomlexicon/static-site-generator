import unittest
from htmlnode import LeafNode
from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    """
    Unit tests for the TextNode object.
    """
    
    def test_equality(self) -> None:
        """
        Tests to check if the equality operator is functioning correctly.
        """
        control_node: TextNode = TextNode("test string", TextType.CODE, "www.google.com")
        
        same_node: TextNode = TextNode("test string", TextType.CODE, "www.google.com")
        diff_text: TextNode = TextNode("Test string", TextType.CODE, "www.google.com")
        diff_format: TextNode = TextNode("test string", TextType.BOLD, "www.google.com")
        diff_url: TextNode = TextNode("test string", TextType.CODE, "www.youtu.be")
        no_url: TextNode = TextNode("test string", TextType.CODE)
        
        self.assertEqual(control_node, same_node)
        self.assertNotEqual(control_node, diff_text)
        self.assertNotEqual(control_node, diff_format)
        self.assertNotEqual(control_node, diff_url)
        self.assertNotEqual(control_node, no_url)
        
    def test_text_to_html(self) -> None:
        """
        Tests to see if TextNodes convert correctly to LeafNodes.
        """
        normal_text: TextNode = TextNode("test", TextType.TEXT)
        bold_text: TextNode = TextNode("test", TextType.BOLD)
        italic_text: TextNode = TextNode("test", TextType.ITALIC)
        code_text: TextNode = TextNode("test", TextType.CODE)
        link: TextNode = TextNode("this is a link", TextType.LINK, "www.google.com")
        image: TextNode = TextNode("this is an image", TextType.IMAGE, "www.image.com")
        fake_node: TextNode = TextNode("This should not work", "fake")
        
        self.assertRaises(ValueError, text_node_to_html_node, fake_node)
        self.assertEqual(
            repr(text_node_to_html_node(normal_text)),
            "LeafNode(None, test, None)"
        )
        self.assertEqual(
            repr(text_node_to_html_node(bold_text)),
            "LeafNode(b, test, None)"
        )
        self.assertEqual(
            repr(text_node_to_html_node(italic_text)),
            "LeafNode(i, test, None)"
        )
        self.assertEqual(
            repr(text_node_to_html_node(code_text)),
            "LeafNode(code, test, None)"
        )
        self.assertEqual(
            repr(text_node_to_html_node(link)),
            "LeafNode(a, this is a link, {'href': 'www.google.com'})"
        )
        self.assertEqual(
            repr(text_node_to_html_node(image)),
            "LeafNode(img, , {'src': 'www.image.com', 'alt': 'this is an image'})"
        )
