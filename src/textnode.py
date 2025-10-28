from enum import Enum
from leafnode import LeafNode
from parentnode import ParentNode
from htmlnode import HTMLNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type,url=None):
        self.text=text
        self.text_type=TextType(text_type)
        self.url=url

    def __eq__(self,other):
        return self.text==other.text and self.text_type==other.text_type and self.url==other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    

def text_node_to_html_node(text_node:TextNode):
    if type(text_node.text_type)!=TextType:
        raise TypeError
    match text_node.text_type.value:
        case "text":
            return LeafNode(None, text_node.text)
        case "bold":
            return LeafNode("b", text_node.text)
        case "italic":
            return LeafNode("i", text_node.text)
        case "code":
            return LeafNode("code", text_node.text)
        case "link":
            return LeafNode("a", text_node.text)
        case "image":
            return LeafNode("img", "", {"src":text_node.url, "alt":text_node.text})
        case _:
            raise TypeError
