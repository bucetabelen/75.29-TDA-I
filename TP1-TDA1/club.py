# El algoritmo debe recibir por parámetro el valor n y luego el nombre del archivo que contiene los socios y sus conocidos. 
# El archivo de los socios corresponde a un archivo de texto que tiene una línea por socio seguido de sus conocidos.
# Cumple con el siguiente formato: nro_socio, nombre, nro_socio_conocido1, nro_socio_conocido2, …nro_socio_conocidox


#Realizo el parseo del file y le doy el formato de lista que necesito para aplicar el algoritmo greedy propuesto
def listSocios(n,socios):
    l = []
    with open(socios) as f:
        
        for line in f.readlines():
            line = line.rstrip()
            s = (line.split(',',2))
            aux = []
            subl = []
           
            for i in s[2].split(','):
                aux.append(int(i))
            subl.append(s[0])
            subl.append(s[1])
            subl.append(aux)
            subl.append(len(aux))
            subl.append(True)
            l.append(subl)
    
    invitados(l)
    
    for i in l: 
        if i[4]:
            print("{}, {}".format(i[0], i[1] ))
 
    return l


def socio_con_menos_conocidos(l):
    min_l = int(9999)
    m = [1,1,1,9999]
    
    for i in l:
       
        if (i[3] < min_l) and i[4]:
            m = i
            min_l = i[3]
    
    
    return m

    #Si la cantidad de conocidos del elemento que conoce a menos personas es menor a 4(o a K) entonces entro y lo saco (porque claramente no cumple la condicion) 

def invitados(lista):
    
    m = socio_con_menos_conocidos(lista)# corresponde a un loop 
    
    while (m[3] < 4):  
        
     
        for i in m[2]:
            
            if(lista[i-1][4]):
                
                lista[i-1][3] -= 1 #le restamos uno a la cantidad total de conocidos de cada conocido del socio en cuestión
        m[4] = False
        m = socio_con_menos_conocidos(lista)
       
        
    return lista
    
    
    
    #Una vez termina el while(esto significa que el minimo tiene una cantidad mayor o igual a 4, por lo tanto todos los demas tambien por definicion de minimo), los que quedaron en active son la solucion



# Se deja listo para ejecutar el ejemplo propuesto por el enunciado. Si se desea, puede comentarse este caso y descomentar cualquier
# de los de abajo para probar.
listSocios(9,"socios.txt")
print()
#listSocios(14,"otrosSocios.txt")
print()
#listSocios(5,"sociosQueCumplen.txt")
print()
#listSocios(4,"sociosQueNoCumplen.txt")# En este caso no se imprimirá nada por pantalla puesto que ningún socio cumple la condición
                                        # para ser invitado
