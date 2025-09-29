from htmlnode import HTMLNode, LeafNode, ParentNode
import unittest


# TODO: Add more ParentNode tests
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

    def test_to_html_with_children(self):
        """Test basic parent with single child"""
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        """Test nested ParentNodes"""
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_children(self):
        """Test parent with multiple children"""
        child1 = LeafNode("b", "Bold text")
        child2 = LeafNode("i", "Italic text")
        child3 = LeafNode("span", "Normal text")
        parent = ParentNode("div", [child1, child2, child3])
        expected = (
            "<div><b>Bold text</b><i>Italic text</i><span>Normal text</span></div>"
        )
        self.assertEqual(parent.to_html(), expected)

    def test_to_html_no_tag_raises_error(self):
        """Test that missing tag raises ValueError"""
        child = LeafNode("span", "child")
        parent = ParentNode(None, [child])
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_to_html_with_props(self):
        """Test parent node with props"""
        child = LeafNode("p", "Content")
        parent = ParentNode("div", [child], {"class": "container"})
        expected = '<div class="container"><p>Content</p></div>'
        self.assertEqual(parent.to_html(), expected)

    def test_to_html_with_multiple_props(self):
        """Test parent node with multiple props"""
        child = LeafNode("p", "Content")
        props = {"class": "container", "id": "main", "data-test": "value"}
        parent = ParentNode("div", [child], props)
        result = parent.to_html()
        self.assertIn("<div", result)
        self.assertIn('class="container"', result)
        self.assertIn('id="main"', result)
        self.assertIn('data-test="value"', result)
        self.assertIn("<p>Content</p>", result)

    def test_to_html_deeply_nested(self):
        """Test deeply nested structure"""
        deepest = LeafNode("span", "deep")
        level3 = ParentNode("p", [deepest])
        level2 = ParentNode("div", [level3])
        level1 = ParentNode("section", [level2])
        expected = "<section><div><p><span>deep</span></p></div></section>"
        self.assertEqual(level1.to_html(), expected)

    def test_to_html_with_text_nodes(self):
        """Test parent with text-only children (no tags)"""
        text_node = LeafNode(None, "Just text")
        bold_node = LeafNode("b", "Bold")
        parent = ParentNode("p", [text_node, bold_node])
        expected = "<p>Just text<b>Bold</b></p>"
        self.assertEqual(parent.to_html(), expected)

    def test_to_html_mixed_children(self):
        """Test parent with mix of LeafNode and ParentNode children"""
        leaf1 = LeafNode("span", "text1")
        leaf2 = LeafNode("b", "bold")
        nested_parent = ParentNode("div", [leaf2])
        parent = ParentNode("section", [leaf1, nested_parent])
        expected = "<section><span>text1</span><div><b>bold</b></div></section>"
        self.assertEqual(parent.to_html(), expected)

    def test_constructor_sets_children_correctly(self):
        """Test that constructor properly sets children"""
        child1 = LeafNode("p", "Test")
        child2 = LeafNode("span", "Test2")
        parent = ParentNode("div", [child1, child2])
        self.assertEqual(len(parent.children), 2)
        self.assertEqual(parent.children[0], child1)
        self.assertEqual(parent.children[1], child2)
        self.assertIsNone(parent.value)  # ParentNode should have no value

    def test_to_html_empty_children_list(self):
        """Test parent with empty children list"""
        parent = ParentNode("div", [])
        # This should return empty div tags
        self.assertEqual(parent.to_html(), "<div></div>")

    def test_to_html_complex_structure(self):
        """Test a more complex, realistic HTML structure"""
        # <div class="container">
        #   <h1>Title</h1>
        #   <p>Text with <b>bold</b> and <i>italic</i></p>
        # </div>
        title = LeafNode("h1", "Title")
        bold = LeafNode("b", "bold")
        italic = LeafNode("i", "italic")
        text1 = LeafNode(None, "Text with ")
        text2 = LeafNode(None, " and ")
        paragraph = ParentNode("p", [text1, bold, text2, italic])
        container = ParentNode("div", [title, paragraph], {"class": "container"})

        expected = '<div class="container"><h1>Title</h1><p>Text with <b>bold</b> and <i>italic</i></p></div>'
        self.assertEqual(container.to_html(), expected)
