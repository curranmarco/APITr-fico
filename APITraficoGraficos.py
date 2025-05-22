import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('traffic_data_full.csv')

# Convertir las columnas 'Id' y 'Date' a tipo string y eliminar espacios en blanco
df['Id'] = df['Id'].astype(str).str.strip()
df['Date'] = df['Date'].astype(str).str.strip()


"""
# Crear el segundo dataframe filtrando por Id y fecha
columnasInteres = ['Date', 'Id','TimeInterval','TotalTraffic']
df2 = df[(df['Id'].isin(['9236','9237'])) & (df['Date'] == '2025-03-01')][columnasInteres]

# Para que Panda no de error al hacer el groupby y lo confunda con un view (que nos deje editar el df2)
df2 = df2.copy()

# Aplicar la función lambda para convertir el TimeInterval a horas
# Divide el TimeInterval entre 4 y convierte a entero para obtener la hora (cogiendo el valor del primer intervalo)
# Formatea la hora como una cadena de 2 dígitos y añade ":00:00" al final
df2['Hour'] = df2['TimeInterval'].apply(lambda x: f"{int(x)//4:02d}:00:00")

# Crear el tercer dataframe agrupandolo por fecha, Id y hora
# Sumamos el TotalTraffic para cada cuatro intervalos de 15 minutos
df3 = df2.groupby(['Date', 'Id', 'Hour'], as_index=False)['TotalTraffic'].sum()

#print(df3)
pivot_df = df3.pivot(index='Hour', columns=['Id'], values='TotalTraffic')

#Crear el gráfico
plt.figure(figsize=(12, 6))
for site_id in pivot_df.columns:
    plt.plot(pivot_df.index, pivot_df[site_id], marker = 'o', label=f'Site {site_id}') 

plt.xlabel('Hour')
plt.ylabel('Total Traffic')
plt.title('Volumen de tráfico por hora 1/3/2025')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
"""

# Funcion para crear los graficos de los puntos que queramos 
def plot_traffic_by_hour(df, site_ids, date, title=None):
    # Filtrar el dataframe por los Ids y la fecha deseada
    columnasInteres = ['Date', 'Id', 'TimeInterval', 'TotalTraffic']
    df2 = df[(df['Id'].isin(site_ids)) & (df['Date'] == date)][columnasInteres].copy()
    
    # Aplicar la función lambda para convertir el TimeInterval a horas
    # Divide el TimeInterval entre 4 y convierte a entero para obtener la hora (cogiendo el valor del primer intervalo)
    # Formatea la hora como una cadena de 2 dígitos y añade ":00:00" al final
    df2['Hour'] = df2['TimeInterval'].apply(lambda x: f"{int(x)//4:02d}:00:00")
    
    # Crear el tercer dataframe agrupandolo por fecha, Id y hora
    # Sumamos el TotalTraffic para cada cuatro intervalos de 15 minutos
    df3 = df2.groupby(['Date', 'Id', 'Hour'], as_index=False)['TotalTraffic'].sum()
    
    # Pivotar el dataframe para que las horas sean el índice y los Ids sean las columnas
    pivot_df = df3.pivot(index='Hour', columns='Id', values='TotalTraffic')

    # Crear el gráfico
    plt.figure(figsize=(12, 6))
    for site_id in pivot_df.columns:
        plt.plot(pivot_df.index, pivot_df[site_id], marker='o', label=f'Site {site_id}')
    plt.xlabel('Hour')
    plt.ylabel('Total Traffic')
    plt.title(title or f'Traffic per Hour for {site_ids} on {date}')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def crear_grafico(site_ids):
    plot_traffic_by_hour(df, site_ids, '2025-03-01', f'Traffic Volume by Hour for Site s {site_ids} on 2025-03-01')

# Uso de la función para crear gráficos con los puntos que queramos 
#plot_traffic_by_hour(df, ['9236', '9237'], '2025-03-01', 'Traffic Volume by Hour for Sites 9236 and 9237 on 2025-03-01')
#plot_traffic_by_hour(df, ['10308', '10559'], '2025-03-01', 'Traffic Volume by Hour for Sites 10308 and 10559 on 2025-03-01')

crear_grafico(['9236', '9237'])
crear_grafico(['10308', '10559'])