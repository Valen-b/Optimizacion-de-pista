import os
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

#parametros para ajuste de precision
discretizacion = 30 #DEBE SER PAR  #indica en cuantos cuadrados diferenciales va a ser dividido cada direccion del sistema de referencia
incremento_en_el_angulo = 10

#parametros globales
max_velocidad = 50
velocidad_max_adm = 24

lado = max_velocidad*2 / discretizacion
area = lado*lado

#parametros auxiliares para la determinacion de pertenencia de cuadrados diferenciales a trapecios
bool_NO_O = True
bool_NE_N = True
bool_SO_S = True
bool_SE_E = True

class Trapecio:
    def __init__(self,direccion,velocidad_inf,velocidad_sup,frecuencia):
        self.direccion = direccion
        self.velocidad_inf = velocidad_inf
        self.velocidad_sup = velocidad_sup
        self.frecuencia = frecuencia
        self.area_total = 0
        self.area_parcial = 0

class Cuadrado_Diferencial:

    def __init__(self,x,y):
        self.x_coor = x
        self.y_coor = y
        self.trape = None
        self.adentro = False

    def en_cual_trapecio(self):
        vel, ang = rec_to_polar(self.x_coor,self.y_coor)

        direccion = None
        vel_inf = None
        vel_sup = None

        global bool_NO_O
        global bool_NE_N
        global bool_SO_S
        global bool_SE_E

        if 0<ang<45 or ang == 360:
            direccion = "NE"
        elif 45<ang<90:
            direccion = "N"
        elif 90<ang<135:
            direccion = "NO"    
        elif 135<ang<180:
            direccion = "O"    
        elif 180<ang<225:
            direccion = "SO"
        elif 225<ang<270:
            direccion = "S"
        elif 270<ang<315:
            direccion = "SE"
        elif 315<ang<360:
            direccion = "E"


        if ang==45 and bool_NE_N:
            direccion = "NE"
            bool_NE_N = not(bool_NE_N)
        elif ang==45 and not(bool_NE_N):
            direccion = "N"
            bool_NE_N = not(bool_NE_N)

        elif ang==135 and bool_NO_O:
            direccion = "NO"
            bool_NO_O = not(bool_NO_O)
        elif ang==135 and not(bool_NO_O):
            direccion = "O"
            bool_NO_O = not(bool_NO_O) 

        elif ang==225 and bool_SO_S:
            direccion = "SO"
            bool_SO_S = not(bool_SO_S)
        elif ang==225 and not(bool_SO_S):
            direccion = "S"
            bool_SO_S = not(bool_SO_S)

        elif ang==315 and bool_SE_E:
            direccion = "SE"
            bool_SE_E = not(bool_SE_E)
        elif ang==315 and not(bool_SE_E):
            direccion = "E"
            bool_SE_E = not(bool_SE_E)

        c3 = 0
        for c3 in range(0,len(lista_v_sup)):
            if vel >= lista_v_inf[c3] and vel < lista_v_sup[c3]:
                vel_inf = lista_v_inf[c3]
                vel_sup = lista_v_sup[c3]
        if vel == lista_v_sup[-1]:
            vel_inf = lista_v_inf[-1]
            vel_sup = lista_v_sup[-1]

        asignado = False
        for e in lista_trapecios:

            if str(e.direccion) == str(direccion) and e.velocidad_sup == vel_sup and e.velocidad_inf == vel_inf:
                self.trape = e
                asignado = True
        
        if not(asignado):
            self.trape = lista_trapecios[-1]

#funcion auxiliar que transforma un par de coordenadas rectangulares a polares
def rec_to_polar(xx,yy):

    velocidad = math.sqrt(xx*xx+yy*yy)

    dotProduct = xx
    modOfVector = math.sqrt(xx*xx + yy*yy) 
    try:
        angle = dotProduct/modOfVector
    except:
        angle = 0
    angulo = math.degrees(math.acos(angle))
    if yy <0:
        angulo = 360 - angulo

    return velocidad, angulo

#cos for a value in degrees
def cos_d(var):
    return round(math.cos(math.radians(var)),15)
#sin for a value in degrees
def sin_d(var):
    return round(math.sin(math.radians(var)),15)


#INICIO-----------------------------------------------------------------------------------------------------------

#lectura de datos
datos = pd.read_excel(r'C:\Users\Valen\My Drive\8vo semestre\5. Transporte II\TPS Transporte II\TP1\Datos.xlsx', sheet_name='Datos en limpio', header=None)

#guardar datos segun el formato de la clase "Trapecio"
lista_trapecios = []
rows, columns = datos.shape
for r in range(2,rows):
    for c in range(1,columns):
        lista_trapecios.append(Trapecio( datos.iat[r,0], datos.iat[0,c],datos.iat[1,c],datos.iat[r,c]))

#agrega un trapecio auxiliar al cual se asignaran todos los cuadrados diferenciales que queden por fuera de la mayor velocidad considerada.
lista_trapecios.append(Trapecio("-",999,999,0))

#almacena los rangos de velocidades
lista_v_inf = []
lista_v_sup = []
for c in range(1,columns):
    lista_v_inf.append(datos.iat[0,c])
    lista_v_sup.append(datos.iat[1,c])

#a continuacion se crean los cuadrados y se determina a que trapecio pertenece cada uno
cuadrados = [[Cuadrado_Diferencial(0, 0) for _ in range(discretizacion)] for _ in range(discretizacion)]#de esta manera cada uno de las instancias de la clase Cuadrado_Diferencial son independientes entre si.
x = -max_velocidad + lado/2
y = -max_velocidad + lado/2

c1 = 0
c2 = 0
for c1 in range(0, discretizacion):
    y = -max_velocidad + lado/2
    c2 = 0
    for c2 in range(0,discretizacion):
        cuadrados[c1][c2].x_coor = x
        cuadrados[c1][c2].y_coor = y
        cuadrados[c1][c2].en_cual_trapecio()
        y = y + lado
    x = x + lado

#se determina el area total de cada trapecio
for e in lista_trapecios:

    c1 = 0
    c2 = 0
    for c1 in range(0, discretizacion):
        for c2 in range(0,discretizacion):
            if e == cuadrados[c1][c2].trape:
                e.area_total = e.area_total + area


#se determinan las rectas que definen a la pista para el ancho dado, y para un angulo alfa

# Use cross product to determine whether a point lies above or below a line.
#   Math: https://math.stackexchange.com/a/274728
#   English: "above" means that looking from point a towards point b, 
#               the point p lies to the left of the line.
is_above = lambda p,a,b: np.cross(p-a, b-a) < 0

alfa = 0
incremento_de_alfa = incremento_en_el_angulo
a = velocidad_max_adm
operatividad = 0
resultados = []

while alfa <= 180:

    print(round(alfa/180*100,2),"%")

    #inicializacion de parametros para una posicion de pista
    for c1 in range(0, discretizacion):
        for c2 in range(0, discretizacion):
            cuadrados[c1][c2].adentro = False

    for e in lista_trapecios:
        e.area_parcial = 0

    operatividad = 0

    #a y b son puntos que estan sobre uno de los filos de la pista. Un par de puntos por cada filo de la pista.
    a1 = np.array([sin_d(alfa)*a, -cos_d(alfa)*a])
    b1 = np.array([sin_d(alfa)*a + cos_d(alfa)*a, -cos_d(alfa)*a + sin_d(alfa)*a])

    a2 = np.array([-sin_d(alfa)*a, cos_d(alfa)*a])
    b2 = np.array([-sin_d(alfa)*a + cos_d(alfa)*a, cos_d(alfa)*a + sin_d(alfa)*a])


    #se busca cuales cuadrados diferenciales estan dentro de la pista, y al final de loop cada trapecio tendrá almacenada el area total de todos los cuadrados de ese trapecio que están dentro de la pista
    c1 = 0
    c2 = 0
    for c1 in range(0, discretizacion):
        for c2 in range(0, discretizacion):
            if is_above(np.array([cuadrados[c1][c2].x_coor,cuadrados[c1][c2].y_coor]),a1,b1) and not(is_above(np.array([cuadrados[c1][c2].x_coor,cuadrados[c1][c2].y_coor]),a2,b2)):
                cuadrados[c1][c2].adentro = True
                cuadrados[c1][c2].trape.area_parcial = cuadrados[c1][c2].trape.area_parcial + area

    #se calcula la operatividad en base a la cantidad de cuadrados de cada trapecio que están dentro de la pista y de la frecuencia de cada trapecio
    for e in lista_trapecios:
        operatividad = e.frecuencia * (e.area_parcial / e.area_total) + operatividad

    #se imprimen los cuadrados diferenciales del sistema de referencia, segun si están o no dentro de la pista.
    os.system('cls')
    c1 = discretizacion-1
    while c1 >= 0:
        c2 = 0
        while c2 <= discretizacion-1:
            if cuadrados[c2][c1].trape == lista_trapecios[-1]:
                print(" \t", end="")
            elif cuadrados[c2][c1].adentro:
                print("🔵 \t", end="")
            else:
                print("o\t", end="")
            c2 = c2 + 1

        c1 = c1 - 1
        print("\n")
    print("\n")

    resultados.append([operatividad, alfa])

    alfa = alfa + incremento_de_alfa

print("RESULTADOS:")
max = resultados[0]
x =[]
y = []
for e in resultados:
    if e[0] > max[0]:
        max = e
    y.append(e[0])
    x.append(e[1])

print("---------------------------------------------------------------------------------------------------")
print("La mejor posición de la pista es:")
print(str(max[1]) + "°, resultando en una operatividad de " + str(round(max[0],2)) + "%" )
print("---------------------------------------------------------------------------------------------------\n")

plt.scatter(x, y)
plt.show()