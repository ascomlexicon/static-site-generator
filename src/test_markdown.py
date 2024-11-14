"""
This module is a test suite for Markdown parsing functions.
"""
import unittest
from typing import Tuple
from textnode import TextNode, TextType
from markdown import split_node_delimiter

class TestMarkdownParsing(unittest.TestCase):
    """
    Unit tests for parsing functions.
    """ 
    
    def test_parse_text(self) -> None:
        """
        Tests the edge cases of simple inline Markdown (that includes no nested
        delimiters).
        """
        no_nodes: Tuple[list[TextNode], str, TextType] = (None, "*", TextType.ITALIC)
        empty_nodes: Tuple[list[TextNode], str, TextType] = ([], "*", TextType.ITALIC)
        
        no_text: Tuple[list[TextNode], str, TextType] = (
            [
                TextNode("Hello World", TextType.BOLD),
                TextNode("**This list should not change**", TextType.BOLD),
            ],
            "**",
            TextType.ITALIC
        )
        unclosed_delimiter: Tuple[list[TextNode], str, TextType] = (
            [TextNode("*Hello World", TextType.TEXT)], "*", TextType.ITALIC
        )
        
        normal_text: Tuple[list[TextNode], str, TextType] = (
            [
                TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
            ],
            "**",
            TextType.BOLD
        )
        start_end_delimiters: Tuple[list[TextNode], str, TextType] = (
            [
                TextNode("*Hello* World", TextType.TEXT),
                TextNode("Goodbye *World*", TextType.TEXT)
            ],
            "*",
            TextType.ITALIC
        )
        
        self.assertRaises(ValueError, split_node_delimiter, *(unclosed_delimiter))
        self.assertEqual(split_node_delimiter(*no_nodes), [])
        self.assertEqual(split_node_delimiter(*empty_nodes), [])
        self.assertEqual(
            split_node_delimiter(*no_text),
            [
                TextNode("Hello World", TextType.BOLD),
                TextNode("**This list should not change**", TextType.BOLD),               
            ]
        )
        self.assertEqual(
            split_node_delimiter(*normal_text),
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded phrase", TextType.BOLD),
                TextNode(" in the middle", TextType.TEXT)
            ]
        )
        self.assertEqual(
            split_node_delimiter(*start_end_delimiters),
            [
                TextNode("Hello", TextType.ITALIC),
                TextNode(" World", TextType.TEXT),
                TextType("Goodbye ", TextType.TEXT),
                TextNode("World", TextType.ITALIC)
            ]
        )
