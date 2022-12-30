import sys

def agregar_nodo(linea, matriz_adyacencia, diccionario, num_tarea, dependencia):
  if dependencia:
    primero = diccionario.get(linea[0])
    segundo = diccionario.get(linea[num_tarea])
    matriz_adyacencia[primero][segundo] = int(linea[num_tarea+1])
    matriz_adyacencia[segundo][primero] = int(linea[num_tarea+1])
  else:
    matriz_adyacencia[0][num_tarea] = int(linea[1])
    matriz_adyacencia[num_tarea][1] = int(linea[2])

def leer_archivo(name_file):
  f = open(name_file, "r")
  matriz_adyacencia = list()
  cant_tareas = 0
  diccionario = {'S':0, 'T':1}

  #Leo una vez el archivo para setear el diccionario y obtener la cantidad de tareas
  for linea in f:
    linea = linea.rstrip().split(",")
    diccionario[linea[0]] = cant_tareas+2
    cant_tareas += 1

  #Creo la matriz de adyacencia con todos ceros
  for i in range (0, cant_tareas+2):
    matriz_adyacencia.append([0]*(cant_tareas+2))

  f.seek(0)
  num_tarea = 2

  #Leo el archivo y voy seteando los valores de la matriz
  for linea in f:
    linea = linea.rstrip().split(",")
    agregar_nodo(linea, matriz_adyacencia, diccionario, num_tarea ,False)
    contador = 3
    for i in linea[3:]:
      if not i.isnumeric(): 
        agregar_nodo(linea, matriz_adyacencia, diccionario, contador, True)
      contador += 1
    num_tarea += 1
  f.close()

  return diccionario, matriz_adyacencia

class Grafo:
    def __init__(self, grafo):
        self.residual = grafo
        self.filas = len(grafo)

    #Devuelve un camino de aumento de flujo s-t
    def BFS(self, s, t, padre):
        nodos_visitados =[False]*(self.filas)
        acumulados=[]
        acumulados.append(s)
        nodos_visitados[s] = True

        while acumulados:
            u = acumulados.pop(0)

            for ind, val in enumerate(self.residual[u]):
                if nodos_visitados[ind] == False and val > 0 :
                    acumulados.append(ind)
                    nodos_visitados[ind] = True
                    padre[ind] = u

        return True if nodos_visitados[t] else False

    # Devulve el flujo maximo desde s a t en el grafo dado
    def FordFulkerson(self, fuente, sumidero):
        padre = [-1]*(self.filas)
        flujo_max = 0

        while self.BFS(fuente, sumidero, padre) :
            flujo_camino = float("Inf")
            s = sumidero
            while(s != fuente):
                flujo_camino = min (flujo_camino, self.residual[padre[s]][s])
                s = padre[s]

            flujo_max += flujo_camino

            v = sumidero
            while(v != fuente):
                u = padre[v]
                self.residual[u][v] -= flujo_camino
                self.residual[v][u] += flujo_camino
                v = padre[v]
        tareas_equipo1 = []
        tareas_equipo2 = []
        numero_tareas = 1
        for tarea in self.residual[0][2:]:
          if tarea == 0:
            tareas_equipo1.append(numero_tareas)
          else:
            tareas_equipo2.append(numero_tareas)
          numero_tareas = numero_tareas + 1

        return flujo_max, tareas_equipo1, tareas_equipo2


#name_file = sys.argv[1]
name_file = "proyectos.txt"
diccionario, matriz_grafo = leer_archivo(name_file)
grafo = Grafo(matriz_grafo)
flujo_max, equipo_1, equipo_2 = grafo.FordFulkerson(0,1)
print("El costo minimo de hacer todas las tareas es: ", flujo_max)
clave_lista = list(diccionario.keys())
valores_lista = list(diccionario.values())


for i in equipo_1:
  posicion = valores_lista.index(i+1)
  print("La tarea:", clave_lista[posicion], "es asignada al equipo 1")

for j in equipo_2:
  posicion = valores_lista.index(j+1)
  print("La tarea:", clave_lista[posicion], "es asignada al equipo 2")