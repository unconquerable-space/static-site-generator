import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_tag(self):
        node = HTMLNode("h1", None, None, None)
        self.assertEqual(node.tag, "h1")

    def test_value(self):
        node = HTMLNode(None,  "foo", None, None)
        self.assertEqual(node.value, "foo")

    def test_children(self):
        node1 = HTMLNode("h1", "hello", None, None)
        node2 = HTMLNode("h2", "world", None, None)
        node3 = HTMLNode(None, None, [node1, node2], None)
        self.assertEqual(len(node3.children), 2)

    def test_props(self):
        node = HTMLNode(None, None, None, { "id": "123" })
        self.assertEqual(node.props["id"], "123")

    def test_leaf_node(self):
        node = LeafNode("p", "This is a paragraph of text.", None)
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_leaf_node_with_attr(self):
        node = LeafNode("a", "Click me!", { "href": "https://www.google.com" })
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")

    def test_parent_node_single_element(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b></p>")

    def test_parent_node_single_value(self):
        node = ParentNode(
            "p",
            [
                LeafNode(None, "text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p>text</p>")

    def test_parent_node_attr(self):
        node = ParentNode(
            "p",
            [
                LeafNode(None, "text"),
            ],
            { "id": "123" },
        )
        self.assertEqual(node.to_html(), "<p id=\"123\">text</p>")

    def test_parent_node_multiple_elements(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_parent_node_no_children(self):
        node = ParentNode("p", None)
        self.assertRaises(ValueError, node.to_html)

    def test_parent_node_no_tag(self):
        node = ParentNode(None, [
                LeafNode("b", "Bold text"),
        ])
        self.assertRaises(ValueError, node.to_html)

if __name__ == "__main__":
    unittest.main()
