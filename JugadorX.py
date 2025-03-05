from Jugador import Jugador
from MyManager import MyManager
from Special import Special

myJugador = Jugador("X")
MyManager.register("get_jugador_x_reciever")
MyManager.register("get_end_game_event")
MyManager.register("get_pos_reciever")
MyManager.register("get_ganador_sender")

manager = MyManager.create_default()
manager.connect()
turn_reciever = manager.get_jugador_x_reciever()
end_game_event = manager.get_end_game_event()
pos_reciever = manager.get_pos_reciever()
ganador_sender = manager.get_ganador_sender()
print("jugador X iniciado.")

try:
    while(True):
        turn = turn_reciever.recv()
        print("turno de jugador X")
        if turn == Special.GAME_OVER:
            break
        pos = pos_reciever.recv()
        myJugador.guardar_pos(pos)
        if myJugador.checar_victoria():
            end_game_event.set()
            ganador_sender.send(myJugador)
            print("jugador X gana!!!")
            break
except KeyboardInterrupt:
    pass
finally:
    print("jugador X ha terminado su proceso.")