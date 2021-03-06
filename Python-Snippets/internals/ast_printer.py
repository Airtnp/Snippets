from ast import *
import sys

def printAst(ast, indent='  ', stream=sys.stdout, initlevel=0):
    "Pretty-print an AST to the given output stream."
    rec_node(ast, initlevel, indent, stream.write)
    stream.write('\n')

def rec_node(node, level, indent, write, attr_name = None):
    "Recurse through a node, pretty-printing it."
    pfx = indent * level
    if isinstance(node, AST):
        children = [(child, node.__dict__[child]) for child in node._fields]
        if children == []:
            write(pfx)
            if attr_name:
                write(attr_name)
                write(' = ')
            write(node.__class__.__name__)
            write(' ()')
            return
        write(pfx)
        if attr_name:
            write(attr_name)
            write(' = ')
        write(node.__class__.__name__)
        write(' (')
        for i, tchild in enumerate(children):
            tname, child = tchild
            if i != 0:
                write(',')
            write('\n')
            if isinstance(child, AST):
                rec_node(child, level + 1, indent, write, tname)
            elif isinstance(child, list):
                if child != []:
                    write(pfx)
                    write(indent)
                    write(tname)
                    write(' = [')
                    for j, elem in enumerate(child):
                        if j != 0:
                            write(',')
                        write('\n')
                        rec_node(elem, level + 2, indent, write)
                    write('\n')
                    write(pfx)
                    write(indent)
                    write(']')
                else:
                    write(pfx)
                    write(indent)
                    write(tname)
                    write(' = ')
                    write('[]')
            else:
                write(pfx)
                write(indent)
                write(tname)
                write(' = ')
                write(repr(child))
        write('\n')
        write(pfx)
        write(')')
    else:
        write(pfx)
        if attr_name:
            write(attr_name)
            write(' = ')
        write(repr(node))
