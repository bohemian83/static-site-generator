from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode


def main():
    node = TextNode("dummy text", TextType.URL, url="http://www.example.com")
    node1 = HTMLNode(
        "a",
        "http://google.com",
        children=None,
        props={"href": "http://google.com", "target": "_blank"},
    )
    node3 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})


main()
