from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError
        start_tag = f"<{self.tag}>"
        child_tags=""
        for child in self.children:
            child_tags+=child.to_html()
        end_tag = f"</{self.tag}>"
        if self.tag == "img":
            return f"<{self.tag} {self.props_to_html()} />"
        if self.tag == "a":
            return f"<{self.tag} href={self.props['url']}>{self.value}</{self.tag}>"
        return start_tag+child_tags+end_tag