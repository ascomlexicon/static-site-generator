import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    """
    Unit tests for the TextNode object.
    """
    
    def test_equality(self):
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
