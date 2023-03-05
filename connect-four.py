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

# PRINTABLE REPRESENTATION
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

# TESTING
def is_win(d):
    """Returns True if game dictionary d shows a win!

    d: dict
    Returns: Boolean
    """
    if len(d) < 7: return False # number of moves to low

    # row, column and player indices of last move
    ((r, c), x) = list(d.items())[-1]

    # vertical
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

def is_final(d):
    """Returns True if game dictionary is a win or no further move is
    possible because the board is filled.

    s: dict
    Returns: Boolean

    """
    return is_win(d) or len(d) == MAXROWS * MAXCOLS

# GENERATORS
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
            l.append(((r, c), p))
    return(l)

def gen_dict(d = {}, lim = 1):
    """Returns list of all possible game dictionaries starting with d. The
    maximum number of moves is limited by the optional parameter.

    d: dict of type ((int, int, int)
    Returns: list of dict with type ((int, int), int)

    """
    ds = [d] # start list
    rs = [] # result list
    ll = min(len(d) + lim, MAXROWS * MAXCOLS)
    while len(ds) > 0:
        x = ds.pop()
        # TODO: replace encode step here
        if len(x) >= ll or is_final(x):
            rs.append(x)
        else:
            for m in gen_next(x):
                l = list(x.items())
                l.append(m)
                ds.append(dict(l))
    return(rs)
