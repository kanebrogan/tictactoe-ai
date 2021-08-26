#!/usr/bin/env python
# coding: utf-8

# In[17]:


import time

winningpositions = [[0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
                    [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
                    [0, 4, 8], [2, 4, 6]]  # diagonals


class Node:
    def __init__(self, xpos, opos, parent=None, children=[]):
        self.xpos = xpos
        self.opos = opos
        self.parent = parent
        self.children = list(children)
        self.mmv = None

    def addchild(self, newchild):
        self.children.append(newchild)

    def addparent(self, newparent):
        self.parent = newparent


class Player:
    def __init__(self, xo):
        self.xo = xo


class Agent(Player):
    def __init__(self, xo, depth=False):
        self.rootn = False  # root node for storing tree
        self.depth = depth
        self.xo = xo

    # override
    def makemove(self, boardstate, depth=-1):
        # calc tree on player's first turn
        re = Node([], [])
        # depth-limited search
        if depth > 0:
            self.rootn = self.gentreebydepth(boardstate, self.xo, depth)
            re = self.calcbestmove(self.rootn)
        # complete tree search
        else:
            if not self.rootn:
                # create entire game tree from agent's first turn
                self.rootn = self.gentree(boardstate, self.xo)
                re = self.calcbestmove(self.rootn)
            else:
                currnode = self.searchnextlvl(self.rootn, boardstate)
                re = self.calcbestmove(currnode)
        self.rootn = re
        return re

    def searchnextlvl(self, rootn, qry):
        res = False
        for ch in rootn.children:
            # print(qry.xpos,qry.opos," ?= ", ch.xpos,ch.opos)
            if qry.xpos == ch.xpos and qry.opos == ch.opos:
                res = ch
                break
        return res

    def calc_moves(self, node, turn):
        xpos = node.xpos
        opos = node.opos
        moveset = []
        if checkwin(opos) or checkwin(xpos):
            return
        availpos = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        for r in range(9):
            if r in xpos or r in opos:
                availpos.remove(r)
        if not availpos:
            return
        if turn == 'o':
            for a in availpos:
                tempset = []
                for i in opos:
                    tempset.append(i)
                tempset.append(a)
                moveset.append(tempset)
        elif turn == 'x':
            for a in availpos:
                tempset = []
                for i in xpos:
                    tempset.append(i)
                tempset.append(a)
                moveset.append(tempset)
        return moveset

    def calcbestmove(self, node):
        bestmove = node.children[0]
        if len(node.children) > 1:  # calcbestmove if more than 1 possible move
            remainc = node.children[1:]
            if self.xo == 'x':
                # check minimax value of children nodes to determine best move
                for c in remainc:
                    if c.mmv > bestmove.mmv:
                        bestmove = c
            elif self.xo == 'o':
                for c in node.children:
                    if c.mmv < bestmove.mmv:
                        bestmove = c
        return bestmove

    def calc_minimax(self, node):
        evalfunc = 0
        x1 = 0
        x2 = 0
        o1 = 0
        o2 = 0
        if checkwin(node.opos):
            evalfunc = -10
        elif checkwin(node.xpos):
            evalfunc = 10
        else:
            for wp in winningpositions:
                # print(wp)
                # checks if o occupies any moves in the winningposition
                if not any([o in node.opos for o in wp]):
                    xn = [x for x in wp if x in node.xpos]
                    if len(xn) == 1:
                        x1 += 1
                    elif len(xn) == 2:
                        x2 += 1
                # checks if x occupies any moves in the winningposition
                if not any([x in node.xpos for x in wp]):
                    on = [o for o in wp if o in node.opos]
                    if len(on) == 1:
                        o1 += 1
                    elif len(on) == 2:
                        o2 += 1
            evalfunc = 3*x2 + x1 - (3*o2 + o1)
        # print("Calculating Minimax for:")
        # printboard(node)
        # print("Result: ", evalfunc)
        return evalfunc

    def gentree(self, rootn, turnplayer):
        currnode = rootn
        # print('X:', currnode.xpos, ' O:', currnode.opos)
        childl = self.calc_moves(currnode, turnplayer)  # calculates children
        if childl:
            for m in childl:
                childnode = Node(currnode.xpos, currnode.opos, currnode)
                if turnplayer == 'x':
                    childnode.xpos = m
                if turnplayer == 'o':
                    childnode.opos = m
                currnode.addchild(childnode)
                # print("Added node for ", turnplayer, " -> X:", childnode.xpos,
                #     ' O:', childnode.opos, ' MMV:', childnode.mmv)
            # calc children for each child
            for chn in currnode.children:
                chn = self.gentree(chn, nextturn(turnplayer))
                # calc mmv of currnode using mmv of chn
                if turnplayer == 'x':
                    if currnode.mmv is None:
                        currnode.mmv = chn.mmv
                    elif currnode.mmv < chn.mmv:
                        currnode.mmv = chn.mmv
                if turnplayer == 'o':
                    if currnode.mmv is None:
                        currnode.mmv = chn.mmv
                    elif currnode.mmv > chn.mmv:
                        currnode.mmv = chn.mmv
                # print(currnode.mmv)

        # if leaf node calc minimax value
        else:
            currnode.mmv = self.calc_minimax(currnode)
            # print("Added mmv for leaf node: ", " -> X:", currnode.xpos,' O:',
            # currnode.opos, ' MMV:', currnode.mmv)
        return currnode

    def gentreebydepth(self, rootn, turnplayer, depth):
        currnode = rootn
        # print('X:', currnode.xpos, ' O:', currnode.opos)
        if depth > 0:
            childl = self.calc_moves(
                currnode, turnplayer)  # calculates children
            if childl:
                for m in childl:
                    childnode = Node(currnode.xpos, currnode.opos, currnode)
                    if turnplayer == 'x':
                        childnode.xpos = m
                    elif turnplayer == 'o':
                        childnode.opos = m
                    # TODO: alpha-beta pruning
                    currnode.addchild(childnode)
                    # print("Added node -> X:", currnode.xpos,
                    # ' O:', currnode.opos, ' MMV:', currnode.mmv)
                # calc next depth
                for chn in currnode.children:
                    chn = self.gentreebydepth(
                        chn, nextturn(turnplayer), depth-1)
                    # calc mmv of currnode using mmv of chn
                    if turnplayer == 'x':
                        if currnode.mmv is None:
                            currnode.mmv = chn.mmv
                        elif currnode.mmv < chn.mmv:
                            currnode.mmv = chn.mmv
                    elif turnplayer == 'o':
                        if currnode.mmv is None:
                            currnode.mmv = chn.mmv
                        elif currnode.mmv > chn.mmv:
                            currnode.mmv = chn.mmv
                    # print("Added MMV for node -> X:", currnode.xpos,
                    # ' O:', currnode.opos, ' MMV:', currnode.mmv)

            # if leaf node calc minimax value
            else:
                currnode.mmv = self.calc_minimax(currnode)
                # print("Added leaf node for ", turnplayer, " -> X:", currnode.xpos,
                #     ' O:', currnode.opos, ' MMV:', currnode.mmv)

        # when depth has reached 0 calc minimax value
        else:
            currnode.mmv = self.calc_minimax(currnode)
            # print("Added depth 0 node for ", turnplayer, " -> X:", currnode.xpos,
            #         ' O:', currnode.opos, ' MMV:', currnode.mmv)
        return currnode


def printboard(node, printpositions=False):
    b = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
    if printpositions:
        print('[0][1][2]')
        print('[3][4][5]')
        print('[6][7][8]')
        print("*****************")
    else:
        for o in node.opos:
            b[o] = 'o'
        for x in node.xpos:
            b[x] = 'x'
        print('[', b[0], ']', '[', b[1], ']', '[', b[2], ']')
        print('[', b[3], ']', '[', b[4], ']', '[', b[5], ']')
        print('[', b[6], ']', '[', b[7], ']', '[', b[8], ']')
        print("*****************")


def checkwin(playerpos):
    win = False
    for wp in winningpositions:
        if all(p in playerpos for p in wp):
            win = True
    return win


def nextturn(turnplayer):
    nextturn = None
    if turnplayer == 'o':
        nextturn = 'x'
    if turnplayer == 'x':
        nextturn = 'o'
    return nextturn


def playgame(playerx, playero):
    # new game state
    turnp = playerx
    gamestate = Node([], [])
    turn = 0
    winner = None
    print("*****Play Game*****")
    print("Position mapping:")
    printboard(gamestate, True)

    # turn loop
    while turn < 9:
        availpos = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        for r in range(9):
            if r in gamestate.xpos or r in gamestate.opos:
                availpos.remove(r)
        start = time.perf_counter()
        if isinstance(turnp, Agent):
            print(turnp.xo, "'s turn: ")
            print(turnp.xo, " is making it's move...")
            if turnp.xo == playerx.xo:
                if not turnp.depth:
                    gamestate = playerx.makemove(gamestate)
                elif turnp.depth:
                    gamestate = playerx.makemove(gamestate, turnp.depth)
                printboard(gamestate)
                if checkwin(gamestate.xpos):
                    winner = turnp
                    break
                finish = time.perf_counter()
                print(turnp.xo, f"'s turn took {finish - start:0.4f} seconds")
                turnp = playero  # swap turn
            elif turnp.xo == playero.xo:
                if not turnp.depth:
                    gamestate = playero.makemove(gamestate)
                elif turnp.depth:
                    gamestate = playero.makemove(gamestate, turnp.depth)
                print(turnp.xo, "'s turn: ")
                printboard(gamestate)
                if checkwin(gamestate.opos):
                    winner = turnp
                    break
                finish = time.perf_counter()
                print(turnp.xo, f"'s turn took {finish - start:0.4f} seconds")
                turnp = playerx
            turn += 1

        # human's turn
        else:
            if turnp.xo == playerx.xo:
                movemade = False
                while not movemade:
                    printboard(gamestate)
                    print(
                        "Make your turn by typing in the number of position and pressing Enter.")
                    print("Available positions: ", availpos)
                    move = input(">>> ")
                    move = int(move)
                    if move in availpos:
                        gamestate.xpos.append(move)
                        movemade = True
                    else:
                        print("Try again...")
                        printboard(gamestate, True)
                print(turnp.xo, "'s turn: ")
                printboard(gamestate)
                if checkwin(gamestate.xpos):
                    winner = turnp
                    break
                finish = time.perf_counter()
                print(turnp.xo, f"'s turn took {finish - start:0.4f} seconds")
                turnp = playero  # swap turn
            elif turnp.xo == playero.xo:
                movemade = False
                while not movemade:
                    printboard(gamestate)
                    print(
                        "Make your turn by typing in the number of position and pressing Enter.")
                    print("Available positions: ", availpos)
                    move = input(">>> ")
                    move = int(move)
                    if move in availpos:
                        gamestate.opos.append(move)
                        movemade = True
                    else:
                        print("Try again...")
                        printboard(gamestate, True)
                print(turnp.xo, "'s turn: ")
                printboard(gamestate)
                if checkwin(gamestate.opos):
                    winner = turnp
                    break
                finish = time.perf_counter()
                print(turnp.xo, f"'s turn took {finish - start:0.4f} seconds")
                turnp = playerx
            turn += 1

    if winner is None:
        print("Draw!")
    else:
        print(winner.xo, " wins!")


def newgame():
    playerx = Player('x')
    playero = Player('o')
    while True:
        print("*****Game Settings*****")
        print("Turn on Depth-Limited Search? type on/off and press Enter: ")
        dls = input()
        dls = dls.lower()
        depth = None
        if dls == "on":
            print("Type a number from 1-8 and press Enter to set depth: ")
            depth = input()
            while not depth.isnumeric:
                print("Please type a NUMBER from 1-8 and press Enter to set depth: ")
                depth = input()
            depth = int(depth)
            print("Do you wish to make the first move? type yes/no and press Enter: ")
            fm = input()
            fm = fm.lower()
            if fm == "yes":
                playero = Agent("o", depth)
                playgame(playerx, playero)
                break  # remove for game to reset after finish
            elif fm == "no":
                playerx = Agent("x", depth)
                playgame(playerx, playero)
                break  # remove for game to reset after finish
            else:
                ("Please try again...")
        elif dls == "off":
            print("Do you wish to make the first move? type yes/no and press Enter: ")
            fm = input()
            fm = fm.lower()
            if fm == "yes":
                playero = Agent("o")
                playgame(playerx, playero)
                break  # remove for game to reset after finish
            elif fm == "no":
                playerx = Agent("x")
                playgame(playerx, playero)
                break  # remove for game to reset after finish
        else:
            print("Please try again...")


# In[19]:


# test root nodes
# turn0 = Node([],[]) # add empty board as root node (used to calc entire game tree)
# turn1 = Node([4],[])
# turn2 = Node([4],[0])
# turn5 = Node([4,6],[0,2])

# start timer
# start = time.perf_counter()
# setup game
# bobai = Agent('x')
# steveai = Agent('o', 2)
# start game
# playgame(bobai, steveai)
# for i in range(9):
#    print('Minimax evalfunc: ', bobai.calc_minimax(Node([i],[]))) # test calc_minimax
# bobai.gentree(bobai.root, 'o')
# bobai.gentreebydepth(bobai.root, 'x', 2)
# finish = time.perf_counter()
# print(f"Finished game in {finish - start:0.4f} seconds")
# print(f"Total processing time : {finish - start:0.4f} seconds")
newgame()


# In[ ]:
