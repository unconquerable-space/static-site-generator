import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter

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

    def test_split_nodes_delimiter_none(self):
        node = TextNode("Some plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "Some plain text")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

    def test_split_nodes_delimiter_unclosed(self):
        self.split_nodes_check("This is text with ** that isn't bold", "**", TextType.BOLD, [
            TextNode("This is text with ** that isn't bold", TextType.TEXT),
        ])

        self.split_nodes_check("This is text with _ that isn't italic", "_", TextType.ITALIC, [
            TextNode("This is text with _ that isn't italic", TextType.TEXT),
        ])

        self.split_nodes_check("This is **bold text** followed by text with ** that isn't bold", "**", TextType.BOLD, [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" followed by text with ** that isn't bold", TextType.TEXT),
        ])

        self.split_nodes_check("This is _italic text_ followed by text with _ that isn't italic", "_", TextType.ITALIC, [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" followed by text with _ that isn't italic", TextType.TEXT),
        ])

        self.split_nodes_check("This is **bold text** followed by **more bold text** followed by text with ** that isn't bold", "**", TextType.BOLD, [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" followed by ", TextType.TEXT),
            TextNode("more bold text", TextType.BOLD),
            TextNode(" followed by text with ** that isn't bold", TextType.TEXT),
        ])

        self.split_nodes_check("This is _italic text_ followed by _more italic text_ followed by text with _ that isn't italic", "_", TextType.ITALIC, [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" followed by ", TextType.TEXT),
            TextNode("more italic text", TextType.ITALIC),
            TextNode(" followed by text with _ that isn't italic", TextType.TEXT),
        ])

        self.split_nodes_check("**This is bold** this is not **this is** this ** is not", "**", TextType.BOLD, [
            TextNode("This is bold", TextType.BOLD),
            TextNode(" this is not ", TextType.TEXT),
            TextNode("this is", TextType.BOLD),
            TextNode(" this ** is not", TextType.TEXT),
        ])

        self.split_nodes_check("_This is italic_ this is not _this is_ this _ is not", "_", TextType.ITALIC, [
            TextNode("This is italic", TextType.ITALIC),
            TextNode(" this is not ", TextType.TEXT),
            TextNode("this is", TextType.ITALIC),
            TextNode(" this _ is not", TextType.TEXT),
        ])

        self.split_nodes_check("This is text with a `code block` word and then a ` for no reason", "`", TextType.CODE, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word and then a ` for no reason", TextType.TEXT),
        ])


    def test_split_nodes_delimiter_one(self):

        self.split_nodes_check("This is text with a `code block` word", "`", TextType.CODE, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])

        self.split_nodes_check("Some **bold** text", "**", TextType.BOLD, [
            TextNode("Some ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ])

        self.split_nodes_check("Some _italic_ text", "_", TextType.ITALIC, [
            TextNode("Some ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ])

        self.split_nodes_check("Some text **bolded**", "**", TextType.BOLD, [
            TextNode("Some text ", TextType.TEXT),
            TextNode("bolded", TextType.BOLD),
        ])

        self.split_nodes_check("Some text _italicized_", "_", TextType.ITALIC, [
            TextNode("Some text ", TextType.TEXT),
            TextNode("italicized", TextType.ITALIC),
        ])

        self.split_nodes_check("_Italicize_ some text", "_", TextType.ITALIC, [
            TextNode("Italicize", TextType.ITALIC),
            TextNode(" some text", TextType.TEXT),
        ])

    def test_split_nodes_delimiter_multi(self):
        self.split_nodes_check("This is text with a `code block` word, but also `another code block`", "`", TextType.CODE, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word, but also ", TextType.TEXT),
            TextNode("another code block", TextType.CODE),
        ])

        self.split_nodes_check("Some **bold** text, and then more **bold** text", "**", TextType.BOLD, [
            TextNode("Some ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text, and then more ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ])

        self.split_nodes_check("Some _italic_ text, and then more _italic_ text", "_", TextType.ITALIC, [
            TextNode("Some ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text, and then more ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ])

        self.split_nodes_check("**bold** not **bold** not **bold**", "**", TextType.BOLD, [
            TextNode("bold", TextType.BOLD),
            TextNode(" not ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" not ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ])

        self.split_nodes_check("_italic_ not _italic_ not _italic_", "_", TextType.ITALIC, [
            TextNode("italic", TextType.ITALIC),
            TextNode(" not ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" not ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
        ])

    def test_split_nodes_delimiter_combo(self):

        s = "this is **bold text** and this is _italic text_"
        self.split_nodes_check(s, "_", TextType.ITALIC, [
            TextNode("this is **bold text** and this is ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
        ])

        self.split_nodes_check(s, "**", TextType.BOLD, [
            TextNode("this is ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" and this is _italic text_", TextType.TEXT),
        ])

    def split_nodes_check(self, text, delimiter, text_type, expected_nodes):
        node = TextNode(text, TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], delimiter, text_type)
        self.assertEqual(len(new_nodes), len(expected_nodes))
        for i, n in enumerate(new_nodes):
            self.assertEqual(new_nodes[i].text, expected_nodes[i].text)
            self.assertEqual(new_nodes[i].text_type, expected_nodes[i].text_type)



if __name__ == "__main__":
    unittest.main()
