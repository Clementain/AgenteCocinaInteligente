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
            "ver_almacen_ingredientes": self.ver_almacen_ingredientes,
            "ver_recetas": self.ver_recetas
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

    def ver_almacen_ingredientes(self):
        return self.almacen_ingredientes

    def ver_recetas(self):
        return self.recetas

    def comprar_ingrediente(self):
        ingrediente = self.percepciones[-1]["ingrediente"]
        cantidad_comprada = 5

        if ingrediente not in self.almacen_ingredientes:
            self.almacen_ingredientes[ingrediente] = cantidad_comprada
        else:
            self.almacen_ingredientes[ingrediente] += cantidad_comprada

        return {"accion": "buscar_ingrediente", "ingrediente": ingrediente, "cantidad": cantidad_comprada}

    def verificar_receta(self):
        receta = self.percepciones[-1]["receta"]
        if receta not in self.recetas:
            print(f"La receta {receta} no está disponible en este momento.")
            return {"accion": "esperar"}
        for ingrediente, cantidad in self.recetas[receta].items():
            if ingrediente not in self.almacen_ingredientes or self.almacen_ingredientes[ingrediente] < cantidad:
                return {"accion": "esperar"}
        return {"accion": "preparar_receta", "receta": receta}

    def preparar_receta(self):
        receta = self.percepciones[-1]["receta"]
        if receta not in self.recetas:
            print(f"La receta {receta} no está disponible en este momento.")
            return {"accion": "esperar"}
        for ingrediente, cantidad in self.recetas[receta].items():
            self.almacen_ingredientes[ingrediente] -= cantidad
        return {"accion": "esperar"}

    def esperar(self):
        return {"accion": "esperar"}


# # Ejemplo de uso
# agente = AgenteCocina()

# print("Buscar ingredientes")
# percepcion = {"accion": "buscar_ingrediente", "ingrediente": "harina"}
# accion = agente.AGENTE(percepcion)
# print(accion)  # {'accion': 'buscar_ingrediente', 'ingrediente': 'harina', 'cantidad': 1}

# print("Verificar receta")
# percepcion = {"accion": "verificar_receta", "receta": "torta"}
# accion = agente.AGENTE(percepcion)
# print(accion)  # {'accion': 'esperar'}

# print("Comprar ingrediente")
# percepcion = {"accion": "comprar_ingrediente", "ingrediente": "harina"}
# accion = agente.AGENTE(percepcion)
# print(accion) # {'accion': 'buscar_ingrediente', 'ingrediente': 'harina', 'cantidad': 5}

# print("Buscar ingredientes (5 unidades)")
# for i in range(5):
#     percepcion = {"accion": "buscar_ingrediente", "ingrediente": "harina"}
#     accion = agente.AGENTE(percepcion)
#     print(accion) # {'accion': 'buscar_ingrediente', 'ingrediente': 'harina', 'cantidad': 1}

# print("Verificar receta")
# percepcion = {"accion": "verificar_receta", "receta": "torta"}
# accion = agente.AGENTE(percepcion)
# print(accion) # {'accion': 'esperar'}

# print("Preparar receta")
# percepcion = {"accion": "preparar_receta", "receta": "torta"}
# accion = agente.AGENTE(percepcion)
# print(accion) # {'accion': 'esperar'}

agente = AgenteCocina()

while True:
    accion = input(
        "¿Qué acción desea realizar? (buscar_ingrediente, comprar_ingrediente, verificar_receta, ver_recetas, preparar_receta, esperar, ver_almacen_ingredientes, salir): ")

    if accion == "salir":
        break

    if accion not in agente.acciones:
        print("Acción no válida. Intente de nuevo.")
        continue

    percepcion = {"accion": accion}

    if accion == "buscar_ingrediente":
        percepcion["ingrediente"] = input("¿Qué ingrediente está buscando? ")

    if accion == "comprar_ingrediente":
        percepcion["ingrediente"] = input("¿Qué ingrediente desea comprar? ")

    if accion == "verificar_receta":
        percepcion["receta"] = input("¿Qué receta desea verificar? ")

    if accion == "preparar_receta":
        percepcion["receta"] = input("¿Que receta desea preparar?")

    if accion == "ver_recetas":
        agente.AGENTE({"accion": "ver_recetas"})

    if accion == "ver_almacen_ingredientes":
        agente.AGENTE({"accion": "ver_almacen_ingredientes"})

    resultado = agente.AGENTE(percepcion)
    print("El agente realizó la siguiente acción:", resultado)
