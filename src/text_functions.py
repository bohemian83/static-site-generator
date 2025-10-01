import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Splits a list of TextNodes based on the delimiter.
    Returns a new list with TextNodes.
    """
    new_nodes = []
    for node in old_nodes:
        if node.text.count(delimiter) % 2 != 0:
            raise Exception("Unclosed delimiter.")

        splits = node.text.split(delimiter)
        for i in range(len(splits)):
            if i % 2 == 0 and splits[i] != "":
                new_nodes.append(TextNode(splits[i], node.text_type))
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
