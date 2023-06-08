ULTIMATE=200000
WINNER=7000
BESTMOVE = 4000
THREAT2_NO_BACKUP = -15
THREAT2_1_BACKUP = -11
THREAT2_2_BACKUP = 7
THREAT1_NO_BACKUP = -1
THREAT1_1_BACKUP = 5
THREAT1_2_BACKUP = 15
SAFE_2_Backup=4
SAFE_1_Backup=2
SAFE_0_Backup=1
REINFORCMENTS = 9
UNDERTHREAT=-10
UNDERTHREAT_NOT_BACKED_UP = -500
REWARD_SAFE_POSITIONS=0

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
    if (ep.boardWhite & ep.ranks[0]).any():
        return ULTIMATE
    elif(ep.boardBlack & ep.ranks[7]).any():
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

    ev+=DD*THREAT2_2_BACKUP+DS*THREAT2_1_BACKUP+DZ*THREAT2_NO_BACKUP+SD*THREAT1_2_BACKUP+SS*THREAT1_1_BACKUP+SZ*THREAT1_NO_BACKUP+sD*SAFE_2_Backup+sS*SAFE_1_Backup+sZ*SAFE_0_Backup
    if Print:
        print("final score",end="=")
        print(ev)


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
        return -ULTIMATE
    if ep.turn:
        ep.boardWhite[frow*8+fcol]=0
        ep.boardWhite[row*8+col]=1
    else:
        ep.boardBlack[frow*8+fcol]=0
        ep.boardBlack[row*8+col]=1
    # 2 or 1 pawn behind current pawn
    reinforcments = ep.pawn_backed_up_by(row, col)
    val=0
    if ep.Safe_passage(row, col):
        val= WINNER if not ep.turn else WINNER
        # pawn is threatened
    elif ep.Pawn_is_under_threat(row, col):
        # move under threat not backed up
        if not reinforcments:
            val= UNDERTHREAT_NOT_BACKED_UP
        # move under threat but backed up
        else:
            val= reinforcments * REINFORCMENTS + UNDERTHREAT
    #pawn is not threatened , give bonus reward
    elif reinforcments:
        val= REWARD_SAFE_POSITIONS+reinforcments*REINFORCMENTS
    else:
        val= REWARD_SAFE_POSITIONS
    if ep.turn:
        ep.boardWhite[frow * 8 + fcol] = 1
        ep.boardWhite[row * 8 + col] = 0
    else:
        ep.boardBlack[frow * 8 + fcol] = 1
        ep.boardBlack[row * 8 + col] = 0

    return val



