import argparse

MENOS_INFINITO = -999

# Objeto que representa a una caja y sus propiedades

class Caja:
     def __init__(self, cod, largo, altura):
        self.cod = cod
        self.largo = int(largo)
        self.altura = int(altura)

# Funcion que lee un archivo linea por linea y crea la lista de objetos de tipo Caja

def readFile(path):
    with open(path) as f: lines = [ line.strip() for line in f ]
    cajas = []
    for line in lines:
        arr_caja = line.split(',')
        caja = Caja(arr_caja[0], arr_caja[1], arr_caja[2])
        cajas.append(caja)

    return cajas

# Funcion que lee los parametros del programa por línea de comando y devuelve el nombre del archivo que contiene la informacion, la cantidad de cajas y
# el largo de las repisas

def readArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='path del archivo que contiene la información de las cajas')
    parser.add_argument('largo',  type=int, help='cantidad de cajas')
    parser.add_argument('n',  type=int, help='largo de las repisa')
    args = parser.parse_args()

    return args.path, args.n, args.largo

# Función que hace uso de la programación dinámica para disponer las cajas ordenadas de manera que se minimice la altura total de los estantes, devuelve la mínima altura
# y el array de estantes a la que corresponde cada caja

def disponerCajas(cajas, L, n):
    max_alturas = [0] * (n+1)
    estantes = [0] * (n+1)

    for i in range(1,n+1):

        # Cargo largo y altura de la caja actual
        largo = cajas[i-1].largo
        altura = cajas[i-1].altura

        # La altura total de los estantes si se pusiese la caja actual en un estante diferent
        max_alturas[i] = max_alturas[i-1] + altura

        # Recorremos desde la caja anterior para atras hasta la primera caja que no entre habiendo incluido las cajas anteriores en un mismo estante que la caja actual
        for j in range(i-1,0,-1):
            
            # si la caja en la posición j anterior a i entra la meto
            if (largo + cajas[j-1].largo <= L):
                
                # cambio la altura a la maxima entre el valor actual de altura y la altura de la caja que voy a agregar
                altura = max(altura, cajas[j-1].altura)
                # cambio el largo ocupado del estante sumandole la nueva caja que voy a agregar
                largo = largo + cajas[j-1].largo

                # si la nueva altura total de los estanmtes es menor a la altura que teniamos guardada entro
                if (altura + max_alturas[j-1] <= max_alturas[i]):
                    # cambio la altura que teniamos guardada por la menor
                    max_alturas[i] = altura + max_alturas[j-1]
                    # agrego la posición del estante que potencialmente puede ir con esa caja
                    estantes[i] = j

            # si la caja en la posición j anterior a i no entra salgo
            else:
                break
    
    return max_alturas[n], estantes

# Función que se encarga de imprimir las cajas pertenecientes a cada estante con la ayuda del array estantes devuelto por la funcion disponerCajas

def imprimirCajas(cajas, estantes, n):
    i = n
    num_estante = 1
    while i > 0:
        tail = estantes[i] - 1
        print("En el estante "+str(num_estante)+":", end=' ')
        if(tail >= 0):  
            dif = i - (tail)
            for j in range(tail, i):
                print(cajas[j].cod, end=' ')
            print("")
        else:
            print(cajas[i-1].cod)
            dif = 1 
        
        i = i - dif
        num_estante += 1


# Main

if __name__=="__main__":

    archivo, n, L = readArguments()
    cajas = readFile(archivo)
    min_altura, estantes = disponerCajas(cajas, L, n)
    print("La mínima altura de todos los estantes será: " + str(min_altura))
    imprimirCajas(cajas, estantes, n)


