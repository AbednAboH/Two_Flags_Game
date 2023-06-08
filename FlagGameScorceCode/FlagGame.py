import multiprocessing
import threading

b_height =512
b_width = 580
b_dimensions = 8
b_size = b_height//b_dimensions
FPS = 15
TILE_SIZE = 64
SCREEN_WIDTH = b_width
SCREEN_HEIGHT = b_height
BOARD_SIZE = b_size * 8
BOARD_X = (SCREEN_WIDTH-BOARD_SIZE)//2
BOARD_Y = int((SCREEN_HEIGHT / 2) - (BOARD_SIZE / 2))
IMG_SCALE = (b_size, b_size)

# Basic colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game colors
SMALL_TEXT_COLOR = (241, 250, 238)
LARGE_TEXT_COLOR = (230, 57, 70)
BG_COLOR = (29, 53, 87)
BG_COLOR_LIGHT = (70, 70, 70)
TILE_COLOR_LIGHT = (241, 250, 238)
TILE_COLOR_DARK = (69, 123, 157)
HIGHLIGHT_COLOR = (51, 153, 255)

# Create screen


# MinMax
DEPTH=9
THRESHHOLD=3

SCORE=800000
#eval
ULTIMATE=20000
WINNER=700
BESTMOVE = 400
THREAT2_NO_BACKUP = -15
THREAT2_1_BACKUP = -11
THREAT2_2_BACKUP = 7
THREAT1_NO_BACKUP = -1
THREAT1_1_BACKUP = 5
THREAT1_2_BACKUP = 15
SAFE_2_Backup=4
SAFE_1_Backup=2
SAFE_0_Backup=1
REINFORCMENTS = 7
UNDERTHREAT=-10
UNDERTHREAT_NOT_BACKED_UP = -500
REWARD_SAFE_POSITIONS=0

import pygame as p
from bitarray import bitarray
import tkinter as tk
import random
from multiprocessing import Queue,Process

class zobrist():
    def __init__(self):
        self.zobrist = [[random.randint(1, 2 ** 64 - 1) for i in range(3)] for j in range(64)]
        self.h = bitarray(64)
        self.h.setall(0)
        self.h = int(self.h.to01())

    def Hash(self, white, black):
        for i in range(64):
            if white[i] != 0:
                self.h = self.h ^ (self.zobrist[i][0])
            if black[i] != 0:
                self.h = self.h ^ (self.zobrist[i][1])
            else:
                self.h = self.h ^ (self.zobrist[i][2])
        return self.h

    def update_hash_value(self, old_new, white, black, black_or_white):
        old = int(old_new // 100)
        old = int(old // 10) * 8 + old % 8
        new = old_new % 100
        new = int(new // 10) * 8 + new % 8
        if (black_or_white):  # ie black's move
            if white[new] == 1:
                self.h = self.h ^ self.zobrist[new][0]  # xor out white pawn in new square
            else:
                self.h = self.h ^ self.zobrist[new][2]  # xor out empty in new square
            self.h = self.h ^ self.zobrist[new][1]  # xor in black pawn in new square
            self.h = self.h ^ self.zobrist[old][1]  # xor out black pawn from
            self.h = self.h ^ self.zobrist[old][2]  # xor in empty
        else:
            if black[new] == 1:
                self.h = self.h ^ self.zobrist[new][1]  # xor out black pawn
            else:
                self.h = self.h ^ self.zobrist[new][2]  # xor out empty
            self.h = self.h ^ self.zobrist[new][0]  # xor in white pawn
            self.h = self.h ^ self.zobrist[old][0]  # xor out white pawn
            self.h = self.h ^ self.zobrist[old][2]  # xor in empty

    def update_hash_value_for_undo(self, old_new, white, black, black_or_white):
        old = int(old_new // 100)
        old = int(old // 10) * 8 + old % 8
        new = old_new % 100
        new = int(new // 10) * 8 + new % 8
        if (black_or_white):  # ie black's move
            self.h = self.h ^ self.zobrist[old][2]  # xor in empty
            self.h = self.h ^ self.zobrist[old][1]  # xor out black pawn from
            self.h = self.h ^ self.zobrist[new][1]  # xor in black pawn in new square
            if white[new] == 1:
                self.h = self.h ^ self.zobrist[new][0]  # xor out white pawn in new square
            else:
                self.h = self.h ^ self.zobrist[new][2]  # xor out empty in new square
        else:
            self.h = self.h ^ self.zobrist[old][2]  # xor in empty
            self.h = self.h ^ self.zobrist[old][0]  # xor out white pawn
            self.h = self.h ^ self.zobrist[new][0]  # xor in white pawn
            if black[new] == 1:
                self.h = self.h ^ self.zobrist[new][1]  # xor out black pawn
            else:
                self.h = self.h ^ self.zobrist[new][2]  # xor out empty
""" timer class"""
class Timer():
    def __init__(self, time, pos):
        self.initial_time = time
        self.time = time
        self.pos = pos
        self.font = p.font.SysFont("Helvitca", 23, True, False)

    def tick(self, dt):
        self.time -= dt

    def reset(self):
        self.time = self.initial_time

    def draw(self,screen):
        mins, secs = divmod(self.time, 60)
        ms = divmod(self.time, 1000)[1]
        if self.time <= 10:
            s = f'{ms:.01f}'
        else:
            s = f'{int(mins):02}:{int(secs):02}'
        txt = self.font.render(s, True, SMALL_TEXT_COLOR)
        if self.pos == "top":
            p.draw.rect(screen, "black", p.Rect(8 * b_size, 1 * b_size,b_size-10, b_size-36))
            screen.blit(txt,  p.Rect(8 * b_size, 1 * b_size, b_size, b_size))
        elif self.pos=="bot":
            p.draw.rect(screen, "black", p.Rect(8 * b_size, 7 * b_size, b_size-10, b_size-36))
            screen.blit(txt, p.Rect(8 * b_size, 7 * b_size, b_size, b_size))
        else:
            p.draw.rect(screen, "black", p.Rect(8 * b_size, 4 * b_size, b_size - 10, b_size - 36))
            screen.blit(txt, p.Rect(8 * b_size, 4 * b_size, b_size, b_size))

def EvaluateBoard(ep):
    ev=0
    Print=False
    #black/white pieces under threat and by how much force
    LW_threat,RW_threat,LB_threat,RB_threat=ep.Pawns_under_threat()
    # not threatened are the not values of above numbers
    W_safe,B_safe=~LW_threat|~RW_threat,~LB_threat|~RB_threat
    #number of backup pieces
    LW_backup,RW_backup,LB_backup,RB_backup=ep.Pawns_backed_up_by()
    # not backed up  "not on above numbers"
    # white under threat and backed up
    """doubl threat"""
    W_double_threat=LW_threat & RW_threat
    B_double_threat=LB_threat & RB_threat

    """double the backup"""
    W_double_backup=LW_backup & LW_backup
    B_double_backup=LB_backup & LB_backup

    """ single threats"""
    W_single_threat=(LW_threat&~W_double_threat)|(RW_threat&~W_double_threat)
    B_single_threat=(LB_threat&~B_double_threat)|(RB_threat&~B_double_threat)

    """single backups """
    W_single_backup=LW_backup &~W_double_backup|RW_backup &~W_double_backup
    B_single_backup=LB_backup &~B_double_backup|RB_backup &~B_double_backup

    """no backup"""
    W_no_backup=ep.boardWhite & ~(LW_backup | RW_backup)
    B_no_backup=ep.boardBlack & ~(LB_backup | RB_backup)

    """value of number of double threats with double backup"""

    WDD=W_double_threat &W_double_backup
    BDD=B_double_threat &B_double_backup

    """double threat one backup"""

    WDS=W_double_threat&W_single_backup
    BDS=B_double_threat&B_single_backup

    """double threat no backup"""
    WDZ=W_double_threat&W_no_backup
    BDZ=B_double_threat&B_no_backup

    """one threat two backup"""
    WSD=W_single_threat&W_double_backup
    BSD=B_single_threat&B_double_backup

    """one threat one backup"""

    WSS=W_single_threat&W_single_backup
    BSS=B_single_threat&B_single_backup

    """one threat no backup"""

    WSZ=W_single_threat&W_no_backup
    BSZ=B_single_threat&B_no_backup

    """safe 2 backup"""

    WsD=W_safe & W_double_backup
    BsD=B_safe & B_double_backup
    """safe 1 backup"""

    WsS=W_safe & W_single_backup
    BsS=B_safe & B_single_backup

    """safe no backup"""

    WsZ=W_safe & W_no_backup
    BsZ=B_safe & B_no_backup

    # Winner=((ep.boardWhite&ep.rankup[1]).count(1)-(ep.boardBlack & ep.rankdown[6]).count(1))*WINNER
    # ev+=Winner
    """safe passage """
    """winner move """
    if (ep.boardWhite & ep.ranks[0])[0:8].any():
        return ULTIMATE
    elif(ep.boardBlack & ep.ranks[7])[55:64].any():
        return -ULTIMATE
    win=0
    DD=DS=DZ=SD=SS=SZ=sD=sS=sZ=0
    for i in range(64):
        if WDD[i]:DD+=1
        if BDD[i]:DD-=1
        if WDS[i]:DS+=1
        if BDS[i]:DS-=1
        if WDZ[i]:DZ+=1
        if BDZ[i]:DZ-=1
        if WSD[i]:SD+=1
        if BSD[i]:SD-=1
        if WSS[i]:SS+=1
        if BSS[i]:SS-=1
        if WSZ[i]:SZ+=1
        if BSZ[i]:SZ-=1
        if WsD[i]:sD-=1
        if BsD[i]:sD-=1
        if WsS[i]:sS+=1
        if BsS[i]:sS-=1
        if WsZ[i]:sZ+=1
        if BsZ[i]:sZ-=1
    # for row in range(8):
    #     for col in range(8):
    #         if ep.boardWhite[row*8+col]:
    #             blocked_road_up = ep.files_line_attack[col] & ep.rankup[row]
    #             blocked_road_up_byfriend = ep.files[col] & ep.rankup[row-1]
    #             blocked_road_up = (blocked_road_up & ep.attackMaskBlack) | (blocked_road_up & ep.boardBlack) | (blocked_road_up_byfriend & ep.boardWhite)
    #
    #             win+=BESTMOVE if not blocked_road_up.any() else 0
    #         if ep.boardBlack[row*8+col]:
    #             blocked_road_down_byfriend = ep.files[col] & ep.rankdown[row+1]
    #             blocked_road_down = ep.files_line_attack[col] & ep.rankdown[row]
    #             blocked_road_down = (blocked_road_down & ep.attackMaskWhite) | (blocked_road_down & ep.boardWhite)|(blocked_road_down_byfriend & ep.boardBlack)
    #
    #             win -=BESTMOVE if not blocked_road_down.any() else 0
    #ev+=DD+DS+DZ+SD+SS+SZ+sD+sS+sZ
    # print (WsZ,BsZ)
    ev+=DD*THREAT2_2_BACKUP+DS*THREAT2_1_BACKUP+DZ*THREAT2_NO_BACKUP+SD*THREAT1_2_BACKUP+SS*THREAT1_1_BACKUP+SZ*THREAT1_NO_BACKUP+sD*SAFE_2_Backup+sS*SAFE_1_Backup+sZ*SAFE_0_Backup







    # for i in range(64):
        # row=i//8
        # col=i-row*8
        # ev+=evaluate(ep,row,col) if ep.boardWhite[i] else 0
        # ev-=evaluate(ep,row,col) if ep.boardBlack[i] else 0

    return ev

def evaluate(ep,fro, row, col):
    frow=fro//8
    fcol=fro%8
    if (ep.boardWhite & ep.ranks[0]).any():
        return ULTIMATE
    elif (ep.boardBlack & ep.ranks[7]).any():
        return ULTIMATE
    if ep.turn:
        ep.boardWhite[frow*8+fcol]=0
        ep.boardWhite[row*8+col]=1
    else:
        ep.boardBlack[frow*8+fcol]=0
        ep.boardBlack[row*8+col]=1
    # 2 or 1 pawn behind current pawn
    reinforcments = ep.pawn_backed_up_by(row, col)
    val=0
    double_threat = False
    threat=ep.Pawn_is_under_threat(row, col)
    onethreat=nothreat=False
    """estimate the value """
    if threat==2:
        double_threat=True
    elif threat==1 :
        onethreat=True
    else:
        nothreat=True
    if ep.Safe_passage(row, col):
        val= WINNER
        # pawn is threatened
    elif double_threat:
        # move under threat not backed up
        if not reinforcments:
            val= THREAT2_NO_BACKUP
        # move under threat but backed upP
        elif reinforcments==1:
            val= THREAT2_1_BACKUP
        else:
            val= THREAT2_2_BACKUP
    elif onethreat:
        if not reinforcments:
            val = THREAT1_NO_BACKUP
            # move under threat but backed upP
        elif reinforcments == 1:
            val = THREAT1_1_BACKUP
        else:
            val = THREAT1_2_BACKUP
    elif nothreat:
        if not reinforcments:
            val = SAFE_0_Backup
            # move under threat but backed upP
        elif reinforcments == 1:
            val = SAFE_1_Backup
        else:
            val = SAFE_2_Backup
    if ep.turn:
        ep.boardWhite[frow * 8 + fcol] = 1
        ep.boardWhite[row * 8 + col] = 0
    else:
        ep.boardBlack[frow * 8 + fcol] = 1
        ep.boardBlack[row * 8 + col] = 0

    return val

class App:
    # 'what' and 'why' should probably be fetched in a different way, suitable to the app
    def __init__(self, root):
        self.parent = root
        self.parent.title("Flags Game")
        self.ip_address=""
        self.port_number=""
        self.Timer=""
        self.agentLabel2=tk.Label(root, text=" agent vs agent:").grid(row=1)
        self.agentLabel=tk.Label(root, text="agent: ").grid(row=2)
        self.humanLabel=tk.Label(root, text="human:").grid(row=3)
        self.serverLabel=tk.Label(root, text="server vs agent:").grid(row=4)
        self.agent1 = tk.IntVar()
        self.agent2 = tk.IntVar()
        self.human1 = tk.IntVar()
        self.server = tk.IntVar()
        tk.Checkbutton(root, text="agent vs agent", variable=self.agent1).grid(row=1, column=1, sticky=tk.W)
        self.agent = tk.Scale(root, from_=True, to=False, orient="horizontal",variable=self.agent2).grid(row=2,column=1)
        self.human= tk.Scale(root, from_=True, to=False, orient="horizontal",variable=self.human1).grid(row=3,column=1)
        tk.Checkbutton(root, text="put server ip and socket number", variable=self.server).grid(row=6, column=1, sticky=tk.W)
        tk.Label(root, text="Add Time ").grid(row=7)
        tk.Label(root, text="Setup").grid(row=8)
        tk.Label(root, text="Server Address(ip)").grid(row=9)
        tk.Label(root, text="port number").grid(row=10)
        self.ip = tk.Entry(self.parent)
        self.port = tk.Entry(self.parent)
        self.time = tk.Entry(self.parent)
        self.setup = tk.Entry(self.parent)
        self.ip.grid(row=9, column=1)
        self.port.grid(row=10, column=1)
        self.time.grid(row=7, column=1)
        self.setup.grid(row=8, column=1)
        tk.Button(root, text='apply', command=self.use_entry).grid(row=11, column=1, sticky=tk.W, pady=4)
    def use_entry(self):
        self.ip_address = self.ip.get()
        self.port_number = self.port.get()
        self.Timer=self.time.get()
        self.Setup=self.setup.get()
        self.parent.destroy() # if you must

global HashTable

HashTableforPlayer1 = {}
HashTableforPlayer2 = {}
Pawns = {}


# ai that calls to nega max
def aiT(ep, valid, move_vals, depth, Qeue):
    global nextMove, nothashed, counter, hashed, HashTable, TempHash,NumberofValidMoves
    TempHash = {}
    nextMove = None
    hashed = nothashed = counter =NumberofValidMoves= 0
    HashTable = HashTableforPlayer1 if ep.turn else HashTableforPlayer2
    print(len(HashTable))

    nega_max_alpha_beta(ep, valid, move_vals, depth, 1 if ep.turn else -1, -900000, 900000,0)

    print("Moves /all recursian iterations:")
    if counter>0:
        print(NumberofValidMoves/counter)
    print("Moves / recursian iterations:")
    if nothashed>0:
        print(NumberofValidMoves/nothashed)
    print("nodes cut by Transposition Table")
    print(hashed)
    if Qeue is None:
        return nextMove
    else:
        Qeue.put(nextMove)

# alpha beta pruning
def nega_max_alpha_beta(ep, ValidMoves, move_vals, depth, turnMultiplier, alpha, beta,boardval):
    global nextMove, nothashed, counter, hashed, HashTable, TempHash,NumberofValidMoves
    if depth == 0:
        return turnMultiplier*boardval
    maxScore = -SCORE
    NumberofValidMoves+=len(ValidMoves)
    for i in range(len(ValidMoves)):
        counter += 1
        move = ValidMoves[i]
        nboardval=move_vals[i] if ep.turn else -move_vals[i]
        ep.move_for_alpha_beta(move)
        if ep.zobrist.h in HashTable.keys():
            score = HashTable[ep.zobrist.h]
            hashed+=1
        # if the gamestate was calculated then check it's depth
        else:
            nextMoves, Vals = ep.possible_moves()
            score = -nega_max_alpha_beta(ep, nextMoves, Vals, depth - 1, -turnMultiplier, -beta, -alpha,nboardval+boardval)
            # score+=nboardval
            if depth <= THRESHHOLD:
                HashTable[ep.zobrist.h] = score
            nothashed += 1
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
                print(boardval)
        ep.undo_for_alpha_beta()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore
# k = int(self.boardWhite.to01(), 2)
import socket

class Client():

    def __init__(self,server):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clock = 30
        self.Setup = ""
        self.start = False
        self.white_is_ai = False
        self.quit = False
        self.setup = False
        self.move=None
        self.end = False
        self.server_address=server
    def get_server_address(self):
        pass

    def Connect(self):
        print('connecting to %s port %s' % self.server_address)
        try:
            self.sock.connect(self.server_address)
        except:
            print("connection failed ,please check server address")

    def send(self, message):
        try:
            # Send data
            message = bytes(message,"utf-8")
            print('"%s"' % message.decode("utf-8"))
            self.sock.send(message)
        finally:
            pass

    def recieve(self):
        while True:

            try:
                data = self.sock.recv(4000)
                data = data.decode("utf-8")
                print(data)
                if (data[:5]=="Setup"):
                    self.Setup=data[6:]
                    self.send(b"OK")
                if (data[:4] == "Time"):
                    self.clock = int(data[4:]) * 60
                    self.send(b"OK")
                elif (data=="Begin"):
                    self.start=True
                    self.white_is_ai=True
                    self.send(b"OK")
                elif data=="exit":
                    self.end=True
                elif (len(data)==4):
                    self.start=True
                    self.move=data
            except:
               pass
    def startprocess(self):
        self.Connect()
        self.recieve()





# variables in game status :

# board : our chess board where 1 is black 2 is white 0 is empty
# history : records our history so that we can undo last move or just to display the moves to the user
# move_white : a flag that points to who's turn it is
# black_count,white_count : counts the number of pawns for each respectively so that we can check later if one of them has non without going through the whole board

# functions :

# move: given a move in a form of type tuple ,applies the move on the board and updates the history using a function

# undo: undo the last move registered in the history stack and removes from history using a function

# update history : add's the move given to it to the history

# code_a_move : creates a tupple (fromx,fromy,tox,toy) so that we can distinguish between the moves

# possible moves : iterates on the board and find's every possible move for every pawn on the chess board

# piece moves : given a place on the board(empty or full) (i,j) appends every move that can happen to a stack

# winner : check who is the winner based on 3 states h1 has a piece ,h8 has a piece ,0 pawns for one of the contenders ,no possible move !

# translate moves from / to the server : will be able to convert from one format (of the moves) to our format of the moves or vise versa

class game_status():
    # numbering of the tiles " here we will be mapping h1,...,h8 to our own coardinates , and do the same for a1 to a8

    # for upcomming ai vs user and maybe visual effects too

    actual_to_row = {"8": 0, "7": 1, "6": 2, "5": 3, "4": 4, "3": 5, "2": 6, "1": 7}

    a_to_col = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    row_to_actual = {v: k for k, v in actual_to_row.items()}
    col_to_a = {v: k for k, v in a_to_col.items()}

    def __init__(self):

        self.boardvalue = 0
        # bitboards
        self.boardWhite = bitarray(64)
        self.boardBlack = bitarray(64)
        self.rank8 = bitarray(64)
        self.rank0 = bitarray(64)
        # to correct the shift
        self.file9 = bitarray(64)
        self.file7 = bitarray(64)
        # two steps
        self.white_two_steps = bitarray(64)
        self.black_two_steps = bitarray(64)
        # enpassant moves
        self.enpassant_black = bitarray(64)
        self.enpassant_white = bitarray(64)
        # set them to zeroes
        self.rank0.setall(False)
        self.rank8.setall(False)
        self.boardWhite.setall(False)
        self.boardBlack.setall(False)
        self.enpassant_black.setall(False)
        self.enpassant_white.setall(False)
        # attack mask for evaluation
        self.attackMaskBlack = bitarray(64)
        self.attackMaskWhite = bitarray(64)
        self.black_attackright= bitarray(64)
        self.black_attackleft= bitarray(64)
        self.white_attackright= bitarray(64)
        self.white_attackleft= bitarray(64)
        # give the bitboards correct starting values
        self.boardBlack[1 * 8:1 * 8 + 8] = 1
        self.boardWhite[6 * 8:6 * 8 + 8] = 1
        # update board value
        self.boardvalue=0
        self.boardvalue_history={}
        # rank 8 and 0 bitboards
        self.rank0[0:8] = True
        self.rank8[56:64] = True
        self.ranks = {}
        # for evaluation purpuses to find safe passage
        self.rankup = {}
        self.rankdown = {}
        self.set_ranks_up()
        self.set_ranks_down()
        self.setranks()
        # initiate files
        self.file9.setall(1)
        self.file7.setall(1)
        self.files = {}
        self.files_line_attack = {}
        self.file9[7:64:8] = False
        self.file7[0:64:8] = False
        self.creat_files()
        self.creat_files_attack_mask()

        # for the initial two steps
        self.white_two_steps.setall(0)
        self.white_two_steps[4 * 8:4 * 8 + 8] = 1
        self.black_two_steps.setall(0)
        self.black_two_steps[3 * 8:3 * 8 + 8] = 1

        # board to display initial values // will be removed    self.history = []
        self.bitboard_history = []
        # to switch between players
        self.turn = True
        # number of pawns
        self.counter_enp_black = 0
        self.counter_enp_white = 0

        # turn timers and game timer
        self.time_p1 = Timer(3000, "bot")
        self.time_p2 = Timer(3000, "top")
        self.gametime = Timer(1800, "game")
        self.zobrist = zobrist()
        self.zobrist.Hash(self.boardWhite, self.boardBlack)
        self.a_move_was_mad = False


# this function creates files so that we can find specific moves meaning file a to h
    def creat_files(self):

        for file in range(0, 8):
            data = bitarray(64)
            data.setall(0)
            data[file:64:8] = True
            self.files[file] = data
# this function creates files for attaks meaning
###########
#0 0 0 1 0 1
#0 0 0 1 0 1
#0 0 0 1 0 1
############
    def creat_files_attack_mask(self):
        for file in range(0, 8):
            if file == 0:
                data = self.files[file + 1]|self.files[file]
            elif file == 7:
                data = self.files[file - 1]|self.files[file]
            else:
                data = self.files[file - 1] | self.files[file]|self.files[file + 1]
            self.files_line_attack[file] = data

# creates all ranks from rank 1 to rank 8
    def setranks(self):

        for file in range(0, 8):
            data = bitarray(64)
            data.setall(0)
            data[8 * file:8 * file + 8] = True
            self.ranks[file] = data

# creates masks for us to look on all above ranks
    def set_ranks_up(self):
        for file in range(0, 8):
            data = bitarray(64)
            data.setall(0)
            if file > 0 and file < 8:
                data[0:8 * file + 8] = True
            else:
                data[8 * file:8 * file + 8] = True
            self.rankup[file] = data

# creates masks for us to look on all the ranks below current rank
    def set_ranks_down(self):
        for file in range(0, 8):
            data = bitarray(64)
            data.setall(0)
            data[8 * file:64] = True
            self.rankdown[file] = data
# creates a mask that check if the pawns rood to victory is empty and that he can march forward with confidance
    def getpassagemask(self, row, col, up_down):
        # passage to top board
        if up_down:
            pass
# after a change in the representaion of the board i used this function to make a move that calles to the function below it
    def move_for_alpha_beta(self, number):
        to_move = number // 100
        to_be_moved_to = number % 100
        to_move = ((to_move // 10), to_move % 10)
        to_be_moved_to = ((to_be_moved_to) // 10, to_be_moved_to % 10)

        self.zobrist.update_hash_value(number, self.boardWhite, self.boardBlack, self.turn)

        self.update_history_bitboard(self.boardBlack, self.boardWhite, self.enpassant_black, self.enpassant_white,number,self.boardvalue)
        self.move(to_move, to_be_moved_to)
# makes a move on the board
    def move(self, to_move, to_be_moved_to):

        place = to_be_moved_to[0] * 8 + to_be_moved_to[1]
        fplace = to_move[0] * 8 + to_move[1]
        is_enpassant = abs(to_be_moved_to[0] - to_move[0])
        # print(self.allmoves)
        if self.turn == True:
            self.boardBlack[place] = False
            self.boardWhite[place] = True
            self.boardWhite[fplace] = False
            # check if the move makes white open to be attacked by enpassant move
            if (is_enpassant == 2):
                self.enpassant_white[place] = True
            # if enpassant capture done then update relevant fields
            if (self.enpassant_black[place + 8]):
                self.boardBlack[place + 8] = self.enpassant_black[place + 8] = False
        # symmetric to the above but for black pawns
        else:
            self.boardBlack[place] = True
            self.boardBlack[fplace] = False
            self.boardWhite[place] = False
            if (is_enpassant == 2):
                self.enpassant_black[place] = True
            if (self.enpassant_white[place - 8]):
                self.boardWhite[place - 8] = self.enpassant_white[place - 8] = False
        self.turn = not self.turn
# undo the last move
    def undo_for_alpha_beta(self):
        #retreav all previos data
        (self.boardBlack, self.boardWhite, self.enpassant_black, self.enpassant_white,move,self.boardvalue) = self.bitboard_history.pop()
        #undo changes to zobrist keys
        self.zobrist.update_hash_value_for_undo(move, self.boardWhite, self.boardBlack, not self.turn)
        # undo turn
        self.turn = not self.turn
# update history array
    def update_history_bitboard(self, blackboard, whiteboard, w, v, move,boardEval):
        self.bitboard_history.append((blackboard.copy(), whiteboard.copy(), w.copy(), v.copy(), move,boardEval))

    # creates signiture for the move from:row,col , to: row,col meaning  from 2,4 to 3,4 becomes 2434

    def code_a_move(self, to_move, to_be_moved_to):
        col_to_move = to_move % 8
        row_to_move = (to_move - col_to_move) / 8
        col_to_be_moved_to = to_be_moved_to % 8
        row_to_be_moved_to = (to_be_moved_to - col_to_be_moved_to) / 8
        return int(row_to_move * 1000 + col_to_move * 100 + row_to_be_moved_to * 10 + col_to_be_moved_to)

# create all possible moves and rate them
    def possible_moves(self):
        valid_moves = []
        queue=[]

        # self.boardvalue=EvaluateBoard(self)
        if (self.turn):
            self.enpassant_white.setall(0)
        else:
            self.enpassant_black.setall(0)
        # first try , assuming whites turn
        # two moves for first play by the pawns
        # white is on the LSB "<<" ,Black MSB ">>"
        """move by one square"""
        nextmoves = (self.boardWhite << 8 ^ (self.boardBlack & self.boardWhite << 8))&(self.boardWhite << 8 ^ (self.boardWhite & self.boardWhite << 8))


        twosteps = self.white_two_steps & (nextmoves << 8 ^ (self.boardBlack & nextmoves << 8))&(nextmoves << 8 ^ (self.boardWhite & nextmoves << 8))
        """attack masks for white"""
        self.white_attackright = self.boardBlack & self.boardWhite << 7 & self.file7
        self.white_attackleft = self.boardBlack & self.boardWhite << 9 & self.file9
        """enpassant capture's"""
        enpassant_r = self.enpassant_black << 8 & self.boardWhite << 7
        enpassant_l = self.enpassant_black << 8 & self.boardWhite << 9

        """black moves"""
        """symmetric to ubove"""
        bnextmoves = (self.boardBlack >> 8 ^ (self.boardWhite & self.boardBlack >> 8))&(self.boardBlack >> 8 ^ (self.boardBlack & self.boardBlack >> 8))
        btwosteps = self.black_two_steps & (bnextmoves >> 8 ^ (self.boardWhite & bnextmoves >> 8))&(bnextmoves >> 8 ^ (self.boardBlack & bnextmoves >> 8))
        self.black_attackleft = self.boardWhite & self.boardBlack >> 7 & self.file9
        self.black_attackright = self.boardBlack >> 9 & self.boardWhite & self.file7
        benpassant_l = self.enpassant_white >> 8 & self.boardBlack >> 7
        benpassant_r = self.enpassant_white >> 8 & self.boardBlack >> 9

        """get full attack mask to be used for sorting the moves"""
        self.attackMaskWhite = self.white_attackright | self.white_attackleft
        self.attackMaskBlack = self.black_attackright | self.black_attackleft
        moves_to_order=[]
        move=0
        # register said moves
        # for i in range(64):
        #     if self.turn:
        #         if nextmoves[i]:
        #             move=self.code_a_move(i + 8, i)
        #             valid_moves.append(move)
        #             moves_to_order.append(evaluation.evaluate(self,i+8,8))
        #         if twosteps[i]:valid_moves.append(self.code_a_move(i + 16, i))
        #         if enpassant_l[i]:valid_moves.append(self.code_a_move(i + 7, i))
        #         if enpassant_r[i]:valid_moves.append(self.code_a_move(i + 9, i))
        #         if self.white_attackleft[i]:valid_moves.append(self.code_a_move(i + 7, i))
        #         if self.white_attackright[i]:valid_moves.append(self.code_a_move(i + 9, i))
        #     else:
        #         if bnextmoves[i]:valid_moves.append(self.code_a_move(i - 8, i))
        #         if btwosteps[i]:valid_moves.append(self.code_a_move(i - 16, i))
        #         if benpassant_l[i]:valid_moves.append(self.code_a_move(i - 7, i))
        #         if benpassant_r[i]:valid_moves.append(self.code_a_move(i - 9, i))
        #         if self.black_attackleft[i]:valid_moves.append(self.code_a_move(i - 7, i))
        #         if self.black_attackright[i]:valid_moves.append(self.code_a_move(i - 9, i))

        #get move values to sort them
        # for i in range(len(valid_moves)):
        #     d=valid_moves[i]%100
        #     row=d//10
        #     col=d%10
        #     queue.append((evaluation.evaluate(self,row,col),valid_moves[i]))
        """evaluate and sort the moves"""
        for row in range(8):
            for col in range(8):
                i = row * 8 + col
                if self.turn:
                    if nextmoves[i]:moves_to_order.append((evaluate(self,i + 8,row,col),self.code_a_move(i + 8, i)))
                    if twosteps[i]:moves_to_order.append((evaluate(self,i + 16,row,col),self.code_a_move(i + 16, i)))
                    if enpassant_r[i]:moves_to_order.append((evaluate(self,i + 7,row,col),self.code_a_move(i + 7, i)))
                    if enpassant_l[i]:moves_to_order.append((evaluate(self,i + 9,row,col),self.code_a_move(i + 9, i)))
                    if self.white_attackright[i]:moves_to_order.append((evaluate(self,i + 7,row,col),self.code_a_move(i + 7, i)))
                    if self.white_attackleft[i]:moves_to_order.append((evaluate(self,i + 9,row,col),self.code_a_move(i + 9, i)))
                else:
                    if bnextmoves[i]:moves_to_order.append((evaluate(self,i - 8, row , col),self.code_a_move(i - 8, i)))
                    if btwosteps[i]:moves_to_order.append((evaluate(self,i - 16, row, col),self.code_a_move(i - 16, i)))
                    if benpassant_l[i]:moves_to_order.append((evaluate(self,i - 7,row,col),self.code_a_move(i - 7, i)))
                    if benpassant_r[i]:moves_to_order.append((evaluate(self,i - 9,row,col),self.code_a_move(i - 9, i)))
                    if self.black_attackleft[i]:moves_to_order.append((evaluate(self,i - 7,row,col),self.code_a_move(i - 7, i)))
                    if self.black_attackright[i]:moves_to_order.append((evaluate(self,i - 9,row,col),self.code_a_move(i - 9, i)))
        valid_moves = sorted(moves_to_order, key=lambda x: x[0], reverse=True)
        queue=[]
        moveValue=[]
        for i in range(len(valid_moves)):
            queue.append(valid_moves[i][1])
            moveValue.append(valid_moves[i][0])
        return queue,moveValue

    # check who is the winner
    # options : 1. no possible moves 2.no pawns left 3. on of the pawns is on the oppponent's first row

    def winner(self, possible_moves,AIsearching):
        if not AIsearching and (self.boardWhite & self.ranks[0]).any() or self.time_p2.time <= 0:
            return 'winner is white'
        elif not AIsearching and (self.boardBlack & self.ranks[7]).any() or self.time_p1.time <= 0:
            return 'winner is black'
        elif not possible_moves and not AIsearching:
            if self.turn:
                return 'winner is black no possible moves'
            else:
                return 'winner is white no possible moves'

        else:return '1'

    # on the assumption that it's a string
    def translate_moves_from_server(self, moves):
        # using h_to_row ,a_to_col
        # h1h2
        from_=self.actual_to_row[moves[1]]*8+self.a_to_col[moves[0]]
        to_=self.actual_to_row[moves[3]]*8+self.a_to_col[moves[0]]
        return self.code_a_move(from_,to_)

    def translate_moves_to_server(self, number):
        #row,col,newrow,newcol like "4546"
        to_move = number // 100
        to_be_moved_to = number % 100
        row,col = (to_move // 10), to_move % 10
        row_to,col_to = ((to_be_moved_to) // 10, to_be_moved_to % 10)
        return self.col_to_a[col]+self.row_to_actual[row]+self.col_to_a[col_to]+self.row_to_actual[row_to]

    def setboard(self,board):
        self.boardBlack.setall(0)
        self.boardWhite.setall(0)
        Words=board.split()
        for Char in Words:
            col = self.a_to_col[Char[1]]
            row = self.actual_to_row[Char[2]]
            if (Char[0]=="W"):
                self.boardWhite[row*8+col]=True
            else:
                self.boardBlack[row*8+col]=True
        self.zobrist.Hash(self.boardWhite, self.boardBlack)




    # evaluations
    def Pawn_here(self, row, col):
        return self.boardWhite[row * 8 + col] if self.turn else self.boardBlack[row * 8 + col]

    # check if pawn is under threat
    def Pawn_is_under_threat(self, row,col):
        if self.turn:
            attack=(self.boardWhite&self.black_attackleft)[row*8+col]+(self.boardWhite&self.black_attackright)[row*8+col]
        else:
            attack=(self.boardBlack&self.white_attackright)[row*8+col]+(self.boardBlack&self.white_attackleft)[row*8+col]
        return attack
    def Pawns_under_threat(self):
        return self.boardWhite&self.black_attackleft,self.boardWhite&self.black_attackright ,self.boardBlack&self.white_attackleft,self.boardBlack&self.white_attackright
    # check by how many pieces the pawn is backed up by
    def pawn_backed_up_by(self, row, col):
        row = row + 1 if self.turn else row - 1
        if row >0 and row <8:
            return self.Pawn_here(row, col - 1) if col-1<8 else 0 + self.Pawn_here(row, col + 1) if col+1>0 else 0
    def Pawns_backed_up_by(self):
        wl=wr=bl=br=bitarray(64)
        wl.setall(0)
        wr.setall(0)
        bl.setall(0)
        br.setall(0)
        for i in range(8):
            wl=wl | (self.ranks[i] & self.boardWhite) & (self.boardWhite << 7 & self.file7)
            wr=wr | (self.ranks[i] & self.boardWhite) & (self.boardWhite << 9 & self.file9)
            bl=bl | (self.ranks[i] & self.boardBlack) &(self.boardBlack >> 7 & self.file9)
            br=br|(self.ranks[i] & self.boardBlack) &(self.boardBlack >> 9 & self.file7)

        return wl,wr,bl,br
    # def oponent_backedup(self,row,col):
    #     row = row + 1 if not self.turn else row - 1
    #     return self.Pawn_here(row, col - 1) + self.Pawn_here(row, col + 1)
    #
    def Safe_passage(self, row, col):
        #################################################
        # self.files[col] & self.rankup[row]
        # 0 1 0 0 0 0..
        # 0 1 0 0 0 0..
        # 0 1 0 0 0 0..
        # 0 0 0 0 0 0..
        # 0 0 0 0 0 0..
        ##################################################
        blocked_road_up = self.files_line_attack[col] & self.rankup[row]
        blocked_road_down = self.files_line_attack[col] & self.rankdown[row]
        blocked_road_up = (blocked_road_up & self.attackMaskBlack) | (blocked_road_up & self.boardBlack)
        blocked_road_down = (blocked_road_down & self.attackMaskWhite) | (blocked_road_down & self.boardWhite)
        if row>0:
            blocked_road_up_byfriend = self.files[col] & self.rankup[row - 1]
            blocked_road_up = blocked_road_up | (blocked_road_up_byfriend & self.boardWhite)
        if row<7:
            blocked_road_down_byfriend = self.files[col] & self.rankdown[row + 1]
            blocked_road_down=blocked_road_down|(blocked_road_down_byfriend & self.boardBlack)
        return not blocked_road_up.any() if self.turn else not blocked_road_down.any()

def drawText(screen, text):
    font = p.font.SysFont("Helvitca", 32, True, False)
    textObject = font.render(text, 0, p.Color('Gray'))
    textLocation = p.Rect(0, 0, b_width, b_height).move(b_width / 2 - textObject.get_width() / 2,
                                                        b_height / 2 - textObject.get_height() / 2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color('Black'))
    screen.blit(textObject, textLocation.move(2, 2))


def load_pawns():
    Pawns[1] = p.transform.scale(p.image.load("images/bp.png"), (b_size, b_size))
    Pawns[2] = p.transform.scale(p.image.load("images/wp.png"), (b_size, b_size))


# draw clocks
def draw_clock(enp_state,start_count, dt, AISearching, ai_ID, ai, ServerOn, player1, player2, turn, screan):
    enp_state.time_p1.draw(screan)
    enp_state.time_p2.draw(screan)
    enp_state.gametime.draw(screan)
    enp_state.gametime.tick(dt)
    if ServerOn :
        # ai white
        if ai_ID:
            if AISearching:
                enp_state.time_p2.tick(dt)
            elif not AISearching:
                enp_state.time_p1.tick(dt)
        else:
            if AISearching:
                enp_state.time_p1.tick(dt)
            elif  not AISearching:
                enp_state.time_p2.tick(dt)
    else:
        # both are ai
        if player1 and player2:
            # white
            if  turn:
                enp_state.time_p1.tick(dt)
            elif  not turn:
                enp_state.time_p2.tick(dt)
        # player1 is ai and white
        elif player1 and not player2:
            if  AISearching:
                enp_state.time_p1.tick(dt)
            elif not AISearching :
                enp_state.time_p2.tick(dt)
        # player 2 is ai and black
        elif player2 and not player1:
            if AISearching:
                enp_state.time_p2.tick(dt)
            elif not AISearching :
                enp_state.time_p1.tick(dt)
        else:
            if enp_state.turn:
                enp_state.time_p1.tick(dt)
            else:
                enp_state.time_p2.tick(dt)


# draw pawn and squares

def draw_state(screen, enp_state):
    draw_squares(screen)
    draw_pawns(screen, enp_state)
    enp_state.a_move_was_mad = False


# draw the squares on the board by using mode 2 on the sum of the raws and columes


def draw_squares(screen):
    c = [p.Color("white"), p.Color("brown")]
    for i in range(b_dimensions):
        for j in range(b_dimensions):
            color = c[(i + j) % 2]
            p.draw.rect(screen, color, p.Rect(j * b_size, i * b_size, b_size, b_size))


# draw pawns


def draw_pawns(screen, enp_state):
    for i in range(b_dimensions):
        for j in range(b_dimensions):
            black = enp_state.boardBlack[i * 8 + j]
            white = enp_state.boardWhite[i * 8 + j]
            if (black == 1):
                screen.blit(Pawns[1], p.Rect(j * b_size, i * b_size, b_size, b_size))
            if (white == 1):
                screen.blit(Pawns[2], p.Rect(j * b_size, i * b_size, b_size, b_size))


def connect(cl):
    cl = Client.Client()


def humanvhuman(human):
    human = not True


def main(whiteplayer, blackplayer, ServerPlayer,server,setup,time):
    client = Client(server)
    if ServerPlayer:

        cl = threading.Thread(target=client.startprocess, args=())
        cl.start()
    p.init()
    SCREEN = p.display.set_mode((b_width, b_height))
    clock = p.time.Clock()
    SCREEN.fill(p.Color("white"))
    enp_state = game_status()
    if(len(setup)):
        enp_state.setboard(setup)
    if(len(time)):
        enp_state.time_p1.time=int(time)*60
        enp_state.time_p2.time=int(time)*60
    load_pawns()
    AISearching = False
    pawn_clicked_location = ()  # which pawn was clicked on
    second_click = []  # where to place the pawn
    game = True
    # AiProcess=None
    AiQ = None
    draw_state(SCREEN, enp_state)


    turn = False
    GameOver = False

    if ServerPlayer:
        while (not client.start):
            game = False
    game = True
    start_count = False
    if (client.start):
        if client.setup:
            enp_state.setboard(client.Setup)
        enp_state.time_p1 = Timer(client.clock, "top")
        enp_state.time_p2 = Timer(client.clock, "bot")
    ai_ID = client.white_is_ai if ServerPlayer else False
    while game:
        if not ServerPlayer:
            ai = (blackplayer and not enp_state.turn) or (whiteplayer and enp_state.turn)
        else:
            ai = client.white_is_ai and enp_state.turn or not (client.white_is_ai or enp_state.turn)
        # get all possible moves on the board / this operation in my opinion is heavy (not the fastest might update it in the future !)
        possible_moves, eval = enp_state.possible_moves()
        if (ai and possible_moves and not GameOver):
            if not AISearching:
                AISearching = True
                turn = bool(enp_state.turn)

                possible_moves, vals = enp_state.possible_moves()
                AiQ = Queue()
                AiProcess = threading.Thread(target=aiT, args=(enp_state, possible_moves, vals, DEPTH, AiQ))

                AiProcess.start()
            if not AiProcess.is_alive():
                nextMove = AiQ.get()
                # print(nextMove)
                if nextMove != None:
                    enp_state.move_for_alpha_beta(nextMove)
                else:
                    if len(possible_moves) != 0:
                        nextMove = possible_moves[random.randint(0, len(possible_moves) - 1)]
                        enp_state.move_for_alpha_beta(nextMove)
                print("---------------")
                print("move is:")
                print(enp_state.translate_moves_to_server(nextMove))
                print("---------------")
                if ServerPlayer:
                    client.send(enp_state.translate_moves_to_server(nextMove))
                if enp_state.winner(possible_moves, False) != '1':
                    GameOver = True
                enp_state.a_move_was_mad = True
                AISearching = False
        dt = clock.tick(FPS) / 1000
        if (ServerPlayer and not AISearching):
            move = None
            if client.move is not None:
                move = enp_state.translate_moves_from_server(client.move)
            if move in possible_moves:
                enp_state.move_for_alpha_beta(move)
                print("---------------")
                print("move made by server:")
                print(move)
                print("---------------")

        for event in p.event.get():

            # closing event (X)
            if event.type == p.QUIT:
                game = False
            elif event.type == p.MOUSEBUTTONDOWN and not ServerPlayer:
                # which piece we clicked
                coordinates = p.mouse.get_pos()
                horizontal = coordinates[1] // b_size
                vertical = coordinates[0] // b_size
                if pawn_clicked_location == (horizontal, vertical):  # double clicked !
                    pawn_clicked_location = ()  # clear
                    second_click = []

                else:  # might be valid !
                    pawn_clicked_location = ((horizontal, vertical))
                    second_click.append(pawn_clicked_location)
                    if len(second_click) == 2:
                        # if we had two clicks then we have all the parameteres that we need
                        move = enp_state.code_a_move(second_click[0][0] * 8 + second_click[0][1],
                                                     second_click[1][0] * 8 + second_click[1][1])
                        if move in possible_moves:
                            # ev = evaluation.evaluate(enp_state, second_click[1][0], second_click[1][1])
                            # enp_state.boardvalue += ev if enp_state else -ev
                            enp_state.move_for_alpha_beta(move)
                            print("---------------")
                            print("move made :")
                            print(enp_state.translate_moves_to_server(move))
                            print("---------------")
                            enp_state.a_move_was_mad = True
                            pawn_clicked_location = ()  # clear
                            second_click = []  # clear clicks

                        else:
                            second_click = [pawn_clicked_location]  # if we changed our mind and clicked another piece

            elif event.type == p.KEYDOWN:
                if event.key == p.K_u:
                    enp_state.undo_for_alpha_beta()

        # if not AISearching:
        win_status = enp_state.winner(possible_moves, AISearching)
        if win_status != '1' or GameOver:
            drawText(SCREEN, win_status)
        if enp_state.a_move_was_mad and not AISearching:
            draw_state(SCREEN, enp_state)
        draw_clock(enp_state,start_count, dt, AISearching, ai_ID, ai, ServerPlayer, whiteplayer, blackplayer, turn, SCREEN)
        p.event.pump()
        p.display.flip()

        # check who is the winner


if __name__ == "__main__":

    root = tk.Tk()
    app=App(root)
    root.mainloop()
    # print(app.port_number,app.ip_address,app.agent1.get(),app.agent2.get(),app.server.get())

    if (len(app.port_number)):
        server=(app.ip_address,int(app.port_number))
    else:
        server=("127.0.0.1",75220)

    agent=app.agent2.get()
    human=app.human1.get()
    agent_vs_agent=app.agent1.get()
    server_flag=app.server.get()
    whiteplayer = False
    blackplayer = False
    ServerPlayer = server_flag
    setup=app.Setup
    time=app.Timer
    if agent_vs_agent:
        whiteplayer = True
        blackplayer = True
    elif agent and not human:
        whiteplayer = True
        blackplayer = False
    elif not agent and human:
        whiteplayer = False
        blackplayer = True


    main(whiteplayer,blackplayer,ServerPlayer,server,setup,time)
