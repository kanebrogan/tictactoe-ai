#!/usr/bin/env python
# coding: utf-8

# In[1]:


# O goes first

# Does not include symmetry or invalid games (games where both O and X win).

# Since we are estimating total number of terminal states,
# the order in which moves are made is not important.
# E.g. [0,1,4] and [4,0,1] will not be counted twice in estimations
# because they are duplicate states, only [0,1,4] will be counted.

#   Position Mapping:
#   0 1 2
#   3 4 5
#   6 7 8

xplayer = []
oplayer = []

winningpositions = [[0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
                    [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
                    [0, 4, 8], [2, 4, 6]]  # diagonals


# Compares players current board stater to possible winning positions
def checkwin(player):
    win = False
    for p in winningpositions:
        if all(x in player for x in p):
            win = True
    return win


def generate_moves(n, winplayer):
    # This function generates the possible combinations of terminal states
    # for the losing player with a minimum of 2 moves generated for a 5-turn
    # games and a maximum of 5 moves generated to calculate draws.
    # opplayer should be a list containing the winning position as this
    # function is calculating the possile combinations of the player opposing
    # the winner. opplayer can be an empty list to calculate all possible
    # combinations on an empty board. This is used to calculate draws.

    validgames = 0
    invalidgames = 0
    currpos = []
    availpos = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    if winplayer:
        for p in winplayer:
            availpos.remove(p)
    print("Possible positions: ", availpos)
    # loop through all possible combinations of size n(no duplicates)
    for i in range(len(availpos)):
        for j in range(i+1, len(availpos)):
            if n > 2:
                for k in range(j+1, len(availpos)):
                    if n > 3:
                        for l in range(k+1, len(availpos)):

                            # calculate 5 moves (checks draw combinations)
                            if n > 4:
                                for m in range(l+1, len(availpos)):
                                    # store positions of both players to check_win to confirm a draw
                                    currpos = [availpos[cp]
                                               for cp in (i, j, k, l, m)]
                                    remainpos = list(availpos)
                                    for r in currpos:
                                        remainpos.remove(r)
                                    # check to confirm draw
                                    if not checkwin(currpos) and not checkwin(remainpos):
                                        print(currpos)
                                        validgames += 1
                                    # do not count as draw if either player wins
                                    else:
                                        print(currpos, " = INVALID STATE")
                                        invalidgames += 1

                            # calculate 4 moves
                            else:
                                currpos = [availpos[i] for i in (i, j, k, l)]
                                if not checkwin(currpos):
                                    print(currpos)
                                    validgames += 1
                                else:
                                    print(currpos, " = INVALID STATE")
                                    invalidgames += 1

                    # calculate 3 moves
                    else:
                        currpos = [availpos[i] for i in (i, j, k)]
                        if not checkwin(currpos):
                            print(currpos)
                            validgames += 1
                        else:
                            print(currpos, " = INVALID STATE")
                            invalidgames += 1

            # only two moves calculated, no need to check_win
            else:
                currpos = [availpos[i] for i in (i, j)]
                print(currpos)
                validgames += 1
    print("Number of valid states: ", validgames)
    print("Number of invalid states: ", invalidgames)
    return validgames


def calcterminalstates():  # Rewrite using more modular code e.g. -> calc_terminal_states(nmoves, winningplayer)
    tstates5 = 0
    tstates6 = 0
    tstates7 = 0
    tstates8 = 0
    tstates9 = 0

    # End in 5 turns (O wins)
    print("***Number of terminal states ending on the 5th move***")
    for p in winningpositions:
        oplayer = p
        print("Winning position for O: ", oplayer)
        tstates5 += generate_moves(2, oplayer)
    print("Total number of terminal states ending on the 5th move: ", tstates5)

    # End in 6 turns (X wins)
    print("***Number of terminal states ending on the 6th move***")
    for p in winningpositions:
        xplayer = p
        print("Winning position for X: ", xplayer)
        tstates6 += generate_moves(3, xplayer)
    print("Total number of terminal states ending on the 6th move: ", tstates6)

    # End in 7 turns (O wins)
    print("***Number of terminal states ending on the 7th move***")
    for p in winningpositions:
        addpos = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        # remove winning position
        for x in p:
            addpos.remove(x)
            # calculate remaining possible combinations
        for i in addpos:
            oplayer = p
            oplayer.append(i)
            print("Winning position for O: ", oplayer)
            tstates7 += generate_moves(3, oplayer)
            oplayer.remove(i)

    print("Total number of terminal states ending on the 7th move: ", tstates7)

    # End in 8 turns (X wins)
    print("***Number of terminal states ending on the 8th move***")
    for p in winningpositions:
        addpos = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        for x in p:
            addpos.remove(x)
        for i in addpos:
            xplayer = p
            xplayer.append(i)
            print("Winning position for X: ", xplayer)
            tstates8 += generate_moves(4, xplayer)
            xplayer.remove(i)
    print("Total number of terminal states ending on the 8th move: ", tstates8)

    # End in 9 turns (O wins + draws)
    print("***Number of terminal states ending on the 9th move***")
    # calculate wins by O
    for p in winningpositions:
        addpos = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        for x in p:
            addpos.remove(x)
        for i in range(len(addpos)):
            for j in range(i+1, len(addpos)):
                oplayer = p
                currpos = [addpos[i] for i in (i, j)]
                oplayer.extend(currpos)
                print("Winning position for O: ", oplayer)
                tstates9 += generate_moves(4, oplayer)
                for k in currpos:
                    oplayer.remove(k)
    print("Total number of terminal states winning on the 9th move: ", tstates9)
    # calculate draws ((all possible combinations of 5 moves) - (all winning combinations of 5 moves))
    oplayer = []
    print("Calculating draws...")
    draws = generate_moves(5, oplayer)

    print("***SUMMARY***")
    print("Total number of terminal states ending on the 5th move: ", tstates5)
    print("Total number of terminal states ending on the 6th move: ", tstates6)
    print("Total number of terminal states ending on the 7th move: ", tstates7)
    print("Total number of terminal states ending on the 8th move: ", tstates8)
    print("Total number of terminal states ending on the 9th move: ", tstates9+draws)
    print("Total number of terminal states: ", tstates5 +
          tstates6+tstates7+tstates8+tstates9+draws)
    print("Total wins by O: ", tstates5+tstates7+tstates9)
    print("Total wins by X: ", tstates6+tstates8)
    print("Total draws: ", draws)


# run calculation
calcterminalstates()
