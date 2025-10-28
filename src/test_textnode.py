import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(node, node2)
    
    def test_noneq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    
    def test_dif_str(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a tex node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_none_url(self):
        node = TextNode("This is a text node", TextType.BOLD, url=None)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_img(self):
        node = TextNode("This is a text node", TextType.IMAGE, url="https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {'src': 'https://www.google.com', 'alt': 'This is a text node'})



if __name__ == "__main__":
    unittest.main()