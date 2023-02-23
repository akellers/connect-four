def get_player(i):
    """Returns the player for move i, either 'R' or 'G'.

    i: int
    Returns: str
    """
    return 'G' if i % 2 == 1 else 'R'

def get_col(s, i):
    """Returns chosen column in move i from game sequence s. 
    The column index is zero-based.

    s: str
    i: int
    """
    return int(s[i]) - 1

def get_row(s, i):
    """Returns resulting row in move i from game sequence s.
    The row index is zero-based.

    s: str
    i: int
    """
    return s.count(s[i], 0, i)

def get_pos(s, i):
    return ((get_row(s, i), get_col(s, i)), get_player(i))

def get_pos_list(s):
    return [get_pos(s, i) for i in range(len(s))]

def get_pos_dict(s):
    d = dict()
    for p in get_pos_list(s):
        d[p[0]] = p[1]
    return d

def get_pos_grid(s):
    d = get_pos_dict(s)
    p = ''
    k = d.keys()
    for r in reversed(range(6)):
        p += '|'
        for c in range(7):
            if (r, c) in k:
                p += " " + d[(r, c)] + " "
            else:
                p += '   '
        p += '|\n'
    return p + '+---------------------+'

