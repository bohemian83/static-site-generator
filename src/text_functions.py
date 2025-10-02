import re
from textnode import TextNode, TextType


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

    return blocks
