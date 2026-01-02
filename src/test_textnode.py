import unittest

from textnode import TextNode, TextType, text_node_to_html_node

TEST_URL = "https://boot.dev"

class TestTextNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("foo", TextType.TEXT)
        self.assertEqual(node.text, "foo")

    def test_text_type(self):
        node = TextNode("", TextType.BOLD)
        self.assertEqual(node.text_type, TextType.BOLD)

    def test_url(self):
        node = TextNode("", TextType.TEXT, TEST_URL)
        self.assertEqual(node.url,TEST_URL)

    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, TEST_URL)
        self.assertNotEqual(node, node2)

    def test_text_to_html_type_text(self):
        node = TextNode("Plain text", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "Plain text")

    def test_text_to_html_type_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")

    def test_text_to_html_type_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")

    def test_text_to_html_type_code(self):
        code = '''
            #include <stdio.h>

            int main() {
                printf("hello world");
                return 0;
            }
        '''
        node = TextNode(code, TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, code)

    def test_text_to_html_type_link(self):
        url = TEST_URL
        node = TextNode(url, TextType.LINK)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, url)

    def test_text_to_html_type_image(self):
        img = "placeholder.jpg"
        alt = "placeholder"
        node = TextNode(alt, TextType.IMAGE, img)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props.get("src"), img)


if __name__ == "__main__":
    unittest.main()
