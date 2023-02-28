#
# Constants
#
MAXROWS = 6
MAXCOLS = 7
PLAYER1 = '\033[1;31;40mR\033[0;37;40m' # red on black
# PLAYER2 = '\033[1;32;40mG\033[0;37;40m' # green on black
PLAYER2 = '\033[1;34;40mB\033[0;37;40m' # blue on black
PLAYERS = { 1 : PLAYER1, 2 : PLAYER2 }

#
# FUNCTIONS
#

# Get Functions
#
def get_player(s):
    """Returns the player number for last move in game sequence s. Returns
    None if s is empty.

    s: str
    Returns: int

    """
    if s == '':
        return None
    else:
        return 1 + len(s) % 2

def get_col(s):
    """Returns the chosen column in last move in game sequence s. The
    column index is zero-based.

    s: str
    Returns: int

    """
    if s == '':
        return None
    else:
        return int(s[-1:]) - 1

def get_row(s):
    """Returns resulting row in move i from game sequence s. The row
    index is zero-based.

    s: str
    Returns: int
    """
    if s == '':
        return None
    else:
        l = len(s)
        return s.count(s[l-1], 0, l-1)

def get_pos(s):
    """Returns tuple with position (as tuple of row and column) and
    player of last move in game sequence s.

    s: str
    Returns: tuple of type ((int, int), str)
    """
    return ((get_row(s), get_col(s)), get_player(s))

def get_pos_list(s):
    """Return list with sequence of positions from game sequence s.

    s: str
    Returns: list of type ((int, int), str)

    TODO: Highly optimizable. Should be re-implemented using
    memofication and iteration.
    """
    return [get_pos(s[0:i]) for i in range(1, len(s)+1)]

def get_pos_dict(s):
    """Return dictionary with positions the players set by the game
    sequence s. Keys are positions as tuple of row and column, values
    are players.

    s: str
    Returns: dict with keys (int, int) and values str
    """
    return dict(get_pos_list(s))

def get_grid(s):
    """Returns printable string representing the board as grid after game
    sequence s. Moves are colored using ASCII encoding.

    s: str
    Returns: str

    """
    p = '' # the result string
    d = get_pos_dict(s)
    for r in reversed(range(MAXROWS)):
        p += ' |'
        for c in range(MAXCOLS):
            if (r, c) in d:
                p += " " + PLAYERS[d[(r, c)]] + " "
            else:
                p += '   '
        p += '| ' + str(r+1) + '\n'
    b = '' # bottom line
    for i in range(MAXCOLS):
        b += '-' + str(i+1) + '-'
    return p + ' +' + b + '+'

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

def is_final(s, i = None):
    """Returns True if move i in game sequence s leads to a win,
    i.e. to four connected positions for one player.

    If parameter i is missing use last move of game sequence instead.

    s: str
    i: int
    Returns: Boolean

    """
    if len(s) < 7: # insufficent numer of moves
        return False
    if i == None:
        n = len(s)-1
    else:
        n = i
    d = get_pos_dict(s[:n+1])
    p = get_pos(s, n)
    r = p[0][0] # row
    c = p[0][1] # col
    x = p[1] # player
    # check vertical
    if r >= 3:
        b1 = (r-1,c) in d and d[(r-1,c)] == x
        b2 = (r-2,c) in d and d[(r-2,c)] == x
        b3 = (r-3,c) in d and d[(r-3,c)] == x
        if b1 and b2 and b3:
            print("%s has won! Vertical in column %d." % (x, c+1))
            return True
        # check diagonal (left)
        b1 = (r-1,c-1) in d and d[(r-1,c-1)] == x
        b2 = (r-2,c-2) in d and d[(r-2,c-2)] == x
        b3 = (r-3,c-3) in d and d[(r-3,c-3)] == x
        if b1 and b2 and b3:
            print("%s has won! Left diagonal from row %d and column %d." % (x, r+1, c+1))
            return True
        # check diagonal (right)
        b1 = (r-1,c+1) in d and d[(r-1,c+1)] == x
        b2 = (r-2,c+2) in d and d[(r-2,c+2)] == x
        b3 = (r-3,c+3) in d and d[(r-3,c+3)] == x
        if b1 and b2 and b3:
            print("%s has won! Right diagonal from row %d and %d." % (x, r+1, c+1))
            return True
    # check horizontal (from left to right)
    b1 = (r,c-3) in d and d[(r,c-3)] == x
    b2 = (r,c-2) in d and d[(r,c-2)] == x
    b3 = (r,c-1) in d and d[(r,c-1)] == x
    if b1 and b2 and b3:
        print("%s has won! In row %d from column %d to %d." % (x, r+1, c-2, c+1))
        return True
    # check horizontal (from left to right)
    b1 = (r,c-2) in d and d[(r,c-2)] == x
    b2 = (r,c-1) in d and d[(r,c-1)] == x
    b3 = (r,c+1) in d and d[(r,c+1)] == x
    if b1 and b2 and b3:
        print("%s has won! In row %d from column %d to %d." % (x, r+1, c-1, c+2))
        return True
    # check horizontal (from left to right)
    b1 = (r,c-1) in d and d[(r,c-1)] == x
    b2 = (r,c+1) in d and d[(r,c+1)] == x
    b3 = (r,c+2) in d and d[(r,c+2)] == x
    if b1 and b2 and b3:
        print("%s has won! In row %d from column %d to %d." % (x, r+1, c, c+3))
        return True
    # check horizontal (from left to right)
    b1 = (r,c+1) in d and d[(r,c+1)] == x
    b2 = (r,c+2) in d and d[(r,c+2)] == x
    b3 = (r,c+3) in d and d[(r,c+3)] == x
    if b1 and b2 and b3:
        print("%s has won! In row %d from column %d to %d." % (x, r+1, c+1, c+4))
        return True

    return False
#
# Generating functions
#
def gen_next_cols(s):
    """Returns list of column indices for the next move after game sequence
    s. The list may be emtpy if no next move available.

    s: str
    Returns: list

    TODO: Implement filtering on win here or elsewhere?
    """
    l = []
    for c in range(MAXCOLS):
        p = get_pos(s + str(c + 1), len(s))
        if p[0][0] < MAXROWS: # column not yet filled!
            l.append(c)
    return l

def gen_next_seqs(s):
    """Returns list of next games sequences by appending one move to
    s. The list may be emtpy if no next move available.

    s: str
    Returns: list
    """
    l = []
    for c in gen_next_cols(s):
        l.append(s + str(c + 1))
    return l

def gen_full_seqs(s = '', lim = MAXROWS * MAXCOLS):
    """Returns list of all game sequences starting with s. Optional
    first argument allows setting of an initial game sequence. The
    number of generated moves can be limited by the named parameter.

    s: str (default is empty sequence '')
    lim: int (default is maximum number of moves)
    """
    xs = [s]
    ys = []
    ll = len(s) + lim
    while len(xs) > 0:
        x = xs[0]; xs = xs[1:]
        n = gen_next_seqs(x)
        if len(n) == 0:
            ys.append(x)
        elif len(n[0]) < ll:
            xs.extend(n)
        else:
            ys.extend(n)
    return ys
