# input + visuals  (front end)
# game_status is a class for the current board status
import heapq

from timer import Timer
from enpassant import transposition

from bitarray import bitarray
import evaluation


# local variables
BLACK = 1
WHITE = 2
EMPTY = 0


# k = int(self.boardWhite.to01(), 2)

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
        self.zobrist = transposition.zobrist()
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
                    if nextmoves[i]:moves_to_order.append((evaluation.evaluate(self,i + 8,row,col),self.code_a_move(i + 8, i)))
                    if twosteps[i]:moves_to_order.append((evaluation.evaluate(self,i + 16,row,col),self.code_a_move(i + 16, i)))
                    if enpassant_r[i]:moves_to_order.append((evaluation.evaluate(self,i + 7,row,col),self.code_a_move(i + 7, i)))
                    if enpassant_l[i]:moves_to_order.append((evaluation.evaluate(self,i + 9,row,col),self.code_a_move(i + 9, i)))
                    if self.white_attackright[i]:moves_to_order.append((evaluation.evaluate(self,i + 7,row,col),self.code_a_move(i + 7, i)))
                    if self.white_attackleft[i]:moves_to_order.append((evaluation.evaluate(self,i + 9,row,col),self.code_a_move(i + 9, i)))
                else:
                    if bnextmoves[i]:moves_to_order.append((evaluation.evaluate(self,i - 8, row , col),self.code_a_move(i - 8, i)))
                    if btwosteps[i]:moves_to_order.append((evaluation.evaluate(self,i - 16, row, col),self.code_a_move(i - 16, i)))
                    if benpassant_l[i]:moves_to_order.append((evaluation.evaluate(self,i - 7,row,col),self.code_a_move(i - 7, i)))
                    if benpassant_r[i]:moves_to_order.append((evaluation.evaluate(self,i - 9,row,col),self.code_a_move(i - 9, i)))
                    if self.black_attackleft[i]:moves_to_order.append((evaluation.evaluate(self,i - 7,row,col),self.code_a_move(i - 7, i)))
                    if self.black_attackright[i]:moves_to_order.append((evaluation.evaluate(self,i - 9,row,col),self.code_a_move(i - 9, i)))
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
        attack=self.boardWhite&self.attackMaskBlack if self.turn else self.boardBlack&self.attackMaskWhite
        return attack[row*8+col]
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
