import unittest

from textnode import TextNode, TextType
from functions import split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_url(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node, node2)
    
    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    
    def test_diftext(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_split_nodes_code(self):
        node = [
            TextNode("This is text with a `code block` word", TextType.TEXT)
        ]
        correct_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter(node, "`", TextType.CODE), correct_nodes)

    def test_split_nodes_bold(self):
        node = [
            TextNode("This is text with a **bold** word", TextType.TEXT)
        ]
        correct_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter(node, "**", TextType.BOLD), correct_nodes)

    def test_split_nodes_italic(self):
        node = [
            TextNode("This is text with an _italic_ word", TextType.TEXT)
        ]
        correct_nodes = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter(node, "_", TextType.ITALIC), correct_nodes)

    def test_split_nodes_wrong_delimiter(self):
        node = [
            TextNode("This is text with an _italic word", TextType.TEXT)
        ]
        with self.assertRaisesRegex(Exception, "Closing delimiter not found"):
            split_nodes_delimiter(node, "_", TextType.ITALIC)

if __name__ == "__main__":
    unittest.main()