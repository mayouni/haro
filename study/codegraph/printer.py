"""printer.py -- a canonical printer for the Ring face: the text a graph says, with none of the author's layout.

The input is the recovered concrete tree of cst.py. The printer keeps every token and every comment and none of the
whitespace: tokens are separated by one space except where the grammar's own scanner reads a space as a different
token (a call's `(` and a subscript's `[` are glued to what they follow), brackets and commas and the member dot are
glued as every Ring text writes them, and each statement starts a line. It is the right inverse of the parser if and
only if printing a tree and parsing the result gives the tree back (round.py judges that).
"""
STATEMENT = {'expression_statement', 'return_statement', 'see_statement', 'give_statement', 'if_statement', 'for_statement',
             'while_statement', 'switch_statement', 'try_statement', 'do_again_statement', 'exit_statement', 'loop_statement',
             'bye_statement', 'load_statement', 'import_statement', 'function_definition', 'class_definition',
             'package_definition', 'else_clause', 'elseif_clause', 'catch_clause', 'finally_clause', 'case_clause',
             'other_clause', 'private_section', 'comment'}
NO_SPACE_BEFORE = {')', ']', ',', '.', '}'}
NO_SPACE_AFTER = {'(', '[', '.', '{'}


def tokens(root):
    """The tokens in source order: (text, kind, parent kind, hidden?)."""
    out = []
    for leaf in root.leaves():
        for h in leaf.hidden_before:
            out.append((h, 'hidden', leaf.parent.kind if leaf.parent else '', True))
        out.append((leaf.text, leaf.kind, leaf.parent.kind if leaf.parent else '', False))
    return out


def print_ring(root):
    """-> text. Walks the tree so that a statement node can start a line before its first token."""
    out, state = [], {'prev': None, 'line_start': True, 'in_string': 0}

    def put(text, kind, parent, hidden):
        prev = state['prev']
        glue = False
        if state['line_start']:
            glue = True                                    # first token of a line: nothing before it
        elif state['in_string']:
            glue = True                                    # inside a string literal: verbatim
        elif kind == 'hidden' and text in ('(', '['):
            glue = True                                    # a parameter list's `(` or a subscript's `[`
        elif kind in ('(', '[') and parent in ('call_expression', 'subscript_expression', 'new_with_parens'):
            glue = True
        elif text in NO_SPACE_BEFORE or (prev is not None and prev[0] in NO_SPACE_AFTER):
            glue = True
        if not glue:
            out.append(' ')
        out.append(text)
        state['prev'] = (text, kind)
        state['line_start'] = False
        if kind == 'comment':
            out.append('\n')
            state['line_start'] = True

    def walk(n):
        starts_line = n.kind in STATEMENT
        if starts_line and not state['line_start']:
            out.append('\n')
            state['line_start'] = True
        if not n.kids:
            for h in n.hidden_before:
                put(h, 'hidden', n.parent.kind if n.parent else '', True)
            put(n.text, n.kind, n.parent.kind if n.parent else '', False)
            return
        if n.kind == 'string':
            # the opening quote is a token like any other; what follows it, up to the closing quote, is verbatim
            walk(n.kids[0])
            state['in_string'] += 1
            for k in n.kids[1:]:
                walk(k)
            state['in_string'] -= 1
            return
        for k in n.kids:
            walk(k)

    walk(root)
    return ''.join(out).rstrip('\n') + '\n'
