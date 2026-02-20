from enum import Enum

from textnode import TextNode, TextType
from node_to_html import text_node_to_html_node
from htmlnode import HTMLNode, ParentNode, LeafNode
from split_nodes import split_nodes_delimiter
from extract_markdown import text_to_text_nodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    elif len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    elif block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    elif block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    elif block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    stripped_blocks = []
    for block in blocks:
        if block == "":
            continue
        stripped_blocks.append(block.strip())
    return stripped_blocks

def text_to_children(text):
    text_nodes = text_to_text_nodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def markdown_to_html_nodes(markdown):
    split_blocks = markdown_to_blocks(markdown)
    children = []
    for block in split_blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    elif block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    elif block_type == BlockType.CODE:
        return code_to_html_node(block)
    elif block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    elif block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)
    elif block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)
    else:
        raise ValueError(f"Unknown BlockType: {block_type}")

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children, None)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading: {level}")
    
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children, None)

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child], None)
    return ParentNode("pre", [code], None)

def unordered_list_to_html_node(block):
    lines = block.split("\n")
    children = []
    for line in lines:
        if not line.startswith("- "):
            raise ValueError("invalid unordered list")
        text = line[2:]
        text_nodes = text_to_text_nodes(text)
        html_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
        children.append(ParentNode("li", html_nodes, None))
    return ParentNode("ul", children, None)

def ordered_list_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        parts = item.split(". ", 1)
        text = parts[1]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children, None))
    return ParentNode("ol", html_items, None)

def quote_to_html_node(block):
    lines = block.split("\n")
    new_line = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote")
        new_line.append(line.lstrip(">").strip())
    content = " ".join(new_line)
    children = text_to_children(content)
    return ParentNode("blockquote", children, None)