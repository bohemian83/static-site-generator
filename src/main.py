from textnode import TextNode, TextType


def main():
    node = TextNode("dummy text", TextType.URL, url="http://www.example.com")
    print(node)


main()
