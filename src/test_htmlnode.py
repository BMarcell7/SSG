import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextType

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_single(self):
        node = HTMLNode(props={"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')

    def test_props_to_html_multiple(self):
        node = HTMLNode(props={"href": "https://example.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com" target="_blank"')

    def test_repr(self):
        node = HTMLNode(tag="div", value="Hello World")
        self.assertEqual(
            repr(node),
            "HTMLNode(tag=div, value=Hello World, children=[], props={})"
        )

class TestLeafNode(unittest.TestCase):
    def test_basic_rend(self):
        leaf = LeafNode("p", "This is a paragraph.")
        assert leaf.to_html() == "<p>This is a paragraph.</p>"
        
    def test_rendering_with_attributes(self):
        leaf = LeafNode("a", "Click me!", props={"href": "https://www.google.com"})
        self.assertEqual(leaf.to_html(), '<a href="https://www.google.com">Click me!</a>')
        
    def test_rend_wo_tag(self):
        leaf = LeafNode(None, "Raw text")
        assert leaf.to_html() == "Raw text"
        
class TestParentNode(unittest.TestCase):
    
    def test_basic_rendering(self):
        leaf1 = LeafNode("b", "Bold text")
        leaf2 = LeafNode(None, "Normal text")
        parent = ParentNode("p", [leaf1, leaf2])
        self.assertEqual(parent.to_html(), "<p><b>Bold text</b>Normal text</p>")
    
    def test_missing_tag(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("b", "Content")])
    
    def test_missing_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", [])

    def test_rendering_with_nested_parent_nodes(self):
        leaf1 = LeafNode("b", "Bold text")
        parent1 = ParentNode("div", [leaf1])
        leaf2 = LeafNode("i", "Italic text")
        parent2 = ParentNode("section", [parent1, leaf2])
        self.assertEqual(parent2.to_html(), "<section><div><b>Bold text</b></div><i>Italic text</i></section>")

class TestTextNodeToHtmlNode(unittest.TestCase):

    def test_text_type(self):
        # Test TEXT type
        text_node = {"type": TextType.TEXT, "content": "This is raw text"}
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "This is raw text")

    def test_bold_type(self):
        # Test BOLD type
        text_node = {"type": TextType.BOLD, "content": "Bold text"}
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<b>Bold text</b>")

    def test_italic_type(self):
        # Test ITALIC type
        text_node = {"type": TextType.ITALIC, "content": "Italic text"}
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<i>Italic text</i>")

    def test_code_type(self):
        # Test CODE type
        text_node = {"type": TextType.CODE, "content": "Code snippet"}
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<code>Code snippet</code>")

    def test_link_type(self):
        # Test LINK type
        text_node = {"type": TextType.LINK, "content": "Click me", "href": "https://example.com"}
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), '<a href="https://example.com">Click me</a>')

    def test_image_type(self):
        # Test IMAGE type
        text_node = {"type": TextType.IMAGE, "src": "image.jpg", "alt": "An image"}
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), '<img src="image.jpg" alt="An image">')

    def test_missing_href_for_link(self):
        # Test missing 'href' for LINK type
        text_node = {"type": TextType.LINK, "content": "Click me"}
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(text_node)
        self.assertEqual(str(context.exception), "LINK type must have an 'href' attribute")

    def test_missing_src_or_alt_for_image(self):
        # Test missing 'src' or 'alt' for IMAGE type
        text_node = {"type": TextType.IMAGE, "src": "image.jpg"}
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(text_node)
        self.assertEqual(str(context.exception), "IMAGE type must have both 'src' and 'alt' attributes")

    def test_unknown_text_type(self):
        # Test unknown TextType
        text_node = {"type": "UNKNOWN_TYPE", "content": "Some content"}
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(text_node)
        self.assertEqual(str(context.exception), "Unknown TextType: UNKNOWN_TYPE")
        
if __name__ == "__main__":
    unittest.main()