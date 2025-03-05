from MyManager import MyManager
from multiprocessing import Pipe

jugador_X_reciever, jugador_X_sender = Pipe(duplex=False)
jugador_O_reciever, jugador_O_sender = Pipe(duplex=False)
end_game_reciever, end_game_sender = Pipe(duplex=False)
pos_reciever, pos_sender = Pipe(duplex=False)
ganador_reciever, ganador_sender = Pipe(duplex=False)
MyManager.register("get_mensaje", lambda: "hola desde main.py.")
MyManager.register("get_jugador_x_reciever", lambda: jugador_X_reciever)
MyManager.register("get_jugador_x_sender", lambda: jugador_X_sender)
MyManager.register("get_jugador_o_reciever", lambda: jugador_O_reciever)
MyManager.register("get_jugador_o_sender", lambda: jugador_O_sender)
MyManager.register("get_end_game_reciever", lambda: end_game_reciever)
MyManager.register("get_end_game_sender", lambda: end_game_sender)
MyManager.register("get_pos_reciever", lambda: pos_reciever)
MyManager.register("get_pos_sender", lambda: pos_sender)
MyManager.register("get_ganador_reciever", lambda: ganador_reciever)
MyManager.register("get_ganador_sender", lambda: ganador_sender)

if __name__ == "__main__":
    try:
        manager = MyManager.create_default()
        server = manager.get_server()
        print("servidor encendido.")
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        print("servidor cerrado.")