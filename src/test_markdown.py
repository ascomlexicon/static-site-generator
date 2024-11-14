"""
This module is a test suite for Markdown parsing functions.
"""
import unittest
from typing import Tuple
from textnode import TextNode, TextType
from markdown import split_node_delimiter, extract_markdown_images, extract_markdown_links

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
                TextNode("Goodbye ", TextType.TEXT),
                TextNode("World", TextType.ITALIC)
            ]
        )
        
    def test_markdown_images(self) -> None:
        """
        A test to check the functionality of extracting image links from raw
        Markdown text.
        """
        no_images: str = "This Markdown has no images."
        one_image: str = "This is a Markdown image ![alt text](www.image.com)."
        multi_images: str = "![image 1](www.image-one.com) ![image 2](www.image-two.com)."
        normal_md: str = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"

        self.assertEqual(extract_markdown_images(""), [])
        self.assertEqual(extract_markdown_images(no_images), [])
        self.assertEqual(extract_markdown_images(one_image), [("alt text", "www.image.com")])
        self.assertEqual(extract_markdown_images(multi_images), [("image 1", "www.image-one.com"), ("image 2", "www.image-two.com")])
        self.assertEqual(
            extract_markdown_images(normal_md),
            [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        )
        
    def test_markdown_links(self) -> None:
        """
        A test to check if Markdown link parsing from raw strings is successful.
        """
        no_links: str = "This Markdown has no links."
        one_link: str = "This is a Markdown string with one link [alt text](www.google.com)."
        multi_links: str = "[link 1](www.link-one.com) [link 2](www.link-two.com)."
        normal_md: str = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"

        self.assertEqual(extract_markdown_links(""), [])
        self.assertEqual(extract_markdown_links(no_links), [])
        self.assertEqual(extract_markdown_links(one_link), [("alt text", "www.google.com")])
        self.assertEqual(extract_markdown_links(multi_links), [("link 1", "www.link-one.com"), ("link 2", "www.link-two.com")])
        self.assertEqual(
            extract_markdown_links(normal_md),
            [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        )
