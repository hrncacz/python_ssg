import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_htmlnodes_props_to_html(self):
        html_node1 = HTMLNode(
            "h1",
            "Test text",
            [],
            {
                "href": "https://www.google.com",
                "target": "_blank",
                "test": "trest"
            })
        self.assertEqual(
            html_node1.props_to_html(), " href=\"https://www.google.com\" target=\"_blank\" test=\"trest\"")
        html_node2 = HTMLNode(
            "p",
            None,
            [],
            {
                "href": "https://www.google.com",
            })
        self.assertEqual(
            html_node2.props_to_html(), " href=\"https://www.google.com\"")

        html_node3 = HTMLNode(
            "",
            "",
            [],
            {
            })
        self.assertEqual(
            html_node3.props_to_html(), "")

    def test_leafnodes_to_html(self):
        leaf_node1 = LeafNode("p", "Tohle je testovaci node1")
        leaf_node2 = LeafNode("b", "Tohle je testovaci node2")
        leaf_node3 = LeafNode("p", None)
        leaf_node4 = LeafNode(None, "Tohle je testovaci node4")
        self.assertEqual(leaf_node1.to_html(),
                         "<p>Tohle je testovaci node1</p>", "OK")
        self.assertEqual(leaf_node2.to_html(),
                         "<b>Tohle je testovaci node2</b>", "OK")
        with self.assertRaises(ValueError):
            leaf_node3.to_html()
        self.assertEqual(leaf_node4.to_html(), "Tohle je testovaci node4")

    def test_parentnodes_to_html(self):
        child_node1 = LeafNode("span", "child")
        parent_node1 = ParentNode("div", [child_node1])
        self.assertEqual(parent_node1.to_html(),
                         "<div><span>child</span></div>")

        grandchild_node2 = LeafNode("b", "grandchild")
        child_node2 = ParentNode("span", [grandchild_node2])
        parent_node2 = ParentNode("a", [child_node2], {
            "href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(
            parent_node2.to_html(),
            "<a href=\"https://www.google.com\" target=\"_blank\"><span><b>grandchild</b></span></a>")

        grandchild_node3 = LeafNode("b", "grandchild")
        grandchild_node3_1 = ParentNode("b", None)
        child_node3 = ParentNode(
            "span", [grandchild_node3, grandchild_node3_1])
        parent_node3 = ParentNode("div", [child_node3])
        with self.assertRaises(ValueError):
            parent_node3.to_html()

        grandchild_node4 = LeafNode("b", "grandchild")
        child_node4 = ParentNode(
            None, [grandchild_node4])
        parent_node4 = ParentNode("div", [child_node4])
        with self.assertRaises(ValueError):
            parent_node4.to_html()


if __name__ == "__main__":
    unittest.main()
