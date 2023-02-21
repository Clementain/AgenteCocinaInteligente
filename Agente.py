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
            "ver_recetas": self.ver_recetas,
            "crear_receta": self.crear_receta,
        }

        self.percepciones = []

    def AGENTE(self, percepcion):
        self.percepciones.append(percepcion)
        accion = self.acciones[percepcion["accion"]]()
        return accion

    def buscar_ingrediente(self):
        ingrediente = self.percepciones[-1]["ingrediente"]
        if ingrediente in self.almacen_ingredientes and self.almacen_ingredientes[ingrediente] > 0:
            return {"accion": "buscar_ingrediente", "ingrediente": ingrediente, "cantidad": self.almacen_ingredientes[ingrediente]}
        else:
            return {"accion": "comprar_ingrediente", "ingrediente": ingrediente}

    def ver_almacen_ingredientes(self):
        for ingrediente, cantidad in self.almacen_ingredientes.items():
            print(f"{ingrediente}: {cantidad}")
        return {"accion": "esperar"}

    def ver_recetas(self):
        for receta, ingredientes in self.recetas.items():
            print(f"{receta}:")
            for ingrediente, cantidad in ingredientes.items():
                print(f"  {ingrediente}: {cantidad}")
        return {"accion": "esperar"}

    def comprar_ingrediente(self):
        ingrediente = self.percepciones[-1]["ingrediente"]
        cantidad_comprada = int(input("Ingresa la cantidad a comprar: "))

        if ingrediente not in self.almacen_ingredientes:
            self.almacen_ingredientes[ingrediente] = cantidad_comprada
        else:
            self.almacen_ingredientes[ingrediente] += cantidad_comprada

        return {"accion": "buscar_ingrediente", "ingrediente": ingrediente, "cantidad": cantidad_comprada}

    def crear_receta(self):
        receta = self.percepciones[-1]["receta"]
        if receta in self.recetas:
            print(f"La receta {receta} ya existe")
            return {"accion": "esperar"}
        ingredientes = {}
        while True:
            ingrediente = input("Ingrediente (o 'terminar' para salir): ")
            if ingrediente == "terminar":
                break
            cantidad = int(input("Cantidad: "))
            ingredientes[ingrediente] = cantidad
            self.recetas[receta] = ingredientes
        return {"accion": "esperar"}

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
        "¿Qué acción desea realizar?\nbuscar_ingrediente\ncomprar_ingrediente\nverificar_receta\nver_recetas\ncrear_receta\npreparar_receta\nesperar\nver_almacen_ingredientes\nsalir\n")

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
        agente.ver_recetas

    if accion == "crear_receta":
        percepcion["receta"] = input("Nombre de la nueva receta: ")

    if accion == "ver_almacen_ingredientes":
        agente.ver_almacen_ingredientes

    resultado = agente.AGENTE(percepcion)
    print("El agente realizó la siguiente acción:", resultado)
