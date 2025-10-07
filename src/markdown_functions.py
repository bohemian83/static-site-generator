import re
from enum import Enum
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Splits a list of TextNodes based on the delimiter.
    Returns a new list with TextNodes.
    """
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if node.text.count(delimiter) % 2 != 0:
            raise Exception("Unclosed delimiter.")

        splits = node.text.split(delimiter)
        for i in range(len(splits)):
            if i % 2 == 0 and splits[i] != "":
                new_nodes.append(TextNode(splits[i], TextType.TEXT))
            elif i % 2 == 1:
                new_nodes.append(TextNode(splits[i], text_type))

    return new_nodes


def extract_markdown_images(text):
    """
    Extracts and returns the alt text and url from markdown images.
    """
    matches = re.findall(r"!\[(.+?)?\]\((.+?)\)", text)

    return matches


def extract_markdown_links(text):
    """
    Extracts and returns the anchor text and url from markdown links.
    """
    matches = re.findall(r"\[(.+?)?\]\((.+?)\)", text)

    return matches


def split_nodes_image(old_nodes):
    """
    Splits a list of TextNodes into TEXT and IMAGE TextNodes
    """
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        imgs = extract_markdown_images(node.text)
        if not imgs:
            new_nodes.append(node)
        else:
            sections = re.split(r"(!\[.+?\]\(.+?\))", node.text)
            for section in sections:
                if not section:
                    continue

                img = extract_markdown_images(section)
                if img:
                    new_nodes.append(TextNode(img[0][0], TextType.IMAGE, img[0][1]))
                else:
                    new_nodes.append(TextNode(section, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    """
    Splits a list of TextNodes into TEXT and LINK TextNodes
    """
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
        else:
            sections = re.split(r"(\[.+?\]\(.+?\))", node.text)
            for section in sections:
                if not section:
                    continue

                link = extract_markdown_links(section)
                if link:
                    new_nodes.append(TextNode(link[0][0], TextType.LINK, link[0][1]))
                else:
                    new_nodes.append(TextNode(section, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text):
    """
    Converts markdown text to a list of TextNode objects
    """
    bold_spliter = split_nodes_delimiter(
        [TextNode(text, TextType.TEXT)], "**", TextType.BOLD
    )
    italic_splitter = split_nodes_delimiter(bold_spliter, "_", TextType.ITALIC)
    code_splitter = split_nodes_delimiter(italic_splitter, "`", TextType.CODE)
    image_splitter = split_nodes_image(code_splitter)
    link_splitter = split_nodes_link(image_splitter)

    return link_splitter


def markdown_to_blocks(markdown):
    """
    Splits a markdown text to a list of markdown blocks
    """
    blocks = markdown.split("\n\n")

    stripped_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        stripped_blocks.append(block)

    return stripped_blocks


def block_to_block_type(block):
    """
    Assigns a markdown block to a BlockType enum
    """
    lines = block.splitlines()
    if re.match(r"#{1,6}\s[\w\s]+", block):
        return BlockType.HEADING
    elif re.match(r"`{3}([\s\S]*?)`{3}", block):
        return BlockType.CODE
    elif all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    elif all(line.startswith("- ") for line in lines):
        return BlockType.ULIST
    elif all(line.startswith(f"{i}. ") for i, line in enumerate(lines, start=1)):
        return BlockType.OLIST
    else:
        return BlockType.PARAGRAPH


def block_to_parent_node(block, block_type):
    match block_type:
        case BlockType.HEADING:
            first_line = block.split("\n")[0]
            hash_count = len(first_line) - len(first_line.lstrip("#"))
            return ParentNode(f"h{hash_count}", None)
        case BlockType.CODE:
            return ParentNode("code", None)
        case BlockType.QUOTE:
            return ParentNode("blockquote", None)
        case BlockType.ULIST:
            return ParentNode("ul", None)
        case BlockType.OLIST:
            return ParentNode("ol", None)
        case BlockType.PARAGRAPH:
            return ParentNode("p", None)


def process_paragraph_block(block):
    block = " ".join(block.split())
    textnodes = text_to_textnodes(block)
    leafnodes = list(map(text_node_to_html_node, textnodes))
    return leafnodes


def process_quote_block(block):
    block = " ".join(line.lstrip("> ").strip() for line in block.split("\n"))
    textnodes = text_to_textnodes(block)
    leafnodes = list(map(text_node_to_html_node, textnodes))
    return leafnodes


def process_heading_block(block):
    block = block.lstrip("#").strip()
    textnodes = text_to_textnodes(block)
    leafnodes = list(map(text_node_to_html_node, textnodes))
    return leafnodes


def process_ulist_block(block):
    lines = block.split("\n")
    leafnodes = []
    for line in lines:
        line = line.lstrip("- ")
        line_textnodes = text_to_textnodes(line)
        line_leafnodes = list(map(text_node_to_html_node, line_textnodes))
        leafnodes.append(ParentNode("li", line_leafnodes))

    return leafnodes


def process_olist_block(block):
    lines = block.split("\n")
    leafnodes = []
    for line in lines:
        line = re.sub(r"\d\.\s", "", line)
        line_textnodes = text_to_textnodes(line)
        line_leafnodes = list(map(text_node_to_html_node, line_textnodes))
        leafnodes.append(ParentNode("li", line_leafnodes))

    return leafnodes


def text_to_children(block, block_type):
    if block_type == BlockType.PARAGRAPH:
        nodes = process_paragraph_block(block)
    elif block_type == BlockType.QUOTE:
        nodes = process_quote_block(block)
    elif block_type == BlockType.HEADING:
        nodes = process_heading_block(block)

    if block_type == BlockType.ULIST:
        nodes = process_ulist_block(block)
    elif block_type == BlockType.OLIST:
        nodes = process_olist_block(block)

    return nodes


def code_to_textnode(block):
    """
    Handles multi line code blocks
    """
    block = block.strip()
    lines = block.split("\n")
    if lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].startswith("```"):
        lines = lines[:-1]
    block = "\n".join(lines)
    if block:
        block += "\n"
    return TextNode(block, TextType.CODE)


def markdown_to_html_node(markdown):
    """
    Splits markdown text to blocks and converts it to HTMLNodes
    """
    mk_blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in mk_blocks:
        block_type = block_to_block_type(block)
        block_node = block_to_parent_node(block, block_type)

        if block_type != BlockType.CODE:
            block_node.children = text_to_children(block, block_type)
        else:
            code_textnode = code_to_textnode(block)
            child_code_node = text_node_to_html_node(code_textnode)
            block_node = ParentNode(tag="pre", children=[child_code_node])

        block_nodes.append(block_node)

    return ParentNode(tag="div", children=block_nodes)
