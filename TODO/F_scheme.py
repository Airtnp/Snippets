from ast import *
import dis
import sys
import os

def printAst(ast, indent='  ', stream=sys.stdout, initlevel=0):
    "Pretty-print an AST to the given output stream."
    rec_node(ast, initlevel, indent, stream.write)
    stream.write('\n')

def rec_node(node, level, indent, write, attr_name = None):
    "Recurse through a node, pretty-printing it."
    pfx = indent * level
    write(pfx)
    if attr_name:
        write(attr_name)
        write(' = ')

    if isinstance(node, AST):
        children = [(child, node.__dict__[child]) for child in node._fields]
        write(node.__class__.__name__)
        if children == []:
            write(' ()')
            return
        write(' (')
        for i, tchild in enumerate(children):
            tname, child = tchild
            if i != 0:
                write(',')
            write('\n')
            if isinstance(child, AST):
                rec_node(child, level + 1, indent, write, tname)
            elif isinstance(child, list):
                write(pfx)
                write(indent)
                write(tname)
                write(' = ')
                if child != []:
                    write('[')
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
        write(repr(node))


def walk_ast(filename):
    func_dict = {}
    with open(filename, 'r') as f:
        tree = parse(f.read())
        printAst(tree)
        for stmt in walk(tree):
            if isinstance(stmt, FunctionDef):
                name = stmt.name
                args = stmt.args
                for expr in stmt.body:
                    if isinstance(stmt, Call):
                        pass


if __name__ == "__main__":
    walk_ast("./test.py")