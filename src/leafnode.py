from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, children=None, props=props)

    def to_html(self):
        if self.value == None: 
            raise ValueError
        if not self.tag:
            return f"{self.value}"
        if self.tag == "img":
            return f"<{self.tag} {self.props_to_html()} />"
        if self.tag == "a":
            return f"<{self.tag} href={self.props['url']}>{self.value}</{self.tag}>"
        return f"<{self.tag}>{self.value}</{self.tag}>"