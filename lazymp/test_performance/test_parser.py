import parser
import sys
import ast 
text = open(sys.argv[1]).read()
st = ast.parse(text)

class v(ast.NodeVisitor):
    def generic_visit(self, node):
        try:
            print node.body
        except:
            pass
        # print node._fields
        ast.NodeVisitor.generic_visit(self, node)

x = v()
x.visit(st)
