from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "Text"
    BOLD = "Bold"
    ITALIC = "Italic"
    CODE = "Code"
    LINK = "Link"
    IMAGE = "Image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text, None)
        case TextType.BOLD:
            return LeafNode("b", text_node.text, None)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text, None)
        case TextType.CODE:
            return LeafNode("code", text_node.text, None)
        case TextType.LINK:
            return LeafNode("a", text_node.text, { "href": text_node.url })
        case TextType.IMAGE:
            return LeafNode("img", "", { "src": text_node.url, "alt": text_node.text })
        case _:
            raise Exception("Invalid text type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for n in old_nodes:
        new_nodes.extend(split_node_delimiter(n, delimiter, text_type))
    return new_nodes

def split_node_delimiter(old_node, delimiter, text_type):
    new_nodes = []
    cur = old_node.text
    if not delimiter in cur:
        return [TextNode(old_node.text, TextType.TEXT)]

    while delimiter in cur:
        before, _, after = cur.partition(delimiter)
        if not delimiter in after:
            new_nodes.append(TextNode(cur, TextType.TEXT))
            break
        content, sep, remainder = after.partition(delimiter)
        if before:
            new_nodes.append(TextNode(before, TextType.TEXT))
        if sep:
            new_nodes.append(TextNode(content, text_type))
        if delimiter in remainder:
            cur = remainder
            continue
        if remainder:
            new_nodes.append(TextNode(remainder, TextType.TEXT))
        break

    return new_nodes



