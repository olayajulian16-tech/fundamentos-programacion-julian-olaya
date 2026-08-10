from ucimlrepo import fetch_ucirepo 
import numpy as np
import pandas as pd

student_performance = fetch_ucirepo(id=320)

X = student_performance.data.features
y = student_performance.data.targets

df = pd.concat([X, y], axis=1)
#print(df.head(),df.tail())
     

#revisamos que tenemos en el principio y en el fin

#ahora vamos a revisar cuantas columnas y filas tenemos
#print(df.shape)
#vamos a revisar que tipo de datos tenemos

##print(df.dtypes)  
##print(df.info())
#vamos hacer un analisis de estadistica descriptova para las variables edad y calificacion por periodo
#print(df["age"].describe(),df["G1"].describe(),df["G2"].describe(),df["G3"].describe())
df["promedio"]=df[["G1","G2","G3"]].mean(axis=1)
#vamos a comparar los dos colegios
comparacion=df.groupby("school")["promedio"].agg(promedio="mean",contar="count")
#del cual nos damos cuenta que gp  tiene mejor promedio apesar que tiene mas estudiantes
comparacion_conteo=df.groupby("school")["promedio"].count()
#print(comparacion_conteo)
def mayor_edad(x):
    if x > 17:
        return (1)
    else:
        return (0)
df["mayor"]=df["age"].apply(mayor_edad)
mayor_edad_colegio=df.groupby("school")["mayor"].sum()
#print(mayor_edad_colegio)
porcentaje_mayores=(mayor_edad_colegio/comparacion_conteo)*100
#print(porcentaje_mayores)
#de conclusion se podria decir que el MS tiene mayor numeros de mayores de edad pero tiene menor calificacion,toca mirar que motivos pueden ser
lugar=list(df["freetime"])
categorias = []
for i in lugar:
    if i < 3:
        categorias.append("desocupado")
    elif i < 4:
        categorias.append("semiocupado")
    else:
        categorias.append("ocupado")
#print(categorias)

df["categoria_freetime"] = categorias
colegio_promedio_freetime=df.groupby("school")["categoria_freetime"].agg(lambda x: x.mode())
#print(colegio_promedio_freetime)
#esto nos esplica porque piede ser que los estudiante de MS sacan menor nota
colegio_promedio_freetime2=df.groupby(["categoria_freetime", "school"])["school"].count()
#print(colegio_promedio_freetime2)
diccionario={"health":df["health"],
             "paid":df["paid"],
             "internet":df["internet"],
             "promedio":df["promedio"]
             }
estiduantes_condicion=[]
contador_condicion=0
for i in range(len(df)):
    if diccionario["health"].iloc[i] > 3 and diccionario["paid"].iloc[i] == "yes" and diccionario["internet"].iloc[i] == "yes":
       estiduantes_condicion.append(diccionario["promedio"].iloc[i])
       contador_condicion+=1
print(contador_condicion)
#solo 22 de todos los estudiantes tiene muy buenas condiciones que considere que es salud pagar horas extra internet
contador_pasar_materia = sum(1 for i in estiduantes_condicion if i >= 12)
print(contador_pasar_materia)
porcentaje_pasar_condiciones=contador_pasar_materia/contador_condicion*100
print(porcentaje_pasar_condiciones)
#esto nos muestra que con las mejores condiciones solo pasa el 54% de los estuciantes un porcentaje que considero bajito
personas_faltantes = 0

while porcentaje_pasar_condiciones < 70:
    contador_pasar_materia += 1
    personas_faltantes += 1
    porcentaje_pasar_condiciones = contador_pasar_materia / contador_condicion * 100

print(f"Faltan {personas_faltantes} personas por pasar para llegar al 70%")
print(f"Nuevo porcentaje: {porcentaje_pasar_condiciones:.2f}%")
     
#considero que para tener las buenas condiciones deberia tener como min un 70% de aprobados y para esto