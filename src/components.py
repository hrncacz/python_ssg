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
        word_arr = checking_node.text.split(" ")
        filtered_arr = filter(lambda word: delimiter in word, word_arr)
        if len(filtered_arr) % 2 != 0:
            raise Exception(f"Missing closing delimiter {
                            delimiter} in: {checking_node.text}")
        indexes = list(map(lambda l: word_arr.index(l), filtered_arr))

    if len(old_nodes) == 1:
        return new_nodes
    new_nodes.extend(split_nodes_delimiter(
        old_nodes[1:], delimiter, text_type))
    return new_nodes
