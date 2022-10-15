"""
Test 3

Genetic algorithm
This algorith solve a Knapsack problem (KP) with 2 backpacks with 
different (or same) weight.

The parameters of the problem has to be written in a txt file.
The first row of the file has the 2 weigths separated by semicolons (;)
The rest of the file are the different objects
Each object has an id, weigth and value, in that order separated by ;

After the algorithm runs you'll have to wait a little in order to have a
better solution

The parameters of the main function can be changed as you like
Think that higher parameters mean more time of execution but also mean 
a better solution

Enjoy the algorithm

Date of beggining 20/07/2022
Date of finishing 13/10/2022
Author Josep Peiró Ramos
    Supervisor Juan Francisco Correcher Valls
"""

from random import randint as rdt
import copy
import matplotlib.pyplot as plt
import pandas as pd


def CrearFichero(nom:str, num:int, peso_m1:int, peso_m2:int):
    try:
        g = open(nom, "w", encoding = "UTF-8")
    except:
        print("Error de creacion")
    else:
        
        g.write(str(peso_m1) + ";" + str(peso_m2) + "\n")
        for i in range(num):
            peso = rdt(1, int(min(peso_m1, peso_m2) * 0.8))
            valor = rdt(0, int(max(peso_m1, peso_m2) * 2.5))
            g.write(str(i + 1) + ";" + str(peso) + ";" + str(valor) + "\n")
        
        g.close()
        
    return


class Instancia: #Definicion del problema

    def __init__(self):
        self.maleta1 = int() #Peso maximo maleta 1
        self.maleta2 = int() #Peso maximo maleta2
        self.objetos = list() #De Objeto 
        
        
    def LeerFichero(self, nom:str):
        
        try:
            f = open(nom, "r", encoding = "UTF-8")
        except:
            print("Error")
        else:
            
            objetos = []
            
            s = f.readline()
            s = s.strip("\n").split(";")
            mlt1 = max(int(s[0]), int(s[1]))
            mlt2 = min(int(s[0]), int(s[1]))
            
            for linea in f:
                
                o = Objeto()
                l = linea.strip("\n").split(";")
                o.id = int(l[0])
                o.peso = float(l[1])
                o.valor = float(l[2])
                
                objetos.append(o)
                
            f.close()
            
            self.maleta1 = mlt1
            self.maleta2 = mlt2
            self.objetos = objetos            
            
        return


class Objeto:
    
    def __init__(self):
        self.id = int() #Identificador del objeto
        self.peso = float() #Peso del objeto
        self.valor = float() #Valor del objeto
        
    def __str__ (self):
        s = "ID: " + str(self.id) + "\n"
        s += "PESO: " + str(self.peso) + "\n"
        s += "VALOR: " + str(self.valor)
        
        return s
        
   
class AlgoritmoGenetico:
    
    def __init__(self):
        self.individuos = int()
        self.porcentaje_elite = float()
        self.porcentaje_nuevos = float()
        self.porcentaje_mutados = float()
        
        
    def Resolver(self, 
                 tiempo:float, #Todavia no lo usamos
                 inst:Instancia,
                 tamano:int,
                 num_generaciones:int,
                 max_deterioros:int)-> (list, list):
        
        g = open("soluciones.txt", "w")
        almacen = CrearPoblacion(tamano, inst) #Lista de Soluciones
        linaje = Generaciones(inst, almacen, 10.12,
                              tamano, num_generaciones, max_deterioros, g)
        
        lista_mejores_soluciones = []
        for a in range(len(linaje)):
            sol, val = MejorSolucion(linaje[a])
            lista_mejores_soluciones.append(val)
        
        return linaje, lista_mejores_soluciones
    
    
    def MostrarSolucion(self, 
                        tiempo:float, #Todavia no lo usamos
                        inst:Instancia,
                        tamano:int,
                        num_generaciones:int,
                        max_deterioros:int):
        
        linaje, lista_mejores_soluciones = self.Resolver(tiempo = tiempo, #Todavia no lo usamos
                               inst = inst,
                               tamano = tamano,
                               num_generaciones = num_generaciones,
                               max_deterioros = max_deterioros)
        
        df = pd.DataFrame({
            "index":list(range(len(linaje))),
            "solucion":lista_mejores_soluciones
            })
        
        df.plot(x = "index", y = "solucion", kind = "line",
                title = "Tamaño: " + str(tamano) + \
                    " Generaciones: " + str(num_generaciones))
        plt.show()
        """
        sol_viejo, val_viejo = MejorSolucion(linaje[0])
        sol, val = MejorSolucion(linaje[len(linaje) - 1])
        print(val_viejo)
        print(val)
        """
        print("Primera Solucion", MejorSolucion(linaje[0])[1])
        #print(MejorSolucion(linaje[0])[1])
        #print("----------------------------------------------------")
        mejor = max(lista_mejores_soluciones)
        #print("Mejora:", (mejor - MejorSolucion(linaje[0])[1]))
        print("Mejor Solucion:", mejor)
        indice_mejor = lista_mejores_soluciones.index(mejor)
        print("Indice solucion:", indice_mejor)
        print()
        print("Descripcion de las soluciones:")
        print(MejorSolucion(linaje[indice_mejor])[0])
                
        
class Solucion:
    
    def __init__(self):
        self.lista1 = [] #De Objeto, lo que lleva la maleta 1
        self.lista2 = [] #De Objeto, lo que lleva la maleta 2
        
    def __str__ (self):
        
        p1 = 0
        p2 = 0
        v = 0
        s = "Id Lista 1: "
        for r in self.lista1:
            p1 += r.peso
            v += r.valor
            s += str(r.id) + ", "
        s += "\n Id Lista 2: "
        for r in self.lista2:
            p2 += r.peso
            v += r.valor
            s += str(r.id) + ", "
        s += "\nPeso Lista 1: " + str(p1) + "\n"
        s += "Peso Lista 2: " + str(p2) + "\n"
        s += "Valor Total: " + str(v)
        
        return s
        

def MejorSolucion(poblacion:list):
    
    mejor_solucion = poblacion[0]
    mejor_valor = CalcularValorTotal(poblacion[0])
    
    for individuo in range(len(poblacion) - 1):
        valor = CalcularValorTotal(poblacion[individuo + 1])
        if valor > mejor_valor:
            mejor_valor = valor
            mejor_solucion = poblacion[individuo + 1]
            
    return mejor_solucion, mejor_valor
                        

def CrearPoblacion(tamano:int, inst:Instancia)->list:
    
    solucion_constructiva = Constructivo(inst)
    almacen = [solucion_constructiva]
    #almacen = []
    for individuo in range(tamano):
    #for individuo in range(tamano - 1):
        solucion_aleatoria = ConstructivoAleatorio(inst)
        almacen.append(solucion_aleatoria)

    return almacen


def Generaciones(inst:Instancia, poblacion:list, prob_mut:int,
                 tamano:int, num_generaciones:int, 
                 max_deterioros:int, g) -> list:
    
    pob = copy.deepcopy(poblacion)
    linaje = [pob]
    generacion = SeleccionNatural(inst, copy.deepcopy(poblacion), 
                                  prob_mut, tamano)
    linaje.append(generacion)
    
    """
    for reproduccion in range(num_generaciones - 1):
        generacion = SeleccionNatural(inst, copy.deepcopy(generacion), 
                                      prob_mut, tamano)
        linaje.append(generacion)
        """
        
    maximo = False
    deterioros = 0
    iteraciones = 2
    mejor = MejorSolucion(pob)[1]
    while not maximo and iteraciones <= num_generaciones:
        generacion = SeleccionNatural(inst, copy.deepcopy(generacion), 
                                      prob_mut, tamano)
        linaje.append(generacion)
        
        mejor_gen = MejorSolucion(generacion)[1]
        
        if mejor_gen - mejor <= 0:
            deterioros += 1
        else:
            deterioros = 0
            mejor = mejor_gen
        
        if deterioros >= max_deterioros:
            maximo = True
            
        iteraciones += 1
        g.write(str(iteraciones) + "\t" + str(mejor) +
              "\t" + str(mejor_gen) + "\t" + str(mejor_gen - mejor) +
              "\t" + str(deterioros) + "\n")
        
        #if MejorSolucion(generacion)[1] > MejorSolucion(linaje[0])[1]:
        #    print("Mejorada", MejorSolucion(generacion)[1] - MejorSolucion(linaje[0])[1])
        #else:
        #    print("Empeorada", MejorSolucion(linaje[0])[1] - MejorSolucion(generacion)[1])

    return linaje


def SeleccionNatural(inst:Instancia, 
                     poblacion:list, 
                     prob_mut:int, 
                     tamano:int) -> list:
    
    nueva_generacion = poblacion
    for apareamiento in range(int(tamano * 2)):
        indice_padre = rdt(0, len(poblacion)-1)
        indice_madre = rdt(0, len(poblacion)-1)
        
        while indice_padre == indice_madre:
            indice_madre = rdt(0, len(poblacion)-1)
        
        nueva_generacion.append(Combinar(inst, 
                                          poblacion[indice_padre],
                                          poblacion[indice_madre]))
    
    for individuo in nueva_generacion:
        
        if Probabilidad(prob_mut):
            Mutacion(inst, individuo)
    
    lista_valores = []
    for valor in nueva_generacion:
        lista_valores.append(CalcularValorTotal(valor))
    
    supervivientes = []
    indice_supervivientes = []
    for i in range(len(lista_valores)):
        if lista_valores[i] > (sum(lista_valores) / len(lista_valores)) * 1.2:
            supervivientes.append(nueva_generacion[i])
            indice_supervivientes.append(i)
            
    for vivos in range(len(indice_supervivientes) - 1, -1, -1):
        nueva_generacion.pop(indice_supervivientes[vivos])
        
    while len(supervivientes) <= tamano:
        indice_suerte = IndiceAleatorio(nueva_generacion)
        supervivientes.append(nueva_generacion[indice_suerte])
        nueva_generacion.pop(indice_suerte)
    
    return supervivientes


def Combinar(inst:Instancia, ind1:Solucion, ind2:Solucion) -> Solucion:
    
    hijo = Solucion()
    
    objetos = []
    for obj in (ind1.lista1 + ind1.lista2 + ind2.lista1 + ind2.lista2):
        if obj not in objetos:
            objetos.append(obj)
            
    objetos = sorted(objetos, key = lambda x: x.peso)

    
    peso_restante = inst.maleta1
    while len(objetos) != 0 and objetos[0].peso < peso_restante:
        
        indice_obj = IndiceAleatorio(objetos)
        if objetos[indice_obj].peso <= peso_restante:
            hijo.lista1.append(objetos[indice_obj])
            peso_restante -= objetos[indice_obj].peso
            objetos.pop(indice_obj)
    peso_restante = inst.maleta2
    
    while len(objetos) != 0 and objetos[0].peso < peso_restante:
        indice_obj = IndiceAleatorio(objetos)
        if objetos[indice_obj].peso <= peso_restante:
            hijo.lista2.append(objetos[indice_obj])
            peso_restante -= objetos[indice_obj].peso
            objetos.pop(indice_obj)
    
    return hijo


def Mutacion(inst:Instancia, individuo:Solucion):
    
    #Guarda los id de los objetos que ya hemos usado
    lista_id = []
    
    for objeto in individuo.lista1:
        lista_id.append(objeto.id)
        
    for objeto in individuo.lista2:
        lista_id.append(objeto.id)
        
    #Elige una de las 2 maletas para hacer el cambio  
    if rdt(0,1) == 0:
        lista_cambio = individuo.lista1
        peso_maximo = inst.maleta1
        
    else:
        lista_cambio = individuo.lista2
        peso_maximo = inst.maleta2

    elemento_cambio = IndiceAleatorio(lista_cambio)
    lista_cambio.pop(elemento_cambio)
    
    peso_maleta_sin_objeto = 0
    for objeto in lista_cambio:
        peso_maleta_sin_objeto += objeto.peso
        
    peso_restante = peso_maximo - peso_maleta_sin_objeto
    objeto_escogido = False
    paciencia = 0
    while not objeto_escogido:
        
        indice = IndiceAleatorio(inst.objetos)
        
        if inst.objetos[indice].peso <= peso_restante and \
            inst.objetos[indice].id not in lista_id:
                lista_cambio.append(inst.objetos[indice])
                objeto_escogido = True
                
        paciencia += 1
        
        if paciencia >= 10000:
            objeto_escogido = True
    
    return
       

def Probabilidad(prob:int)->float: #Se le pasa el numero sobre 100
    
    numero_aleatorio = rdt(0,99999)
    if numero_aleatorio < prob * 1000:
        respuesta = True
    
    else:
        respuesta = False
        
    return respuesta


def IndiceAleatorio(lista:list)->int:
            
    elemento = rdt(0, len(lista)-1)
    return elemento


def CalcularValorTotal(sol:Solucion):
    
    valor_total = 0
    for obj in sol.lista1:
        valor_total += obj.valor
    for obj in sol.lista2:
        valor_total += obj.valor
        
    return valor_total


def ConstructivoAleatorio(inst:Instancia)-> Solucion:
    
    maleta1 = []
    maleta2 = []
    peso_maleta1 = inst.maleta1
    peso_maleta2 = inst.maleta2
    
    obj = inst.objetos.copy()
    
    continua = True
    while peso_maleta1 > 0 and continua and len(obj) > 0:
        
        indice_seleccion = IndiceAleatorio(obj)
        elemento = obj[indice_seleccion]

        if peso_maleta1 > elemento.peso:
            maleta1.append(elemento)
            obj.pop(indice_seleccion)
            peso_maleta1 -= elemento.peso
            
        else:
            continua = False
            
    continua = True
    while peso_maleta2 >0 and continua and len(obj) > 0:
        
        indice_seleccion = IndiceAleatorio(obj)
        elemento = obj[indice_seleccion]

        if peso_maleta2 > elemento.peso:
            maleta2.append(elemento)
            obj.pop(indice_seleccion)
            peso_maleta2 -= elemento.peso
            
        else:
            continua = False
            
    sol = Solucion()
    sol.lista1 = maleta1
    sol.lista2 = maleta2
    
    return sol


def RelacionPesoValor(inst:Instancia) -> list:
    
    relacion = []
    
    for i in range(len(inst.objetos)):
        relacion.append(inst.objetos[i].valor / inst.objetos[i].peso)
        
    return relacion


def IndiceMayorRelacion(relacion_ordenada:list, relacion:list, i:int) -> int:
    
    indice = relacion.index(relacion_ordenada[i])    
    
    return indice


def Constructivo(inst:Instancia)-> Solucion:

    peso_maleta1 = inst.maleta1
    peso_maleta2 = inst.maleta2
    
    maleta1 = []
    maleta2 = []
    
    relacion = RelacionPesoValor(inst)
    relacion_aux = relacion.copy()
    
    relacion_ordenada = sorted(relacion.copy(), reverse=True)
    
    i = 0
    while peso_maleta1 > 0 and i < len(relacion):
        indice = IndiceMayorRelacion(relacion_ordenada, relacion_aux, i)

        if peso_maleta1 >= inst.objetos[indice].peso:
            maleta1.append(indice + 1)
            peso_maleta1 -= inst.objetos[indice].peso
            relacion_aux[indice] = -1
            
        i +=1
     
    relacion_restante = relacion.copy()
    for elegido in sorted(maleta1, reverse = True):
        relacion_restante.pop(elegido-1)
            
    relacion_restante_ord = sorted(relacion_restante, reverse = True)
    

    j = 0
    while peso_maleta2 > 0 and j < len(relacion_restante_ord):
        
        indice = IndiceMayorRelacion(relacion_restante_ord, relacion_aux, j)

        if peso_maleta2 >= inst.objetos[indice].peso:
            maleta2.append(indice + 1)
            peso_maleta2 -= inst.objetos[indice].peso
            relacion_aux[indice] = -1
            
        j +=1

    mlt1 = []
    mlt2 = []
    for k in maleta1:
        mlt1.append(inst.objetos[k-1])
    for l in maleta2:
        mlt2.append(inst.objetos[l-1])
        
    sol = Solucion()
    sol.lista1 = mlt1
    sol.lista2 = mlt2
    
    return sol
    
            
def main():
    
    print(__doc__)
    print("Loading")
    
    inst = Instancia()
    CrearFichero(nom = "datos_aleatorios_problema_optimizacion.txt",
                 num = 5000, peso_m1 = 360, peso_m2 = 248)
    inst.LeerFichero("datos_aleatorios_problema_optimizacion.txt")
    
    gen = AlgoritmoGenetico()
    print("A solution is being created")
    print()
    gen.MostrarSolucion(30, inst, tamano = 200, num_generaciones = 1500,
                 max_deterioros = 300)
    
if __name__ == '__main__':
    main()