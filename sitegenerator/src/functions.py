from textnode import TextNode, TextType
from htmlnode import LeafNode, ParentNode
from blocktype import BlockType
import os
import shutil
import re

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src":text_node.url, "alt":text_node.text})
        

    
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        elif delimiter in node.text:
            parts = node.text.split(delimiter)
            if len(parts) % 2 == 0:
                raise Exception("Closing delimiter not found")
            for i, part in enumerate(parts):
                if part == "":
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(part, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(part, text_type))
        else:
            new_nodes.append(node)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        sections = node.text
        if len(images) == 0:
            new_nodes.append(node)
        else:
            for image in images:
                sections = sections.split(f"![{image[0]}]({image[1]})", 1)
                if sections[0]:
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                sections = sections[1]
            if sections:
                new_nodes.append(TextNode(sections, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        sections = node.text
        if len(links) == 0:
            new_nodes.append(node)
        else:
            for link in links:
                sections = sections.split(f"[{link[0]}]({link[1]})", 1)
                if sections[0]:
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                sections = sections[1]
            if sections:
                new_nodes.append(TextNode(sections, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    node = [
        TextNode(text, TextType.TEXT)
    ]
    nodes = split_nodes_delimiter(node, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    good_blocks = []
    for block in blocks:
        block = block.strip()
        if block:
            good_blocks.append(block)
    return good_blocks

def block_to_block_type(block):
    lines = block.split("\n")
    if len(lines) == 1 and lines[0].startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 2 and lines[0].startswith("```") and lines[-1].endswith("```"):
        return BlockType.CODE
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    if all(line.startswith(f"{i}. ") for i, line in enumerate(lines, start=1)):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        blocktype = block_to_block_type(block)
        match(blocktype):
            case BlockType.HEADING:
                level = len(block.split(" ")[0])
                node = ParentNode(f"h{level}", text_to_children(block.removeprefix("#" * level + " ")))
                nodes.append(node)
            case BlockType.CODE:
                text = block.removeprefix("```\n").removesuffix("```")
                textnode = TextNode(text, TextType.CODE)
                nodes.append(ParentNode("pre", [text_node_to_html_node(textnode)]))
            case BlockType.QUOTE:
                lines = [line.removeprefix("> ").removeprefix(">") for line in block.split("\n")]
                nodes.append(ParentNode("blockquote", text_to_children(" ".join(lines))))
            case BlockType.UNORDERED_LIST:
                lines = [line.removeprefix("- ") for line in block.split("\n")]
                list_nodes = []
                for line in lines:
                    list_nodes.append(ParentNode("li", text_to_children(line)))
                nodes.append(ParentNode("ul", list_nodes))
            case BlockType.ORDERED_LIST:
                lines = [line.split(". ", 1)[1] for line in block.split("\n")]
                list_nodes = []
                for line in lines:
                    list_nodes.append(ParentNode("li", text_to_children(line)))
                nodes.append(ParentNode("ol", list_nodes))
            case BlockType.PARAGRAPH:
                node = ParentNode("p", text_to_children(block.replace("\n", " ")))
                nodes.append(node)
    return ParentNode("div", nodes)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

def copy_contents(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)
    copy(src, dest)

def copy(src, dest):
    for file in os.listdir(src):
        file_path = os.path.join(src, file)
        target_path = os.path.join(dest, file)
        print(f"Copying {file_path} to {target_path}")
        if not os.path.isfile(file_path):
            os.mkdir(target_path)
            copy(file_path, target_path)
        else:
            shutil.copy(file_path, target_path)

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        cleaned = block.strip()
        if cleaned.startswith("# "):
            return cleaned.split("\n")[0].removeprefix("#").strip()
    raise Exception("No h1 header")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as g:
        template = g.read()
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as h:
        h.write(template)