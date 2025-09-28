from textnode import TextNode, TextType
from htmlnode import HTMLNode


def main():
    node = TextNode("dummy text", TextType.URL, url="http://www.example.com")
    node1 = HTMLNode(
        "a",
        "http://google.com",
        children=None,
        props={"href": "http://google.com", "target": "_blank"},
    )
    print(node1.props_to_html())
    print(node)


main()
