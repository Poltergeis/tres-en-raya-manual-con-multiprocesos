from Jugador import Jugador
from MyManager import MyManager
from Special import Special

myJugador = Jugador("O")
MyManager.register("get_jugador_o_reciever")
MyManager.register("get_end_game_sender")
MyManager.register("get_pos_reciever")
MyManager.register("get_ganador_sender")

manager = MyManager.create_default()
manager.connect()
turn_reciever = manager.get_jugador_o_reciever()
end_game_sender = manager.get_end_game_sender()
pos_reciever = manager.get_pos_reciever()
ganador_sender = manager.get_ganador_sender()
print("jugador O iniciado.")

try:
    while(True):
        turn = turn_reciever.recv()
        print("turno de jugador O")
        if turn == Special.GAME_OVER:
            break
        pos = pos_reciever.recv()
        myJugador.guardar_pos(pos)
        if myJugador.checar_victoria():
            end_game_sender.send("jugador_o")
            ganador_sender.send(myJugador)
            print("jugador O gana!!!")
            break
except KeyboardInterrupt:
    pass
finally:
    print("jugador O ha terminado su proceso.")