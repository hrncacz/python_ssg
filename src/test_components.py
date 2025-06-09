import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from components import text_node_to_html_node, split_nodes_delimiter, split_nodes_link_and_image


class TestHTMLNode(unittest.TestCase):
    def test_textnode_to_html(self):
        node_text = TextNode("This is a text node", TextType.TEXT)
        html_node_text = text_node_to_html_node(node_text)
        self.assertEqual(html_node_text.tag, None)
        self.assertEqual(html_node_text.value, "This is a text node")
        node_italic = TextNode("This is a italic node", TextType.ITALIC)
        html_node_italic = text_node_to_html_node(node_italic)
        self.assertEqual(html_node_italic.tag, "i")
        self.assertEqual(html_node_italic.value, "This is a italic node")
        node_link = TextNode("This is a anchor node",
                             TextType.LINK, "https://www.google.com")
        html_node_link = text_node_to_html_node(node_link)
        self.assertEqual(html_node_link.tag, "a")
        self.assertEqual(html_node_link.value, "This is a anchor node")
        self.assertEqual(html_node_link.props, {
                         "href": "https://www.google.com"})

    def test_split_nodes_delimiter(self):
        node1 = TextNode(
            "This is text with a `code block` word", TextType.TEXT)
        new_nodes1 = split_nodes_delimiter([node1], "`", TextType.CODE)
        self.assertEqual(new_nodes1, [TextNode("This is text with a ", "normal", None), TextNode(
            "code block", "code", None), TextNode(" word", "normal", None)])

        node2 = TextNode(
            "This is text with a **bold block** and also _italic block_ word", TextType.TEXT)
        bold_nodes2 = split_nodes_delimiter([node2], "**", TextType.BOLD)
        italic_nodes2 = split_nodes_delimiter(
            bold_nodes2, "_", TextType.ITALIC)
        self.assertEqual(italic_nodes2, [TextNode("This is text with a ", "normal", None), TextNode("bold block", "bold", None), TextNode(
            " and also ", "normal", None), TextNode("italic block", "italic", None), TextNode(" word", "normal", None)])
        node3 = TextNode(
            "This is text with a **bold block** and also _italic block word", TextType.TEXT)
        bold_nodes3 = split_nodes_delimiter([node3], "**", TextType.BOLD)
        with self.assertRaises(Exception):
            italic_nodes3 = split_nodes_delimiter(
                bold_nodes3, "_", TextType.ITALIC)

    def test_split_nodes_link_and_image(self):

        text_node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)
        node = split_nodes_link_and_image([text_node], TextType.LINK)
        print("!Test text pro split,".split("!", 1))


if __name__ == "__main__":
    unittest.main()
