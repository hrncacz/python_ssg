from enum import Enum
import re
from htmlnode import ParentNode, LeafNode
from textnode_tools import text_to_text_nodes, text_node_to_html_node, TextNode, TextType


class BlockType(Enum):
    PARAGRAPH = "p"
    HEADING = "h"
    CODE = "pre"
    QUOTE = "blockquote"
    UNORDERED_LIST = "ul"
    LIST_ITEM = "li"
    ORDERED_LIST = "ol"


def block_to_block_type(block):
    if re.search(r"^\#{1,6}\s{1}", block):
        splited = block.split(" ", 1)
        h_level = splited[0].count("#")
        return basic_blocks(BlockType.HEADING.value + str(h_level), splited[1])
    elif block.startswith("```") and block.endswith("```"):
        return code_blocks(BlockType.CODE.value, block[3:len(block)-3].removeprefix("\n"))
    elif block.startswith(">"):
        return basic_blocks(BlockType.QUOTE.value, block[1:].strip())
    elif block.startswith("- "):
        return ulist_blocks(BlockType.UNORDERED_LIST.value, block[2:])
    elif re.search(r"^\d+\.\s", block):
        return olist_blocks(BlockType.ORDERED_LIST.value, block)
    else:
        return basic_blocks(BlockType.PARAGRAPH.value, block)


def markdown_to_blocks(text):
    blocks = text.split("\n\n")
    blocks_striped = list(map(lambda l: l.strip(), blocks))
    blocks_filtered = list(filter(lambda l: len(l) > 0, blocks_striped))
    return blocks_filtered


def basic_blocks(tag, clean_text):
    children = text_to_text_nodes(clean_text.replace("\n", " "))
    children_html = list(map(lambda l: text_node_to_html_node(l), children))
    return ParentNode(tag, children_html)


def code_blocks(tag, clean_text):
    return ParentNode(tag, [text_node_to_html_node(TextNode(clean_text, TextType.CODE, None))])


def ulist_blocks(tag, text):
    li_array = text.split("\n- ")
    li_array_text_nodes = list(map(lambda l: text_to_text_nodes(l), li_array))
    children_array = list(map(lambda l: ParentNode("li", list(
        map(lambda k: text_node_to_html_node(k), l))), li_array_text_nodes))
    return ParentNode(tag, children_array)


def olist_blocks(tag, text):
    li_array = text.split("\n")
    li_array_text_nodes = list(
        map(lambda l: text_to_text_nodes(l.split(". ")[1]), li_array))
    children_array = list(map(lambda l: ParentNode("li", list(
        map(lambda k: text_node_to_html_node(k), l))), li_array_text_nodes))
    return ParentNode(tag, children_array)


def markdown_to_html(text):
    blocks = markdown_to_blocks(text)
    children = list(map(lambda a: block_to_block_type(a), blocks))
    return ParentNode("div", children)
