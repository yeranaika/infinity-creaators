# inventory.py
class Item:
    def __init__(self, nombre, tipo, modificador):
        self.nombre = nombre
        self.tipo = tipo  # Puede ser "arma", "armadura", "consumible", etc.
        self.modificador = modificador  # Diccionario con los cambios en las estadísticas

class Inventory:
    def __init__(self):
        self.items = []  # Lista de objetos en el inventario
        self.equipado = {"arma": None, "armadura": None}  # Objetos equipados

    def agregar_item(self, item):
        self.items.append(item)

    def equipar_item(self, item):
        if item.tipo in self.equipado:
            if self.equipado[item.tipo]:
                # Si ya hay un objeto equipado, devolver sus efectos
                self.quitar_item(self.equipado[item.tipo])
            self.equipado[item.tipo] = item
            return item.modificador

    def usar_item(self, item, jugador):
        for stat, value in item.modificador.items():
            setattr(jugador, stat, getattr(jugador, stat) + value)
        self.items.remove(item)

    def quitar_item(self, item):
        if item.tipo in self.equipado and self.equipado[item.tipo] == item:
            self.equipado[item.tipo] = None
            return {stat: -value for stat, value in item.modificador.items()}