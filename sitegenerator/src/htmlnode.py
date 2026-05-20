from textnode import TextType
class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    
    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props == None or len(self.props) == 0:
            return ""

        string = ""
        for prop in self.props:
            string += (f' {prop}="{self.props[prop]}"')
        return string
    
    def __repr__(self):
        return f"HTMLnode({self.tag}, {self.value}, {self.children}, {self.props})"

    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError
        elif self.tag is None:
            return self.value
        else:
            if self.tag == "a":
                return f"<a {self.props_to_html()}>{self.value}</a>"
            elif self.tag=="img":
                return f'<img{self.props_to_html()} />'
            else:
                return f"<{self.tag}>{self.value}</{self.tag}>"
    
    def text_node_to_html_node(text_node):
        match text_node.text_type:
            case TextType.TEXT:
                return LeafNode(None, text_node.text)
            case TextType.BOLD:
                return LeafNode("b", text_node.text)
            case TextType.ITALIC:
                return LeafNode("i", text_node.text)
            case TextType.CODE:
                return LeafNode("code", text_node.text)
            case TextType.LINK:
                return LeafNode("a", text_node.text, {"href":text_node.url})
            case TextType.IMAGE:
                return LeafNode("img", "", {"src":text_node.url, "alt":text_node.text})

    
    def __repr__(self):
        return f"Leafnode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("Missing tag")
        if self.children is None:
            raise ValueError("Missing children")
        string = ""
        for child in self.children:
            string += child.to_html()

        return f"<{self.tag}>{string}</{self.tag}>"
            


