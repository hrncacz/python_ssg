from functools import reduce
from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": ""})
        case _:
            raise Exception("Invalid TEXT TYPE")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    checking_node = old_nodes[0]
    if checking_node.text_type != TextType.TEXT:
        new_nodes.append(checking_node)
    else:
        if checking_node.text[0] == delimiter:
            new_nodes.extend(check_text_for_delimiter(
                checking_node.text, delimiter, text_type, text_type))
        else:
            new_nodes.extend(check_text_for_delimiter(
                checking_node.text, delimiter, TextType.TEXT, text_type))

    if len(old_nodes) == 1:
        return new_nodes
    new_nodes.extend(split_nodes_delimiter(
        old_nodes[1:], delimiter, text_type))
    return new_nodes


def check_text_for_delimiter(sentence, delimiter, finding_text_type, text_type):
    nodes = []
    if finding_text_type != TextType.TEXT:
        check = sentence.find(delimiter)
        if check == -1:
            raise Exception(f"Closing delimiter {
                            delimiter} was not found in --- {sentence}")
    splited_text = sentence.split(delimiter, 1)
    nodes.append(TextNode(splited_text[0], finding_text_type))
    if len(splited_text) == 1:
        return nodes
    if finding_text_type != text_type:
        return nodes + check_text_for_delimiter(splited_text[1], delimiter, text_type, text_type)
    else:
        return nodes + check_text_for_delimiter(splited_text[1], delimiter, TextType.TEXT, text_type)
