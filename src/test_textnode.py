import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        print("TEST EQ")
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        node3 = TextNode("Ahoj tohle je test.",
                         TextType.LINK, "https://boot.dev")
        node4 = TextNode("Ahoj tohle je test.",
                         TextType.LINK, "https://boot.dev")
        self.assertEqual(node3, node4)
        node5 = TextNode("Test trest", TextType.ITALIC)
        node6 = TextNode("Test trest", TextType.ITALIC)
        self.assertEqual(node5, node6)

    def test_neq(self):
        print("TEST NEQ")
        node = TextNode("This is a text node", TextType.BOLD)
        node4 = TextNode("Ahoj tohle je test.",
                         TextType.LINK, "https://boot.dev")
        self.assertNotEqual(node, node4)
        node5 = TextNode("Test trest", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node5, node2)
        node6 = TextNode("Test trest", TextType.ITALIC)
        node3 = TextNode("Ahoj tohle je test.",
                         TextType.LINK, "https://boot.dev")
        self.assertNotEqual(node6, node3)


if __name__ == "__main__":
    unittest.main()
