import pandas  as pd 
import mathplot as mth
import matplotlib.pyplot as plt

plt.rcParams['figure.dpi'] = 140 # Mejora la nitidez del gráfico
plt.style.use('ggplot')          # Le da un estilo más profesional (parecido a R)

df= pd.read_csv("Dataset/video_games_sales.csv")

print (df.head())