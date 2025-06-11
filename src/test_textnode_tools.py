import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode_tools import text_node_to_html_node, split_nodes_delimiter, split_nodes_link_and_image, text_to_text_nodes


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
        new_nodes1 = split_nodes_delimiter([node1],  TextType.CODE)
        self.assertEqual(new_nodes1, [TextNode("This is text with a ", "normal", None), TextNode(
            "code block", "code", None), TextNode(" word", "normal", None)])

        node2 = TextNode(
            "This is text with a **bold block** and also _italic block_ word", TextType.TEXT)
        bold_nodes2 = split_nodes_delimiter([node2],  TextType.BOLD)
        italic_nodes2 = split_nodes_delimiter(
            bold_nodes2,  TextType.ITALIC)
        self.assertEqual(italic_nodes2, [TextNode("This is text with a ", "normal", None), TextNode("bold block", "bold", None), TextNode(
            " and also ", "normal", None), TextNode("italic block", "italic", None), TextNode(" word", "normal", None)])
        node3 = TextNode(
            "This is text with a **bold block** and also _italic block word", TextType.TEXT)
        bold_nodes3 = split_nodes_delimiter([node3],  TextType.BOLD)
        with self.assertRaises(Exception):
            italic_nodes3 = split_nodes_delimiter(
                bold_nodes3,  TextType.ITALIC)

    def test_split_nodes_link_and_image(self):

        text_node1 = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)
        node1 = split_nodes_link_and_image([text_node1], TextType.LINK)
        self.assertEqual(node1, [TextNode("This is text with a link ", TextType.TEXT, None), TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                         TextNode(" and ", TextType.TEXT, None), TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")])

        text_node2 = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)
        text_node2_2 = TextNode(
            "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)
        text_node2_3 = TextNode(
            "This is text with a link ![to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)
        node2 = split_nodes_link_and_image(split_nodes_link_and_image(
            [text_node2, text_node2_2, text_node2_3], TextType.IMAGE), TextType.LINK)
        self.assertEqual(node2, [TextNode("This is text with a link ", TextType.TEXT, None), TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"), TextNode(" and ", TextType.TEXT, None), TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"), TextNode("This is text with a link ", TextType.TEXT, None), TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
                         TextNode(" and ", TextType.TEXT, None), TextNode("to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev"), TextNode("This is text with a link ", TextType.TEXT, None), TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"), TextNode(" and ", TextType.TEXT, None), TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")])

        text_node3 = TextNode(
            "![to boot dev](https://www.boot.dev)[to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)
        node3 = split_nodes_link_and_image(split_nodes_link_and_image(
            [text_node3], TextType.IMAGE), TextType.LINK)
        self.assertEqual(node3, [TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
                         TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")])

    def test_text_to_text_nodes(self):
        text1 = "Tohle je testovací **bold text** a toto zase _italic text_ v tomhle bloku otestuju `code text` teď třeba image ![seznam cz](https://www.seznam.cz) a poslední je link [google com](https://www.google.com) a konec."
        self.assertEqual(text_to_text_nodes(text1), [TextNode("Tohle je testovací ", TextType.TEXT, None), TextNode("bold text", TextType.BOLD, None), TextNode(" a toto zase ", TextType.TEXT, None), TextNode("italic text", TextType.ITALIC, None), TextNode(" v tomhle bloku otestuju ", TextType.TEXT, None), TextNode(
            "code text", TextType.CODE, None), TextNode(" teď třeba image ", TextType.TEXT, None), TextNode("seznam cz", TextType.IMAGE, "https://www.seznam.cz"), TextNode(" a poslední je link ", TextType.TEXT, None), TextNode("google com", TextType.LINK, "https://www.google.com"), TextNode(" a konec.", TextType.TEXT, None)])


if __name__ == "__main__":
    unittest.main()
