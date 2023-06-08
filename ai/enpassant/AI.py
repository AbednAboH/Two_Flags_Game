from settings import *
from evaluation import *

global HashTable

HashTableforPlayer1 = {}
HashTableforPlayer2 = {}


# this document includes
def ai(ep, valid, move_vals, depth, Qeue):
    global nextMove, nothashed, counter, hashed, HashTable, TempHash
    TempHash = {}
    nextMove = None
    hashed = nothashed = counter = 0
    HashTable = HashTableforPlayer1 if ep.turn else HashTableforPlayer2
    print(HashTable.__sizeof__())
    nega_max_alpha_beta(ep, valid, move_vals, depth, 1 if ep.turn else -1, -5000, 5000)
    print("hashed ")
    print(hashed)
    print("nothashed")
    print(nothashed)
    print("all")
    print(counter)
    if Qeue is None:
        return nextMove
    else:
        Qeue.put(nextMove)


def nega_max_alpha_beta(ep, ValidMoves, move_vals, depth, turnMultiplier, alpha, beta):
    global nextMove, nothashed, counter, hashed, HashTable, TempHash
    if depth == 0:
        # if ep.zobrist.h not in HashTable.keys():
        #     HashTable[ep.zobrist.h]=turnMultiplier*ep.boardvalue
        return turnMultiplier * EvaluateBoard(ep)
    maxScore = -SCORE
    for i in range(len(ValidMoves)):
        counter += 1
        move = ValidMoves[i]
        ep.move_for_alpha_beta(move)
        # check if the gamstate was calculated before
        # if it wasn't then calculate it
        if ep.zobrist.h in HashTable.keys():
            hashed += 1
            score = HashTable[ep.zobrist.h]
        # if the gamestate was calculated then check it's depth
        else:
            nextMoves, Vals = ep.possible_moves()
            score = -nega_max_alpha_beta(ep, nextMoves, Vals, depth - 1, -turnMultiplier, -beta, -alpha)
            if depth <= THRESHHOLD:
                HashTable[ep.zobrist.h] = score
            nothashed += 1
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        ep.undo_for_alpha_beta()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore

# add to alpha beta

# int Quiesce( int alpha, int beta ) {
#     int stand_pat = Evaluate();
#     if( stand_pat >= beta )
#         return beta;
#     if( alpha < stand_pat )
#         alpha = stand_pat;
#
#     until( every_capture_has_been_examined )  {
#         MakeCapture();
#         score = -Quiesce( -beta, -alpha );
#         TakeBackMove();
#
#         if( score >= beta )
#             return beta;
#         if( score > alpha )
#            alpha = score;
#     }
#     return alpha;
# }
