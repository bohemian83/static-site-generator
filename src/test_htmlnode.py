from htmlnode import HTMLNode, LeafNode, ParentNode
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


class LeafNodeTest(unittest.TestCase):
    def test_leaf_to_html_no_props(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

        node2 = LeafNode("b", "Bold text")
        self.assertEqual(node2.to_html(), "<b>Bold text</b>")

    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        # Note: This test will currently fail due to bug in LeafNode.to_html()
        expected = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node.to_html(), expected)

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just some text")
        self.assertEqual(node.to_html(), "Just some text")

        node2 = LeafNode(value="Another text node")
        self.assertEqual(node2.to_html(), "Another text node")

    def test_leaf_to_html_no_value_raises_error(self):
        node = LeafNode("p")
        with self.assertRaises(ValueError):
            node.to_html()

        node2 = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node2.to_html()

    def test_leaf_to_html_empty_value_raises_error(self):
        node = LeafNode("p", "")
        with self.assertRaises(ValueError):
            node.to_html()

    def test_multiple_props(self):
        props = {"class": "btn", "id": "submit-btn", "disabled": "true"}
        node = LeafNode("button", "Submit", props)
        result = node.to_html()
        # Note: This will fail due to the bug - props aren't being used
        self.assertIn('class="btn"', result)
        self.assertIn('id="submit-btn"', result)
        self.assertIn('disabled="true"', result)

