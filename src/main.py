from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode


def main():
    node = TextNode("dummy text", TextType.URL, url="http://www.example.com")
    node1 = HTMLNode(
        "a",
        "http://google.com",
        children=None,
        props={"href": "http://google.com", "target": "_blank"},
    )
    node3 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    grandchild_node = LeafNode("b", "grandchild")
    child_node = ParentNode("span", [grandchild_node])
    parent_node = ParentNode("div", [child_node])
    print(parent_node.to_html())


main()
