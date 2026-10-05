from Varios import nuevo_tema

nuevo_tema("Diccionarios")

aula_micro = {
    "alumnos" : 15,
    "mesas": 4,
    "sillas": 20,
    "pizarron": 1
}

print(aula_micro)
# acceder a un elemento del diccionario
print('aula_micro.get("alumnos"):', aula_micro.get("alumnos"))

# cambiando un elemento del diccionario
aula_micro.update({"mesas" : 6 })

print(aula_micro)
# obteniendo las parejas de elmentos
print("aula_micro.items():", aula_micro.items())

# obteniendo las claves
print("aula_micro.keys():", aula_micro.keys())

# obteniendo los valores
print("aula_micro.values():", aula_micro.values())

for clave, valor in aula_micro.items():
    print(f"{clave}.- {valor} ")