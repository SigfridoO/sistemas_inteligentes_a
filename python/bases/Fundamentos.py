from Varios import nuevo_tema

print ("hola mundo")



nuevo_tema("Variables")
nombre = "Mauricio"
edad = 21
estatura = 1.70
fuma = True

print("nombre:", nombre)
print("edad:", edad)
print("estatura:", estatura)
print("fuma:", fuma)


nuevo_tema("Operadores aritmeticos")
a = 11
b = 3
print("a: ", a)
print("b:", b)
print ("a + b: ", a + b)
print ("a - b: ", a - b)
print ("a * b: ", a * b)
print ("a / b: ", a / b)
print ("a % b: ", a % b)
print ("a ** b: ", a ** b)


nuevo_tema("Operadores de comparación")
print ("a > b:", a > b)
print ("a >= b:", a > b)
print ("a < b:", a < b)
print ("a <= b:", a <= b)
print ("a == b :", a == b)

nuevo_tema("Operadores de lógicos")
print ("True  OR False: ", True or False)
print ("True  AND False: ", True and False)
print ("NOT False: ", not False)

nuevo_tema("Operadores a nivel de bits")
a = 11
b= 5
print ("a: ", a)
print ("b: ", b)
print ("a | b:", a | b)
print ("a & b:", a & b)
print ("a ^ b:", a ^ b)
print ("~a:", ~a)
print ("a>>1:", a>>1)
print ("a<<1:", a<<1)

nuevo_tema("Instrucciones de control")
numero1 = 3
numero2 = 5
print("numero1: ", numero1)
print("numero2: ", numero2)
if numero1 > numero2:
    print("numero1 es mayor a numero2")
else:
    print("numero1 no esmayor a numero2")


nuevo_tema("Listas")
frutas = []
frutas = ['manzanas', 'limones', "platanos", "sandias", "kiwis", "naranjas"]
print("frutas:" , frutas)

mi_lista = ['peras', 23.6, True, frutas]
print("mi_lista:", mi_lista)

print ("seleccionando un elemento: frutas[1]:", frutas[1])
print ("seleccionando un elemento: frutas[3]:", frutas[3])

# agregando elementos 
frutas.append("melones")
frutas.append("papayas")
print("frutas: ", frutas)

print ("seleccionando un rango: frutas[1:5]:", frutas[1:5])
print ("seleccionando el ultimo: frutas[-1]:", frutas[-1])
print ("numero de elementos:", len(frutas))
print ("del 1 al 7 de 2 en 2:", frutas[1:8:2])


# ==================== Funciones =====================

