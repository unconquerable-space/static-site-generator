
class HTMLNode:
    def __init__(self, tag, value, children, props):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props == None:
            return ""
        output=[]
        for k, v in self.props.items():
            output.append(f"{k}=\"{v}\"")
        return ' '.join(output)

    def __repr__(self):
        return str(self)

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
       if self.value == None:
           raise ValueError()
       if self.tag == None:
           return self.value

       output = "<" + self.tag
       props = self.props_to_html()
       if len(props) > 0:
           output += " " + props
       output += ">" + self.value + "</" + self.tag + ">"
       return output

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
       if self.children == None:
           raise ValueError("The `children` property was set to None")
       if self.tag == None:
           raise ValueError("The `tag` property was set to None")

       output = "<" + self.tag
       props = self.props_to_html()
       if len(props) > 0:
           output += " " + props
       output += ">" 
       for child in self.children:
           output += child.to_html()
       output += "</" + self.tag + ">"
       return output

