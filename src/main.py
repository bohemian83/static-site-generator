from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from text_functions import split_nodes_delimiter, extract_markdown_images


def main():
    # node = TextNode("dummy text", TextType.URL, url="http://www.example.com")
    # node1 = HTMLNode(
    #     "a",
    #     "http://google.com",
    #     children=None,
    #     props={"href": "http://google.com", "target": "_blank"},
    # )
    # node3 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    # grandchild_node = LeafNode("b", "grandchild")
    # child_node = ParentNode("span", [grandchild_node])
    # parent_node = ParentNode("div", [child_node])
    # print(child_node.to_html())

    # node4 = TextNode("This is text with a `code block` word", TextType.TEXT)
    # node5 = TextNode("This is text with an *italic* word", TextType.TEXT)
    # node6 = TextNode("This is text with a **bold** word", TextType.TEXT)
    # node = TextNode("text **unclosed delimiter", TextType.CODE)
    # old_nodes = [node]
    # new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)

    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
    print(extract_markdown_images(text))


main()
