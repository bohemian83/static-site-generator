from htmlnode import HTMLNode
import unittest


class HTMLNodeTest(unittest.TestCase):
    def test_eq(self):
        children = [HTMLNode("h1", "heading1"), HTMLNode("h2", "heading2")]
        node = HTMLNode(
            tag="p", value="paragraph", children=children, props={"id": "id1"}
        )
        node2 = HTMLNode(
            tag="p", value="paragraph", children=children, props={"id": "id1"}
        )
        self.assertEqual(node, node2)

    def test_uneq(self):
        children = [HTMLNode("h1", "heading1"), HTMLNode("h2", "heading2")]
        children2 = [HTMLNode("h2", "heading2"), HTMLNode("h2", "heading2")]
        node = HTMLNode("p", "paragraph", children, props={"id": "id1"})
        node2 = HTMLNode("p", "paragraph", children, props={"id": "id2"})
        node3 = HTMLNode("p", "paragraph", children2, props={"id": "id2"})
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node, node2)

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "a",
            "http://google.com",
            children=None,
            props={"href": "http://google.com", "target": "_blank"},
        )
        self.assertEqual(
            repr(node),
            "HTMLNode(tag=\"a\", value=\"http://google.com\", children=None, props={'href': 'http://google.com', 'target': '_blank'})",
        )

    def test_props_to_html(self):
        node = HTMLNode(
            "a",
            "http://google.com",
            children=None,
            props={"href": "http://google.com", "target": "_blank"},
        )
        props = node.props_to_html()
        self.assertEqual(
            props,
            ' href="http://google.com" target="_blank"',
        )
