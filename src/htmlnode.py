from textnode import TextNode, TextType


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        html_str = ""
        if self.props:
            for k in self.props:
                html_str += f' {k}="{self.props[k]}"'

        return html_str

    def __eq__(self, o):
        if (
            self.tag == o.tag
            and self.value == o.value
            and self.children == o.children
            and self.props == o.props
        ):
            return True
        return False

    def __repr__(self):
        return f'HTMLNode(tag="{self.tag}", value="{self.value}", children={self.children}, props={self.props})'


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Invalid HMTL: no value")

        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Invalid HMTL: no tag")

        if self.children is None:
            raise ValueError("invalid HTML: no children")

        tag_html = ""
        for child in self.children:
            tag_html += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{tag_html}</{self.tag}>"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    try:
        text_type = TextType(text_node.text_type)
        match text_type:
            case TextType.TEXT:
                return LeafNode(tag=None, value=text_node.text, props=None)
            case TextType.BOLD:
                return LeafNode(tag="b", value=text_node.text, props=None)
            case TextType.ITALIC:
                return LeafNode(tag="i", value=text_node.text, props=None)
            case TextType.CODE:
                return LeafNode(tag="code", value=text_node.text, props=None)
            case TextType.LINK:
                return LeafNode(
                    tag="a", value=text_node.text, props={"href": text_node.url}
                )
            case TextType.IMAGE:
                return LeafNode(
                    tag="img",
                    value="",
                    props={"src": text_node.url, "alt": text_node.text},
                )
    except Exception as e:
        return f"Error: {e}"
