import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from components import text_node_to_html_node


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


if __name__ == "__main__":
    unittest.main()
