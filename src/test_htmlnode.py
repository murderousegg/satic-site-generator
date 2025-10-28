import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    def test_defaults_and_repr_empty_props(self):
        n = HTMLNode()
        self.assertEqual(n.props_to_html(), "")
        self.assertEqual(repr(n), "tag=None, value=None, children=None, props=")

    def test_to_html_raises_not_implemented(self):
        n = HTMLNode()
        with self.assertRaises(NotImplementedError):
            n.to_html()

    def test_props_to_html_single_prop_trailing_space(self):
        n = HTMLNode(props={"class": "btn"})
        self.assertEqual(n.props_to_html(), 'class="btn" ')
        self.assertTrue(n.props_to_html().endswith(" "))

    def test_props_to_html_empty_dict(self):
        n = HTMLNode(props={})
        self.assertEqual(n.props_to_html(), "")

    def test_props_to_html_multiple_props_order_preserved(self):
        n = HTMLNode(props={"id": "hero", "class": "btn", "data-x": "1"})
        self.assertEqual(n.props_to_html(), 'id="hero" class="btn" data-x="1" ')

    def test_props_to_html_non_string_values(self):
        n = HTMLNode(props={"tabindex": 0, "data-count": 42})
        self.assertEqual(n.props_to_html(), 'tabindex="0" data-count="42" ')

    def test_props_to_html_boolean_values(self):
        n = HTMLNode(props={"hidden": True, "draggable": False})
        self.assertEqual(n.props_to_html(), 'hidden="True" draggable="False" ')

    def test_repr_includes_children_structure(self):
        c1 = HTMLNode(tag="span", value="x")
        c2 = HTMLNode(tag="b", value="y")
        n = HTMLNode(tag="div", children=[c1, c2], props={"id": "p"})
        r = repr(n)
        self.assertIn("tag=div", r)
        self.assertIn("children=[", r)
        self.assertIn("tag=span", r)
        self.assertIn("tag=b", r)
        self.assertIn('props=id="p" ', r)

    def test_props_to_html_special_chars_unescaped(self):
        # Current implementation does not escape quotes in values.
        n = HTMLNode(props={"title": 'He said "hi"'})
        self.assertEqual(n.props_to_html(), 'title="He said "hi"" ')

    def test_large_prop_set_spacing(self):
        props = {f"data-k{i}": f"v{i}" for i in range(5)}
        n = HTMLNode(props=props)
        out = n.props_to_html()
        for i in range(5):
            self.assertIn(f'data-k{i}="v{i}" ', out)
        self.assertNotIn("  ", out)

if __name__ == "__main__":
    unittest.main()