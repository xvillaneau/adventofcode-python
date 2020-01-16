from parsimonious.grammar import Grammar
from parsimonious.nodes import Node


GRAM = Grammar("""
group        = GP_OPEN content_list? GP_END
content_list = content (SEP content)*
content      = group / garbage_seq
garbage_seq  = GB_OPEN garbage GB_END
garbage      = (garbage_char / escaped_char)*
garbage_char = !(ESCAPE / GB_END) ANY 
escaped_char = ESCAPE ANY

ESCAPE  = "!"
ANY     = ~"."
SEP     = ","
GP_OPEN = "{"
GP_END  = "}"
GB_OPEN = "<"
GB_END  = ">"
""")


def score(stream: str):
    tree = GRAM.parse(stream)

    def _score(node: Node, depth: int) -> int:
        next_depth = depth + 1 if node.expr_name == 'group' else depth
        self_score = depth if node.expr_name == 'group' else 0
        children_score = sum(_score(child, next_depth) for child in node)
        return self_score + children_score

    return _score(tree, 1)


def count_garbage(stream: str):
    tree = GRAM.parse(stream)

    def _count_garbage(node: Node) -> int:
        children_score = sum(_count_garbage(child) for child in node)
        self_score = 1 if node.expr_name == 'garbage_char' else 0
        return self_score + children_score

    return _count_garbage(tree)


def main(data: str):
    yield score(data)
    yield count_garbage(data)
