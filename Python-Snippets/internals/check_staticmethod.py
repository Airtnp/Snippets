import ast
import six

class StaticmethodChecker(object):
    def __init__(self, tree, filename):
        self.tree = tree
 
    def run(self):
        for stmt in ast.walk(self.tree):
        # Ignore non-class
    if not isinstance(stmt, ast.ClassDef):
        continue
    # If it's a class, iterate over its body member to find methods
    for body_item in stmt.body:
        # Not a method, skip
        if not isinstance(body_item, ast.FunctionDef):
            continue
        # Check that it has a decorator
        for decorator in body_item.decorator_list:
            if (isinstance(decorator, ast.Name)
               and decorator.id == 'staticmethod'):
                # It's a static function, it's OK
                break
        else:
            try:
                first_arg = body_item.args.args[0]
            except IndexError:
                yield (
                    body_item.lineno,
                    body_item.col_offset,
                    "H905: method misses first argument",
                    "H905",
                )
                # Check next method
                continue
            for func_stmt in ast.walk(body_item):
                if six.PY3:
                    if (isinstance(func_stmt, ast.Name)
                       and first_arg.arg == func_stmt.id):
                        # The first argument is used, it's OK
                        break
                else:
                    if (func_stmt != first_arg
                       and isinstance(func_stmt, ast.Name)
                       and func_stmt.id == first_arg.id):
                        # The first argument is used, it's OK
                        break
            else:
                yield (
                    body_item.lineno,
                    body_item.col_offset,
                    "H904: method should be declared static",
                    "H904",
                )