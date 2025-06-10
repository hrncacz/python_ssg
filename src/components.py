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


def delimiter_from_text_type(text_type):
    match text_type:
        case TextType.TEXT:
            return " "
        case TextType.ITALIC:
            return "_"
        case TextType.BOLD:
            return "**"
        case TextType.CODE:
            return "`"
        case TextType.LINK:
            return ("[", "](", ")")
        case TextType.IMAGE:
            return ("![", "](", ")")
        case _:
            raise Exception("Invalid TEXT TYPE")

# "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"


def split_nodes_link_and_image(old_nodes, text_type):
    new_nodes = []
    checking_node = old_nodes[0]
    if checking_node.text_type != TextType.TEXT:
        new_nodes.append(checking_node)
    else:
        new_nodes.extend(check_text_for_link_and_image(
            checking_node.text, text_type))

    if len(old_nodes) == 1:
        return new_nodes
    new_nodes.extend(split_nodes_link_and_image(
        old_nodes[1:], text_type))
    return new_nodes


def split_nodes_delimiter(old_nodes, text_type):
    new_nodes = []
    checking_node = old_nodes[0]
    if checking_node.text_type != TextType.TEXT:
        new_nodes.append(checking_node)
    else:
        new_nodes.extend(check_text_for_delimiter(
            checking_node.text,  TextType.TEXT, text_type))

    if len(old_nodes) == 1:
        return new_nodes
    new_nodes.extend(split_nodes_delimiter(
        old_nodes[1:], text_type))
    return new_nodes


def check_text_for_delimiter(sentence, finding_text_type, text_type):
    nodes = []
    delimiter = delimiter_from_text_type(text_type)
    if finding_text_type != TextType.TEXT:
        check = sentence.find(delimiter)
        if check == -1:
            raise Exception(f"Closing delimiter {
                            delimiter} was not found in --- {sentence}")
    splited_text = sentence.split(delimiter, 1)
    if len(splited_text[0]) != 0:
        nodes.append(TextNode(splited_text[0], finding_text_type))
    if len(splited_text) == 1:
        return nodes
    if finding_text_type != text_type:
        return nodes + check_text_for_delimiter(splited_text[1],  text_type, text_type)
    else:
        return nodes + check_text_for_delimiter(splited_text[1],  TextType.TEXT, text_type)


def check_text_for_link_and_image(sentence, text_type):
    if text_type != TextType.LINK and text_type != TextType.IMAGE:
        raise Exception("Wrong TextType passed")
    nodes = []
    splited_text = sentence.split(delimiter_from_text_type(text_type)[0], 1)
    if len(splited_text[0]) != 0:
        nodes.append(TextNode(splited_text[0], TextType.TEXT))
    if len(splited_text) == 1:
        return nodes
    try:
        link_image_tuple, rest_of_sentence = find_alt_text(
            splited_text[1], text_type)
    except Exception as e:
        raise e
    nodes.append(
        TextNode(link_image_tuple[0], text_type, link_image_tuple[1]))
    return nodes + check_text_for_link_and_image(rest_of_sentence, text_type)


def find_alt_text(sentence, text_type):
    splited_text = sentence.split(delimiter_from_text_type(text_type)[1], 1)
    if len(splited_text) == 1:
        raise Exception(
            f"Missing closing brackets of LINK/IMAGE node in --- {sentence}")
    try:
        url, rest_of_sentence = find_url(splited_text[1], text_type)
    except Exception as e:
        raise e
    alt_text_url_tuple = (splited_text[0], url)
    return alt_text_url_tuple, rest_of_sentence


def find_url(sentence, text_type):
    splited_text = sentence.split(delimiter_from_text_type(text_type)[2], 1)
    if len(splited_text) == 1:
        raise Exception(
            f"Missing closing brackets of of LINK/IMAGE node in --- {sentence}")
    return splited_text[0], splited_text[1]


def text_to_text_nodes(text):
    text_codes = split_nodes_delimiter(
        [TextNode(text, TextType.TEXT)], TextType.CODE)
    text_bolds = split_nodes_delimiter(text_codes, TextType.BOLD)
    text_italics = split_nodes_delimiter(text_bolds, TextType.ITALIC)
    text_images = split_nodes_link_and_image(text_italics, TextType.IMAGE)
    text_links = split_nodes_link_and_image(text_images, TextType.LINK)
    return text_links
