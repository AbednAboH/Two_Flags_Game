import random
from bitarray import bitarray
import struct

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