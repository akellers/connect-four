#
# Python implementation of the Connect Four-Game
#
# File: connect-four.py
# Date: 2023-03-05
#
# General idea: Connect Four can be understood as sequence of
# moves. These game sequence can be encoded as string where each
# character names the chosen columns (from 1 to 7).
#
# For implementation purposes this game sequence can be represented by
# a dictionary. Keys of the dictionary are the resulting position on
# the board (a grid with 6 rows and 7 columns). The values hold the
# respective player index (0 or 1).
#
# Note: The `encode' function relies on the fact that Python
# dictionaries preserve insertion (since version 3.7)
#

# CONSTANTS
MAXROWS = 6
MAXCOLS = 7
# ASCII encoded characters for the players
PLAYER1 = '\033[1;31;40mR\033[0;37;40m' # red on black
PLAYER2 = '\033[1;34;40mB\033[0;37;40m' # blue on black
PLAYERS = { 0 : PLAYER1, 1 : PLAYER2 }
# '\033[1;32;40mG\033[0;37;40m' # green on black
# '\033[1;33;40mG\033[0;37;40m' # yellow on black

# ENCODING/DECODING
def decode(s):
    """Return dict from game sequence s with postions (int, int) as key
    and player index (int). Decoding stops if resulting position is
    not valid, i.e. exceeds maximum number of rows or columns.

    s: str
    Returns: dict with key (int, int) and value int

    """
    dic = {} # resulting dict
    # local dict with free rows per columns (initially 0)
    row = { i : 0 for i in range(MAXCOLS) }
    if s == '':
        return dic
    else:
        for i in range(len(s)):
            # TODO: check character in '1' to '7'?
            c = int(s[i]) - 1 # column index zero based
            p = i % 2 # player index starting with 0
            r = row.get(c, -1) # free row in column c
            if 0 <= c < MAXCOLS and 0 <= r < MAXROWS:
                dic[(r, c)] = p # add pos and player into dict
                row[c] = r + 1 # increase row for column c
            else:
                print("Move %d '%s' in sequence '%s' leads to invalid position (%d, %d)!" % (i, s[i], s, r, c))
                return dic
    return dic

def encode(d):
    """Return string with game sequence from dictionary d.

    d: dict
    Returns: str
    """
    return ''.join([str(k[1]+1) for k in d.keys()])

# GET FUNCTIONS
# def get_player(s):

#     """Returns the player index for last move in game sequence s. Player
#     indices are zero based, starting with 0 for the first
#     move. Returns None if s is empty.

#     s: str
#     Returns: int

#     """
#     if s == '':
#         return None
#     else:
#         return (len(s) + 1) % 2

# def get_col(s):
#     """Returns the chosen column in last move in game sequence s. The
#     column index is zero-based.

#     s: str
#     Returns: int

#     """
#     if s == '':
#         return None
#     else:
#         return int(s[-1:]) - 1

# def get_row(s):
#     """Returns resulting row in move i from game sequence s. The row
#     index is zero-based.

#     s: str
#     Returns: int
#     """
#     if s == '':
#         return None
#     else:
#         l = len(s)
#         return s.count(s[l-1], 0, l-1)

# def get_pos(s):
#     """Returns tuple with position (as tuple of row and column) and
#     player of last move in game sequence s.

#     s: str
#     Returns: tuple of type ((int, int), int)
#     """
#     return ((get_row(s), get_col(s)), get_player(s))

# def get_pos_list(s):
#     """Return list with sequence of positions from game sequence s.

#     s: str
#     Returns: list of type ((int, int), str)
#     TODO: Obsolete with get_pos_dict
#     """
#     return [get_pos(s[0:i]) for i in range(1, len(s)+1)]

# def get_pos_dict(s):
#     """Return dictionary with positions the players set by the game
#     sequence s. Keys are positions as tuple of row and column, values
#     are player indices.

#     s: str
#     Returns: dict with keys (int, int) and values int
#     TODO: Obsolete with `decode`
#     """
#     dic = {}
#     row = { i : 0 for i in range(MAXCOLS) }
#     if s == '':
#         return dic
#     else:
#         for i in range(len(s)):
#             c = int(s[i]) - 1 # zero based
#             p = i % 2
#             r = row[c]
#             dic[(r, c)] = p
#             row[c] = r + 1
#     return dic
#     # return dict(get_pos_list(s))

def get_grid(s):
    """Returns printable string representing the board after game
    sequence s. Moves are colored using ASCII encoding.

    s: str
    Returns: str

    """
    p = '' # the result string
    d = decode(s)
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
# Test Functions
#
# def is_valid(s, rec = False):
#     """Returns True if last move in game sequences s is valid regarding
#     number of columns and rows, i.e. the column exist and are yet not
#     filled.

#     With optional boolean parameter check validity recursivly.
#     TODO: Obsolete. Validity is checked in `get_dict`

#     s: str
#     rec: Boolean (optional)
#     Returns: Boolean

#     """
#     if len(s) == 0:
#         return True
#     else:
#         b = get_col(s) < MAXCOLS and get_row(s) < MAXROWS
#         if rec == True:
#             return b and is_valid(s[:-1], rec)
#         else:
#             return b

def is_win(d):
    """Returns True if game dictionary d shows a win!

    d: dict
    Returns: Boolean
    """
    if len(d) < 7: return False # unsufficient number of moves

    # d = get_pos_dict(s)
    # row, column and player indices of last move
    ((r, c), x) = next(reversed(list(d.items())))

    # vertical
    if r >= 3:
        b1 = (r-1,c) in d and d[(r-1,c)] == x
        b2 = (r-2,c) in d and d[(r-2,c)] == x
        b3 = (r-3,c) in d and d[(r-3,c)] == x
        if b1 and b2 and b3:
            print("%s wins! Vertical at (%d, %d) [%s]." % (PLAYERS[x], r+1, c+1, encode(d)))
            return True
    # diagonal (upwards)
    b0 = (r+3,c+3) in d and d[(r+3,c+3)] == x
    b1 = (r+2,c+2) in d and d[(r+2,c+2)] == x
    b2 = (r+1,c+1) in d and d[(r+1,c+1)] == x
    b3 = (r-1,c-1) in d and d[(r-1,c-1)] == x
    b4 = (r-2,c-2) in d and d[(r-2,c-2)] == x
    b5 = (r-3,c-3) in d and d[(r-3,c-3)] == x
    if (b0 and b1 and b2) or (b1 and b2 and b3) or (b2 and b3 and b4) or (b3 and b4 and b5):
        print("%s wins! Diagonal at (%d, %d) [%s]." % (PLAYERS[x], r+1, c+1, encode(d)))
        return True

    # diagonal (downwards)
    b0 = (r+3,c-3) in d and d[(r+3,c-3)] == x
    b1 = (r+2,c-2) in d and d[(r+2,c-2)] == x
    b2 = (r+1,c-1) in d and d[(r+1,c-1)] == x
    b3 = (r-1,c+1) in d and d[(r-1,c+1)] == x
    b4 = (r-2,c+2) in d and d[(r-2,c+2)] == x
    b5 = (r-3,c+3) in d and d[(r-3,c+3)] == x
    if (b0 and b1 and b2) or (b1 and b2 and b3) or (b2 and b3 and b4) or (b3 and b4 and b5):
        print("%s wins! Diagonal at (%d, %d) [%s]." % (PLAYERS[x], r+1, c+1, encode(d)))
        return True

    # check horizontal (from left to right)
    b0 = (r,c-3) in d and d[(r,c-3)] == x
    b1 = (r,c-2) in d and d[(r,c-2)] == x
    b2 = (r,c-1) in d and d[(r,c-1)] == x
    b3 = (r,c+1) in d and d[(r,c+1)] == x
    b4 = (r,c+2) in d and d[(r,c+2)] == x
    b5 = (r,c+3) in d and d[(r,c+3)] == x
    if (b0 and b1 and b2) or (b1 and b2 and b3) or (b2 and b3 and b4) or (b3 and b4 and b5):
        print("%s wins! Horizontal at (%d, %d) [%s]." % (PLAYERS[x], r+1, c+1, encode(d)))
        return True

    return False

# def is_draw(d):
#     """Returns True if game dictionary d represents a draw.

#     s: dict
#     Returns: Boolean
#     """
#     return len(s) == MAXROWS * MAXCOLS and not is_win(s)

def is_final(d):
    """Returns True if game dictionary is a win or no further move is
    possible because the board is filled.

    s: dict
    Returns: Boolean

    """
    return is_win(d) or len(s) == MAXROWS * MAXCOLS

#
# Generator Functions
#
def gen_next(d):
    """Returns list with possible next tupels for game dictionary
    d. Tuples contain position and player. List may be empty if
    there is no next move.

    d: dict of type ((int, int), int)
    Returns: list of type ((int, int), int)

    """
    l = [] # result list
    p = len(d) % 2 # player for next move
    # iterate over columns
    k = d.keys()
    for c in range(MAXCOLS):
        r = 0 # initial row
        # positions in column c?
        ps = filter(lambda t: t[1] == c, d.keys())
        for t in ps:
            r = max(t[0]+1, r)
        if r < MAXROWS:
            l.append(((r, c), 1))
    return(l)


    """
    l = []
    for i in range(MAXCOLS):
        c = str(i+1)
        p = get_pos(s + c)
        if p[0][0] < MAXROWS: # column not yet filled!
            l.append(c)
    return l

def gen_next_seqs(s):
    """Returns list of next games sequences s by appending one move. The
    list may be emtpy if no next move available.

    s: str
    Returns: list

    """
    l = []
    for c in gen_next_cols(s):
        l.append(s + c)
    return l

def gen_game_seqs(s = '', lim = MAXROWS * MAXCOLS):
    """Returns list of all game sequences starting with s. Optional
    first argument allows setting of an initial game sequence. The
    number of generated moves can be limited by the named parameter.

    s: str (default is empty sequence '')
    lim: int (default is maximum number of moves)
    """
    xs = [s]
    ys = []
    ll = min(len(s) + lim, MAXROWS * MAXCOLS)
    while len(xs) > 0:
        x = xs[0]; xs = xs[1:]
        # sequence x final or limit reached?
        if is_final(x) or len(x) >= ll:
            ys.append(x)
        else:
            xs.extend(gen_next_seqs(x))
    return ys
