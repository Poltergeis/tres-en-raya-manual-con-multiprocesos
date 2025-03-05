from typing import Literal

class Jugador:
    def __init__(self, nombre:str):
        self.nombre:Literal["O", "X"] = nombre
        self._posiciones:list[str] = []
        self._win_conds:list[tuple[str,str,str]] = [("1-1", "1-2", "1-3"), ("2-1", "2-2", "2-3"), ("3-1", "3-2", "3-3"),
                                                    ("1-1", "2-1", "3-1"), ("1-2", "2-2", "3-2"), ("1-3", "2-3", "3-3"),
                                                    ("1-1", "2-2", "3-3"), ("1-3", "2-2", "3-1")]
        
        
    def guardar_pos(self, pos:str):
        self._posiciones.append(pos)
        
    def checar_victoria(self):
        for win_cond in self._win_conds:
            if set(win_cond).issubset(set(self._posiciones)):
                return True
        return False