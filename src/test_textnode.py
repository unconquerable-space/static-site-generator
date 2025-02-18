import unittest

from textnode import TextNode, TextType

TEST_URL = "https://boot.dev"

class TestTextNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("foo", TextType.NORMAL)
        self.assertEqual(node.text, "foo")

    def test_text_type(self):
        node = TextNode("", TextType.BOLD)
        self.assertEqual(node.text_type, TextType.BOLD)

    def test_url(self):
        node = TextNode("", TextType.NORMAL, TEST_URL)
        self.assertEqual(node.url,TEST_URL)

    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, TEST_URL)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
