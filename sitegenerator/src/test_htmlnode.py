import unittest
import functions

from blocktype import BlockType
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType


class TestHTMLNode(unittest.TestCase):

    def test1(self):
        node1 = HTMLNode("p", "This is a value", None, {"href": "https://www.google.com", "target": "_blank",})
        #print(node1)
    
    def test2(self):
        node1 = HTMLNode("p", "This is a value", None, {"href": "https://www.google.com", "target": "_blank",})
        #print(node1.props_to_html())

    def test3(self):
        node1 = HTMLNode()
        #print(node1)

    def test_leafnode_img(self):
        node = LeafNode("img", "", {"src": "url/of/image.jpg", "alt":"Description of image"})
        self.assertEqual(node.to_html(), '<img src="url/of/image.jpg" alt="Description of image" />')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        #print(node)
        #print(node.to_html)
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Hello, world!")
        #print(node)
        #print(node.to_html)
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        #print(node)
        #print(node.to_html)
        self.assertEqual(node.to_html(), '<a  href="https://www.google.com">Click me!</a>')
    
    
    def test_parent_node(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ]
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_parent_node_with_none_children(self):
        node = ParentNode("p", None)
        with self.assertRaisesRegex(ValueError,"Missing children"):
            node.to_html()
    
    def test_parent_node_with_none_tag(self):
        node = ParentNode(None, [LeafNode("b", "bold text")])
        with self.assertRaisesRegex(ValueError,"Missing tag"):
            node.to_html()
    
    def test_parent_node_with_props(self):
        node = ParentNode("p", [LeafNode("a", "Click me!", {"href": "https://www.google.com"})])
        self.assertEqual(node.to_html(), '<p><a  href="https://www.google.com">Click me!</a></p>')
    

    
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = functions.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = functions.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is a italic node", TextType.ITALIC)
        html_node = functions.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = functions.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.google.com")
        html_node = functions.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href":"https://www.google.com"})

    def test_image(self):
        node = TextNode("This is a image node", TextType.IMAGE, "url/of/image.jpg")
        html_node = functions.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src":"url/of/image.jpg", "alt":"This is a image node"})
    
    def test_extract_markdown_images(self):
        matches = functions.extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = functions.extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_markdown_images_multi(self):
        matches = functions.extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_links_multi(self):
        matches = functions.extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = functions.split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = functions.split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_links_no_links(self):
        node = TextNode(
            "This is text with a link and another link",
            TextType.TEXT,
        )
        new_nodes = functions.split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link and another link", TextType.TEXT),

            ],
            new_nodes,
        )

    def test_split_images_no_images(self):
        node = TextNode(
            "This is text with an image and another image",
            TextType.TEXT,
        )
        new_nodes = functions.split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an image and another image", TextType.TEXT),

            ],
            new_nodes,
        )

    def test_split_image_at_start(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = functions.split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links_at_start(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = functions.split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_image_btb(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = functions.split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links_btb(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png)[second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = functions.split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = functions.split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_links_single(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = functions.split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )
    
    def test_split_images(self):
        node = TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png")
        new_nodes = functions.split_nodes_image([node])
        self.assertListEqual([TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png")], new_nodes)

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = functions.text_to_textnodes(text)
        self.assertListEqual(new_nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ] )

    def test_text_to_textnodes_all_bold(self):
        text = "This is **text** with a **bold** word, and **another**, and **yet** another, and lastly **bold sentence of nonsense**"
        new_nodes = functions.text_to_textnodes(text)
        self.assertListEqual(new_nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word, and ", TextType.TEXT),
            TextNode("another", TextType.BOLD),
            TextNode(", and ", TextType.TEXT),
            TextNode("yet", TextType.BOLD),
            TextNode(" another, and lastly ", TextType.TEXT),
            TextNode("bold sentence of nonsense", TextType.BOLD),
        ] )

    def test_text_to_textnodes_single(self):
        text = "**bold**"
        new_nodes = functions.text_to_textnodes(text)
        self.assertListEqual(new_nodes, [
            TextNode("bold", TextType.BOLD),
        ] )

    def test_text_to_textnodes_single_mistake(self):
        text = "**bold"
        with self.assertRaisesRegex(Exception, "Closing delimiter not found"):
                functions.text_to_textnodes(text)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = functions.markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md ="""
This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items
"""
        blocks = functions.markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


    def test_markdown_to_blocks_single_line(self):
        md = "Just a single paragraph with no blank lines."
        blocks = functions.markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Just a single paragraph with no blank lines."
            ],
        )

    def test_block_to_block_type_heading(self):
        md ="# Heading something"
        blocktype = functions.block_to_block_type(md)
        self.assertEqual(
            blocktype, BlockType.HEADING
        )
    def test_block_to_block_type_incorrect_heading(self):
        md ="####### Heading something"
        blocktype = functions.block_to_block_type(md)
        self.assertEqual(
            blocktype, BlockType.PARAGRAPH
        )

    def test_block_to_block_type_multiline_heading(self):
        md ="####### Heading something\nsome more stuff"
        blocktype = functions.block_to_block_type(md)
        self.assertEqual(
            blocktype, BlockType.PARAGRAPH
        )

    def test_block_to_block_type_code(self):
        md ="```\ncode\n```"
        blocktype = functions.block_to_block_type(md)
        self.assertEqual(
            blocktype, BlockType.CODE
        )
    
    def test_block_to_block_type_incorrect_code(self):
        md ="```\n```"
        blocktype = functions.block_to_block_type(md)
        self.assertEqual(
            blocktype, BlockType.PARAGRAPH
        )

    def test_block_to_block_type_quote(self):
        md =">This is a quote"
        blocktype = functions.block_to_block_type(md)
        self.assertEqual(
            blocktype, BlockType.QUOTE
        )

    def test_block_to_block_type_unordered_list(self):
        md ="- item 1\n- item 3\n- item 2\n- item 5\n- item 4"
        blocktype = functions.block_to_block_type(md)
        self.assertEqual(
            blocktype, BlockType.UNORDERED_LIST
        )

    def test_block_to_block_type_ordered_list(self):
        md ="1. item 1\n2. item 2\n3. item 3"
        blocktype = functions.block_to_block_type(md)
        self.assertEqual(
            blocktype, BlockType.ORDERED_LIST
        )

    def test_block_to_block_type_ordered_list_incorrect(self):
        md ="1. item 1\n3. item 2\n2. item 3"
        blocktype = functions.block_to_block_type(md)
        self.assertEqual(
            blocktype, BlockType.PARAGRAPH
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

        """

        node = functions.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
        """

        node = functions.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
        
    def test_mixed_block(self):
        md = """
# Heading

This is a paragraph with **bold** and _italic_.

- list item one
- list item two

> a quote line
> another quote line

1. first
2. second
        """
        node = functions.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading</h1><p>This is a paragraph with <b>bold</b> and <i>italic</i>.</p><ul><li>list item one</li><li>list item two</li></ul><blockquote>a quote line another quote line</blockquote><ol><li>first</li><li>second</li></ol></div>"
        )

    def test_extract_title(self):
        md = "# Hello"
        title = functions.extract_title(md)
        self.assertEqual(
            title,
            "Hello"
        )
    
    def test_extract_title_double_titles(self):
        md = """
# Hello

# Hello too
        """
        title = functions.extract_title(md)
        self.assertEqual(
            title,
            "Hello"
        )

    def test_extract_title_skip_title(self):
        md = """
## Hello

# Hello too
        """
        title = functions.extract_title(md)
        self.assertEqual(
            title,
            "Hello too"
        )


    def test_extract_title_incorrect(self):
        md = "## Hello"
        with self.assertRaisesRegex(Exception,"No h1 header"):
            functions.extract_title(md)
    
    def test_extract_title_whitespace(self):
        md = "   #    Hello    "
        title = functions.extract_title(md)
        self.assertEqual(
            title,
            "Hello"
        )


if __name__ == "__main__":
    unittest.main()