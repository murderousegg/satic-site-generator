from enum import Enum
import re
from htmlnode import HTMLNode
from textnode import text_node_to_html_node
from split_nodes import text_to_textnodes
from parentnode import ParentNode
from leafnode import LeafNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def is_incremental_list(text):
    # Extract leading numbers from each line
    numbers = [int(n) for n in re.findall(r'^(\d+)\. ', text, flags=re.MULTILINE)]
    # Check if they start at 1 and increase by 1
    return numbers == list(range(1, len(numbers) + 1))

def block_to_block_type(markdown):
    pattern = re.compile(r'^(#{1,6})\s.+$', re.MULTILINE)
    if bool(pattern.match(markdown)):
        return BlockType.HEADING
    if markdown[:3] == "```" and markdown[-3:] == "```":
        return BlockType.CODE
    # check > at start of every line
    pattern = re.compile(r'^(?:>[^\n]*(?:\n|$))+$')
    if bool(pattern.match(markdown)):
        return BlockType.QUOTE
    pattern = re.compile(r'^(?:- [^\n]*(?:\n|$))+$')
    if bool(pattern.match(markdown)):
        return BlockType.UNORDERED_LIST
    if is_incremental_list(markdown) and markdown[:3] == "1. ":
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    md_split = markdown.split("\n\n")
    res = []
    for md in md_split:
        if md == "":
            continue
        res.append(md.strip())
    return res

def text_to_children(text):
    nodes = text_to_textnodes(text)
    html_nodes = []
    for node in nodes:
        html_node = text_node_to_html_node(node)
        html_nodes.append(html_node)
    return html_nodes

def markdown_to_html_node(markdown):
    md_blocks = markdown_to_blocks(markdown)
    parent_node = ParentNode("div", children=[])
    for block in md_blocks:
        block_type = block_to_block_type(block)
        node = None
        match block_type:
            case BlockType.HEADING:
                split_heading = block.split(" ", 1)
                count = len(split_heading[0])
                node = ParentNode(tag=f"h{count}", children=text_to_children(split_heading[1]))
            case BlockType.QUOTE:
                split_lines = block.split("\n")
                fixed_lines = []
                for line in split_lines:
                    fixed_lines.append(re.sub(r'^>\s?', '', line))
                txt = "\n".join(fixed_lines)
                node = ParentNode("blockquote", children=text_to_children(txt))
            case BlockType.UNORDERED_LIST:
                node = ParentNode("ul",[])
                split_lines = block.split("\n")
                for line in split_lines:
                    line = re.sub(r'^-\s?', '', line)
                    line_node = ParentNode("li", text_to_children(line))
                    node.children.append(line_node)
            case BlockType.ORDERED_LIST:
                node = ParentNode("ol",[])
                split_lines = block.split("\n")
                for line in split_lines:
                    line = re.sub(r'^\d+\. ?', '', line)
                    line_node = ParentNode("li", text_to_children(line))
                    node.children.append(line_node)
            case BlockType.PARAGRAPH:
                node = ParentNode("p",text_to_children(block.replace("\n", " ")))
            case BlockType.CODE:
                nest_node = LeafNode("code", block[3:-3].lstrip("\n"))
                node = ParentNode("pre", [nest_node])
        parent_node.children.append(node)
    return parent_node

def extract_title(markdown):
    matches = re.findall(r'^# .*', markdown, re.MULTILINE)
    if len(matches) == 0:
        raise Exception("no title found")
    title = matches[0].strip("# ")
    return title

        

                