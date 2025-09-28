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
