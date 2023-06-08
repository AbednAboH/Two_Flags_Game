# back end
import threading
from app import App
from settings import *
from enpassant import Client
import pygame as p
import random
import tkinter as tk
from enpassant import enpassant_engine
from enpassant import AI

from multiprocessing import Queue, Process
import evaluation
from timer import Timer

# cl = Client.Client()
cl = 0
# dictionary of 2 pawns
Pawns = {}
# ai

human = False


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
                enp_state.time_p1.tick(dt)
            elif not enp_state.turn and not AISearching:
                enp_state.time_p2.tick(dt)
        else:
            if AISearching:
                enp_state.time_p2.tick(dt)
            elif enp_state.turn and not AISearching:
                enp_state.time_p1.tick(dt)
    else:
        # both are ai
        if player1 and player2:
            # white
            if ai and turn:
                enp_state.time_p1.tick(dt)
            elif ai and not turn:
                enp_state.time_p2.tick(dt)
        # player1 is ai and white
        elif player1 and not player2:
            if enp_state.turn and AISearching:
                enp_state.time_p1.tick(dt)
            elif not AISearching and enp_state.turn:
                enp_state.time_p2.tick(dt)
        # player 2 is ai and black
        elif player2 and not player1:
            if not enp_state.turn:
                enp_state.time_p2.tick(dt)
            elif not AISearching and enp_state.turn:
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
    p.init()
    SCREEN = p.display.set_mode((b_width, b_height))
    clock = p.time.Clock()
    SCREEN.fill(p.Color("white"))
    enp_state = enpassant_engine.game_status()
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
    client = Client.Client(server)

    turn = False
    GameOver = False
    cl = threading.Thread(target=client.startprocess, args=())
    if ServerPlayer:
        cl.start()
        while (not client.start):
            game = False
    game = True
    start_count = False
    if (client.start):
        if client.setup:
            enp_state.setboard(client.Setup)
        enp_state.time_p1 = Timer(client.clock, "top")
        enp_state.time_p2 = Timer(client.clock, "bot")
    ai_ID = client.white_is_ai and enp_state.turn if ServerPlayer else whiteplayer and enp_state.turn
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
                AiProcess = threading.Thread(target=AI.ai, args=(enp_state, possible_moves, vals, DEPTH, AiQ))
                # AiProcess = Process(target=AI.ai,args=(enp_state, possible_moves, DEPTH, AiQ))
                # NegaMin(enp_state,possible_moves,DEPTH,-1)
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
    print(app.port_number,app.ip_address,app.agent1.get(),app.agent2.get(),app.server.get())

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
