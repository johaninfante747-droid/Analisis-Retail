import pandas as pd
print("Cargando datos")
df = pd.read_csv("Dataset/16. Retail-Dataset_real.csv")
print("Cantidad de filas originales:", len(df))
df = df.dropna()
print("Cantidad de filas sin los nulos:", len(df))

print("Revisando el formato de las fechas")
df["Date"] = pd.to_datetime(df["Date"])
print("Fechas correctas")

print("Buscando transacciones duplicadas")
df = df.drop_duplicates()
print("Cantidad de filas despues de borrar duplicados:" , len(df))
