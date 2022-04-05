import ast
import astunparse
import black


def ast_name(name):
    return ast.Name(id=name)


def ast_module(*body):
    return ast.Module(body=ast_body(body))


def ast_body(body):
    return [item for item in body if item]


def ast_import(module, name=None, alias=None):
    if name:
        if isinstance(name, dict):
            names = [(n, a) for n, a in name.items()]
        elif isinstance(name, (list, tuple)):
            names = [(n, None) for n in name]
        else:
            names = [(name, alias)]
        return ast.ImportFrom(
            module=module,
            names=[ast.alias(name=n, asname=a) for n, a in names],
            level=0,
        )
    else:
        return ast.Import(
            names=[ast.alias(name=module, asname=alias)], level=0
        )


def ast_expr(val):
    return ast.Expr(val)


def ast_call(fname, *args, comma=None, **kwargs):
    keywords = ast_keywords(kwargs)
    if comma or (kwargs and len(args) + len(kwargs) > 1):
        keywords.append(ast_trailing_comma())
    return ast.Call(
        func=ast_name(fname),
        args=ast_args(args),
        keywords=keywords,
    )


def ast_assign(name, val):
    if val is None:
        return None
    return ast.Assign(
        targets=[ast_name(name)],
        value=ast_val(val),
    )


def ast_val(val):
    if isinstance(val, ast.AST):
        return val
    else:
        return ast.Constant(val, kind=None)


def ast_args(args):
    return [ast_val(arg) for arg in args]


def ast_keywords(kwargs):
    keywords = []
    for key, val in kwargs.items():
        keywords.append(
            ast.keyword(
                key,
                ast_val(val),
            )
        )
    return keywords


def ast_class(name, bases, *body):
    return ast.ClassDef(
        name=name,
        bases=[ast_name(base) for base in bases],
        keywords=[],
        starargs=[],
        kwargs=[],
        body=ast_body(body),
        decorator_list=[],
    )


def ast_def(name, args, *body):
    return ast.FunctionDef(
        name=name,
        args=ast.arguments(
            posonlyargs=[],
            args=[ast.arg(arg=arg, annotation=None) for arg in args],
            vararg=None,
            kwonlyargs=[],
            kw_defaults=[],
            kwarg=None,
            defaults=[],
        ),
        body=ast_body(body),
        decorator_list=[],
        returns=None,
    )


def ast_return(value):
    return ast.Return(value)


def ast_trailing_comma():
    return ast.Name(id="")


def ast_newline():
    return ast.Expr(ast.Name(id=""))


def ast_comment(comment):
    return ast.Name(id="# " + comment)


def ast_list(args):
    return ast.List(elts=ast_args(list(args)) + [ast_trailing_comma()])


def ast_tuple(args):
    return ast.Tuple(elts=ast_args(list(args)) + [ast_trailing_comma()])


def ast_dict(obj=None, **kwargs):
    if obj:
        kwargs = obj
    return ast.Dict(
        keys=ast_args(kwargs.keys()) + [None],
        values=ast_args(kwargs.values()) + [ast_trailing_comma()],
    )


def unparse(tree):
    code = astunparse.unparse(tree).replace(", **}", ",}")
    return black.format_str(code, mode=black.FileMode())
