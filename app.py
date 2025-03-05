import customtkinter
import threading
from MyManager import MyManager
from typing import Literal
from Jugador import Jugador
from Special import Special

posiciones = [("1-1", "1-2", "1-3"),
              ("2-1", "2-2", "2-3"),
              ("3-1", "3-2", "3-3")]

condiciones_de_victoria = [("1-1", "1-2", "1-3"), ("2-1", "2-2", "2-3"), ("3-1", "3-2", "3-3"),
                           ("1-1", "2-1", "3-1"), ("1-2", "2-2", "3-2"), ("1-3", "2-3", "3-3"),
                           ("1-1", "2-2", "3-3"), ("1-3", "2-2", "3-1")]

turno_actual = "o"
casillas_marcadas: list[str] = []

ctk = customtkinter.CTk()
screen_width = ctk.winfo_screenwidth()
screen_height = ctk.winfo_screenheight()
layout = customtkinter.CTkFrame(ctk, width=screen_width, height=screen_height)
layout.pack()

titulo = customtkinter.CTkLabel(layout, text="JUEGO DEL GATO MULTIPROCESOS", width=int(screen_width * 0.4), height=int(screen_height * 0.05))
titulo.place(x=int(screen_width * 0.3), y=int(screen_height * 0.05))

label_p1 = customtkinter.CTkLabel(layout, text="jugador 1: [O]", width=int(screen_width * 0.25), height=int(screen_height * 0.05))
label_p2 = customtkinter.CTkLabel(layout, text="jugador 2: [X]", width=int(screen_width * 0.25), height=int(screen_height * 0.05))

label_p1.place(x=int(screen_width * 0.125), y=int(screen_height * 0.12))
label_p2.place(x=int(screen_width * 0.625), y=int(screen_height * 0.12))

cuadricula_layout_width = int(screen_width / 3)
cuadricula_layout_height = int(screen_height * 0.4)
cuadricula_layout = customtkinter.CTkFrame(layout, width=cuadricula_layout_width, height=cuadricula_layout_height)
cuadricula_layout.place(x=int(screen_width / 3), y=int(screen_height * 0.25))
botones = []

MyManager.register("get_jugador_o_sender")
MyManager.register("get_jugador_x_sender")
MyManager.register("get_pos_sender")
MyManager.register("get_ganador_reciever")
MyManager.register("get_end_game_event")

manager = MyManager.create_default()
manager.connect()

jugador_o_sender = manager.get_jugador_o_sender()
jugador_x_sender = manager.get_jugador_x_sender()
pos_sender = manager.get_pos_sender()
ganador_reciever = manager.get_ganador_reciever()
end_game_event = manager.get_end_game_event()

def on_button_press(boton: customtkinter.CTkButton, casilla):
    global turno_actual
    if casilla in casillas_marcadas or boton.cget("text") != "^": 
        return

    boton.configure(text=turno_actual)
    casillas_marcadas.append(casilla)

    if turno_actual == "x":
        jugador_x_sender.send("turno de x")
        turno_actual = "o"
    else:
        jugador_o_sender.send("turno de o")
        turno_actual = "x"
    pos_sender.send(casilla)

fuente_botones = customtkinter.CTkFont(family="Arial", size=int(cuadricula_layout_width/9), weight="bold")
for i in range(3):
    for j in range(3):
        boton = customtkinter.CTkButton(cuadricula_layout, text="^", width=int(cuadricula_layout_width/3), height=int(cuadricula_layout_height/3),
                                        font=fuente_botones)
        boton.configure(command=lambda btn=boton, casilla=f"{i+1}-{j+1}": on_button_press(btn, casilla))
        boton.place(x=int(j * (cuadricula_layout_width / 3)), y=int(i * (cuadricula_layout_height/3)))
        botones.append(boton)

fuente_label_victoria = customtkinter.CTkFont(family="Arial", size=int(cuadricula_layout_width/11), weight="bold")
label_victoria = customtkinter.CTkLabel(layout, text="---", width=int(screen_width * 0.3), height=int(screen_height * 0.1),
                                        font=fuente_label_victoria)
label_victoria.place(x=int(screen_width * 0.35), y=int(screen_height * 0.7))

def end_game_listener(label_victoria:customtkinter.CTkLabel, end_game_event, turn_o_sender, turn_x_sender, ganador_reciever):
    try:
        end_game_event.wait()
        j_ganador:Jugador = ganador_reciever.recv()
        if j_ganador.nombre == "O":
            turn_x_sender.send(Special.GAME_OVER)
        else:
            turn_o_sender.send(Special.GAME_OVER)
        label_victoria.configure(text=f"jugador {j_ganador.nombre} ha ganado!!!")
    except Exception:
        return

end_game_listener_t = threading.Thread(target=end_game_listener, args=(label_victoria, end_game_event, jugador_o_sender, jugador_x_sender, ganador_reciever))
end_game_listener_t.start()

ctk.mainloop()