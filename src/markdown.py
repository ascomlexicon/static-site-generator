"""
This module contains functions that parses markdown files.
"""
import re
from textnode import TextNode, TextType

def split_node_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    """
    Takes in a list of TextNodes and parses their values against a delimiter if
    they are a `TextType.TEXT` node.

    :param old_nodes: TextNodes to parse.
    :param delimiter: The symbol to parse against.
    :param text_type: The type to convert the text within the delimiter to.
    :return: A list of TextNode as a result of parsing with a delimiter.
    :raise: ValueError in the cases where the delimiter is not closed.
    """
    if old_nodes is None:
        return []

    parsed_nodes: list[TextNode] = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            parsed_nodes.append(node)
            continue

        split_string = node.text.split(delimiter)
        if len(split_string) % 2 == 0:
            raise ValueError(f"Invalid markdown: '{delimiter}' is unclosed.")
        
        for index, text in enumerate(split_string):
            if not text:
                continue

            if index % 2 == 0:
                parsed_nodes.append(TextNode(text, node.text_type))
            else:
                parsed_nodes.append(TextNode(text, text_type))
                
    return parsed_nodes

def split_nodes_images(old_nodes: list[TextNode]) -> list[TextNode]:
    """
    Takes in a list of TextNodes (of TextType.TEXT) and extract the nodes
    containing image data. 
    
    :param old_nodes: The TextNodes to parse.
    :return: The list of parsed TextNodes
    """
    if old_nodes is None:
        return []
    
    new_nodes: list[TextNode] = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        md_images: list[tuple[str, str]] = extract_markdown_images(node.text)

        if len(md_images) == 0:
            new_nodes.append(node)
            continue

        text_to_parse: str = node.text

        for image in md_images:
            alt_text: str = image[0]
            image_link: str = image[1]
            
            sections: list[str] = text_to_parse.split(f"![{alt_text}]({image_link})", 1)

            if sections[0]:
                new_nodes.append(TextNode(sections[0], node.text_type))
                
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, image_link))
            
            text_to_parse = sections[1]
            
        if sections[1]:
            new_nodes.append(TextNode(sections[1], node.text_type))
            
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    """
    Takes in a list of TextNodes (of TextType.TEXT) and extract the nodes
    containing standard links. 
    
    :param old_nodes: The TextNodes to parse.
    :return: The list of parsed TextNodes
    """
    if old_nodes is None:
        return []
    
    new_nodes: list[TextNode] = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        links: list[tuple[str, str]] = extract_markdown_links(node.text)

        if len(links) == 0:
            new_nodes.append(node)
            continue

        text_to_parse: str = node.text

        for link in links:
            alt_text: str = link[0]
            url: str = link[1]
            
            sections: list[str] = text_to_parse.split(f"[{alt_text}]({url})", 1)

            if sections[0]:
                new_nodes.append(TextNode(sections[0], node.text_type))
                
            new_nodes.append(TextNode(alt_text, TextType.LINK, url))
            
            text_to_parse = sections[1]
            
        if sections[1]:
            new_nodes.append(TextNode(sections[1], node.text_type))
            
    return new_nodes

def extract_markdown_images(raw_md: str) -> list[tuple[str, str]]:
    """
    Takes in a string of raw markdown and parses it for image links.
    
    :param raw_md: The Markdown text to parse.
    :return: A list of tuples containing the alt text and image source.
    """
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", raw_md)

def extract_markdown_links(raw_md: str) -> list[tuple[str, str]]:
    """
    Takes in a string representing Markdown, and parses it for links.

    :param raw_md: The raw Markdown text to parse.
    :return: A list of tuples holding the alt text and link.
    """
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", raw_md)
