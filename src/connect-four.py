#
# Constants
#
MAXROWS = 6
MAXCOLS = 7
PLAYER1 = '\033[1;31;40mR\033[0;37;40m' # red on black
# PLAYER2 = '\033[1;32;40mG\033[0;37;40m' # green on black
PLAYER2 = '\033[1;34;40mB\033[0;37;40m' # blue on black

#
# FUNCTIONS
#

# Get-Functions
#
def get_player(i):
    """Returns the player for move i, either 'R' or 'G'.
    The character is colored with ANSI escape codes.

    i: int
    Returns: str
    """
    return PLAYER1 if i % 2 == 0 else PLAYER2

def get_col(s, i):
    """Returns the chosen column in move i from game sequence s.  The
    column index is zero-based.

    s: str
    i: int
    Returns: int
    """
    return int(s[i]) - 1

def get_row(s, i):
    """Returns resulting row in move i from game sequence s. The row
    index is zero-based.

    s: str
    i: int
    Returns: int
    """
    return s.count(s[i], 0, i)

def get_pos(s, i):
    """Returns tuple with position (as tuple of row and column) and
    player of move i from game sequence s.

    s: str
    i: int
    Returns: tuple of type ((int, int), str)
    """
    return ((get_row(s, i), get_col(s, i)), get_player(i))

def get_pos_list(s):
    """Return list with sequence of positions from game sequence s.

    s: str
    Returns: list of type ((int, int), str)

    TODO: Highly optimizable. Should be re-implemented using
    memofication and iteration.
    """
    return [get_pos(s, i) for i in range(len(s))]

def get_pos_dict(s):
    """Return dictionary with positions the players set by the game
    sequence s. Keys are positions as tuple of row and column, values
    are players.

    s: str
    Returns: dict with keys (int, int) and values str
    """
    d = dict()
    for p in get_pos_list(s):
        d[p[0]] = p[1]
    return d

def get_pos_grid(s):
    """Returns printable string representing the board as the grid
    after performing the game sequence s.

    s: str
    Returns: str
    """
    p = '' # the result string
    d = get_pos_dict(s)
    k = d.keys()
    for r in reversed(range(MAXROWS)):
        p += '|'
        for c in range(MAXCOLS):
            if (r, c) in k:
                p += " " + d[(r, c)] + " "
            else:
                p += '   '
        p += '|\n'
    b = '' # bottom line
    for i in range(MAXCOLS):
        b += '-' + str(i) + '-'
    return p + '+' + b + '+'

#
# Testing functions
#
def is_valid(s, i = None):
    """Returns True if s is a valid game sequences regarding number of
    columns and rows, i.e. the columns exist and are yet not filled.

    With optional parameter i check validity only for move i in game
    sequence s.

    s: str
    i: int
    Returns: Boolean

    """
    if len(s) == 0:
        return True
    elif i == None: # `reduce' operation
        res = True; j = 0
        while res and j < len(s):
            res = is_valid(s, j)
            j += 1
        return res
    else:
        return get_col(s, i) < MAXCOLS and get_row(s, i) < MAXROWS

