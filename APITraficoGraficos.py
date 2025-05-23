import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('traffic_data_full.csv')

# Convertir las columnas 'Id' y 'Date' a tipo string y eliminar espacios en blanco
df['Id'] = df['Id'].astype(str).str.strip()
df['Date'] = df['Date'].astype(str).str.strip()

# Funcion para crear los graficos de los puntos que queramos 
def plot_traffic_by_hour(df, site_ids, date, title=None):
    # Filtrar el dataframe por los Ids y la fecha deseada
    columnasInteres = ['Date', 'Id', 'TimeInterval', 'TotalTraffic']
    df2 = df[(df['Id'].isin(site_ids)) & (df['Date'] == date)][columnasInteres].copy()
    
    df2['TimeInterval'] = pd.to_numeric(df2['TimeInterval'], errors='coerce')
    df2['TotalTraffic'] = pd.to_numeric(df2['TotalTraffic'], errors='coerce')
    
    # Aplicar la función lambda para convertir el TimeInterval a horas
    # Divide el TimeInterval entre 4 y convierte a entero para obtener la hora (cogiendo el valor del primer intervalo)
    # Formatea la hora como una cadena de 2 dígitos y añade ":00:00" al final
    df2['Hour'] = df2['TimeInterval'].apply(lambda x: f"{int(x)//4:02d}:00:00")
    
    # Crear el tercer dataframe agrupandolo por fecha, Id y hora
    # Sumamos el TotalTraffic para cada cuatro intervalos de 15 minutos
    df3 = df2.groupby(['Date', 'Id', 'Hour'], as_index=False)['TotalTraffic'].sum()
    
    # Pivotar el dataframe para que las horas sean el índice y los Ids sean las columnas
    pivot_df = df3.pivot(index='Hour', columns='Id', values='TotalTraffic')
    
    # Rellenar NaN con 0 para evitar errores en el gráfico
    pivot_df = pivot_df.fillna(0)  
    
    for site_id in site_ids:
        if site_id not in pivot_df.columns:
            pivot_df[site_id] = 0
    pivot_df = pivot_df[site_ids]

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
    
    filename = f"traffic_plot_{'_'.join(site_ids)}_{date[0]}_{date[-1]}.png"
    plt.savefig(filename)
    #plt.show()
    
# Función para crear el gráfico porcentual de M6 Toll vs Exit
def plot_weekly_toll_percentage(df, site_ids, week_dates, title=None):
    # site_ids[0] = 10464 (M6 Toll), site_ids[1] = 10654 (Total)
    # Filtrar el dataframe por los Ids y las fechas de la semana deseada
    df_week = df[(df['Id'].isin(site_ids)) & (df['Date'].isin(week_dates))]
    # Agrupar por Id y sumar el TotalTraffic
    totals = df_week.groupby('Id')['TotalTraffic'].sum()
    # Obtener los totales para M6 Toll y el total
    m6_toll = totals.get(site_ids[0], 0)
    total = totals.get(site_ids[1], 0)
    # Calcular el porcentaje de M6 Toll y el número de vehículos que han salido
    exit_count = total - m6_toll if total > m6_toll else 0

    # Crear el gráfico de pastel
    values = [m6_toll, exit_count]
    labels = [f'M6 Toll ({site_ids[0]})', f'Exit ({site_ids[1]})']
    colors = ['#4CAF50', '#FFC107']

    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90, wedgeprops=dict(width=0.4))
    plt.title(title or 'Percentage of Vehicles: M6 Toll vs Exit')
    
    filename = f"weekly_toll_percentage_{'_'.join(site_ids)}_{week_dates[0]}_{week_dates[-1]}.png"
    plt.savefig(filename)
    #plt.show()

def crear_grafico(site_ids, Date):
    plot_traffic_by_hour(df, site_ids, Date, f'Traffic Volume by Hour for Site s {site_ids} on {Date}')

# Uso de la función para crear gráficos con los puntos que queramos 
#plot_traffic_by_hour(df, ['9236', '9237'], '2025-03-01', 'Traffic Volume by Hour for Sites 9236 and 9237 on 2025-03-01')
#plot_traffic_by_hour(df, ['10308', '10559'], '2025-03-01', 'Traffic Volume by Hour for Sites 10308 and 10559 on 2025-03-01')


df['TimeInterval'] = pd.to_numeric(df['TimeInterval'], errors='coerce')
df['TotalTraffic'] = pd.to_numeric(df['TotalTraffic'], errors='coerce')

"""
crear_grafico(['9236', '9237'], '2025-03-01')
crear_grafico(['10308', '10559'], '2025-03-01')
crear_grafico(['10464', '10654'], '2025-03-01')
crear_grafico(['9238', '9239'], '2025-03-01')
"""

#! Seleccionar una semana entera en la que podamos recoger datos en la location 
#! En principio vamos a usar la location direccion southbound de M6 - m6Toll -> la tercera llamada
#! Crear un grafico para cada dia de la semana, para ver el flujo de tráfico de esa location durante esa semana 
#! Una vez tengamos esa semana , mirar otras semanas para poder comparar y ver patrones 
#! En principio para ese site, deberiamos tener alrededor de 7 graficos por semana 

"""
# Gráficos de puntos southbound de M6 - m6Toll en Enero 2025
crear_grafico(['10464', '10654'], '2025-01-13')
crear_grafico(['10464', '10654'], '2025-01-14')
crear_grafico(['10464', '10654'], '2025-01-15')
crear_grafico(['10464', '10654'], '2025-01-16')
crear_grafico(['10464', '10654'], '2025-01-17')
crear_grafico(['10464', '10654'], '2025-01-18')
crear_grafico(['10464', '10654'], '2025-01-19')


# Gráficos de puntos southbound de M6 - m6Toll en Febrero 2025
crear_grafico(['10464', '10654'], '2025-02-10')
crear_grafico(['10464', '10654'], '2025-02-11')
crear_grafico(['10464', '10654'], '2025-02-12')
crear_grafico(['10464', '10654'], '2025-02-13')
crear_grafico(['10464', '10654'], '2025-02-14')
crear_grafico(['10464', '10654'], '2025-02-15')
crear_grafico(['10464', '10654'], '2025-02-16')

# Gráficos de puntos southbound de M6 - m6Toll en Marzo 2025
crear_grafico(['10464', '10654'], '2025-03-10')
crear_grafico(['10464', '10654'], '2025-03-11')
crear_grafico(['10464', '10654'], '2025-03-12')
crear_grafico(['10464', '10654'], '2025-03-13')
crear_grafico(['10464', '10654'], '2025-03-14')
crear_grafico(['10464', '10654'], '2025-03-15')
crear_grafico(['10464', '10654'], '2025-03-16')

# Gráficos de puntos southbound de M6 - m6Toll en Abril 2025
crear_grafico(['10464', '10654'], '2025-04-07')
crear_grafico(['10464', '10654'], '2025-04-08')
crear_grafico(['10464', '10654'], '2025-04-09')
crear_grafico(['10464', '10654'], '2025-04-10')
crear_grafico(['10464', '10654'], '2025-04-11')
crear_grafico(['10464', '10654'], '2025-04-12')
crear_grafico(['10464', '10654'], '2025-04-13')
"""

"""
enero = [
    '2025-01-13', '2025-01-14', '2025-01-15', '2025-01-16',
    '2025-01-17', '2025-01-18', '2025-01-19'
]
febrero = [
    '2025-02-10', '2025-02-11', '2025-02-12', '2025-02-13',
    '2025-02-14', '2025-02-15', '2025-02-16'
]
marzo = [
    '2025-03-10', '2025-03-11', '2025-03-12', '2025-03-13',
    '2025-03-14', '2025-03-15', '2025-03-16'
]
abril = [
    '2025-04-07', '2025-04-08', '2025-04-09', '2025-04-10',
    '2025-04-11', '2025-04-12', '2025-04-13'
]
plot_weekly_toll_percentage(df, ['10464', '10654'], enero, 'M6 Toll vs Exit (Enero 13-19, 2025)')
plot_weekly_toll_percentage(df, ['10464', '10654'], febrero, 'M6 Toll vs Exit (Febrero 10-16, 2025)')
plot_weekly_toll_percentage(df, ['10464', '10654'], marzo, 'M6 Toll vs Exit (Marzo 10-16, 2025)')
plot_weekly_toll_percentage(df, ['10464', '10654'], abril, 'M6 Toll vs Exit (Abril 7-13, 2025)')
"""