class AgenteCocina:
    def __init__(self):
        self.almacen_ingredientes = {
            "harina": 10,
            "huevos": 6,
            "leche": 3,
            "azucar": 5,
        }

        self.recetas = {
            "torta": {"harina": 2, "huevos": 2, "leche": 1, "azucar": 2},
            "panqueques": {"harina": 1, "huevos": 1, "leche": 1},
            "huevo_frito": {"huevos": 1},
        }

        self.acciones = {
            "buscar_ingrediente": self.buscar_ingrediente,
            "comprar_ingrediente": self.comprar_ingrediente,
            "verificar_receta": self.verificar_receta,
            "preparar_receta": self.preparar_receta,
            "esperar": self.esperar,
        }

        self.percepciones = []

    def AGENTE(self, percepcion):
        self.percepciones.append(percepcion)
        accion = self.acciones[percepcion["accion"]]()
        return accion

    def buscar_ingrediente(self):
        ingrediente = self.percepciones[-1]["ingrediente"]
        if ingrediente in self.almacen_ingredientes and self.almacen_ingredientes[ingrediente] > 0:
            return {"accion": "buscar_ingrediente", "ingrediente": ingrediente, "cantidad": 1}
        else:
            return {"accion": "comprar_ingrediente", "ingrediente": ingrediente}

    def comprar_ingrediente(self):
        ingrediente = self.percepciones[-1]["ingrediente"]
        return {"accion": "buscar_ingrediente", "ingrediente": ingrediente, "cantidad": 5}

    def verificar_receta(self):
        receta = self.percepciones[-1]["receta"]
        for ingrediente, cantidad in self.recetas[receta].items():
            if ingrediente not in self.almacen_ingredientes or self.almacen_ingredientes[ingrediente] < cantidad:
                return {"accion": "esperar"}
        return {"accion": "preparar_receta", "receta": receta}

    def preparar_receta(self):
        receta = self.percepciones[-1]["receta"]
        for ingrediente, cantidad in self.recetas[receta].items():
            self.almacen_ingredientes[ingrediente] -= cantidad
        return {"accion": "esperar"}

    def esperar(self):
        return {"accion": "esperar"}


# Ejemplo de uso
agente = AgenteCocina()

print("Buscar ingredientes")
percepcion = {"accion": "buscar_ingrediente", "ingrediente": "harina"}
accion = agente.AGENTE(percepcion)
print(accion)  # {'accion': 'buscar_ingrediente', 'ingrediente': 'harina', 'cantidad': 1}

print("Verificar receta")
percepcion = {"accion": "verificar_receta", "receta": "torta"}
accion = agente.AGENTE(percepcion)
print(accion)  # {'accion': 'esperar'}

print("Comprar ingrediente")
percepcion = {"accion": "comprar_ingrediente", "ingrediente": "harina"}
accion = agente.AGENTE(percepcion)
print(accion) # {'accion': 'buscar_ingrediente', 'ingrediente': 'harina', 'cantidad': 5}

print("Buscar ingredientes (5 unidades)")
for i in range(5):
    percepcion = {"accion": "buscar_ingrediente", "ingrediente": "harina"}
    accion = agente.AGENTE(percepcion)
    print(accion) # {'accion': 'buscar_ingrediente', 'ingrediente': 'harina', 'cantidad': 1}

print("Verificar receta")
percepcion = {"accion": "verificar_receta", "receta": "torta"}
accion = agente.AGENTE(percepcion)
print(accion) # {'accion': 'esperar'}

print("Preparar receta")
percepcion = {"accion": "preparar_receta", "receta": "torta"}
accion = agente.AGENTE(percepcion)
print(accion) # {'accion': 'esperar'}