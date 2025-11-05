from textnode import TextNode, TextType
from typing import List
import re

def split_nodes_delimiter(old_nodes:List[TextNode], delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        elif delimiter not in old_node.text:
            new_nodes.append(old_node)
            continue
        split_text = old_node.text.split(delimiter)
        if split_text[0] != '':
            new_node = [TextNode(split_text[0], TextType.TEXT)]    
        else:
            new_node = []
        for i in range(1,len(split_text)):
            if i%2==0:
                new_node.append(TextNode(split_text[i], TextType.TEXT))
            else:
                new_node.append(TextNode(split_text[i], text_type))
        new_nodes.extend(new_node)
    return new_nodes

def extract_markdown_images(text):
    txt = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return txt

def extract_markdown_links(text):
    txt = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return txt

def split_nodes_image(old_nodes:List[TextNode]):
    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        node = []
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if sections[0]!="":
                node.append(TextNode(sections[0], TextType.TEXT))
                node.append(TextNode(image[0], TextType.IMAGE, url=image[1]))
            else:
                node.append(TextNode(image[0], TextType.IMAGE, url=image[1]))
            original_text = sections[1]
        if original_text != "":
            node.append(TextNode(original_text, TextType.TEXT))
        new_nodes.extend(node)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        node = []
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if sections[0]!="":
                node.append(TextNode(sections[0], TextType.TEXT))
                node.append(TextNode(link[0], TextType.LINK, url=link[1]))
            else:
                node.append(TextNode(link[0], TextType.LINK, url=link[1]))
            original_text = sections[1]
        if original_text != "":
            node.append(TextNode(original_text, TextType.TEXT))
        new_nodes.extend(node)
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes