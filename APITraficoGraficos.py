import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('traffic_data_full.csv')

df['DateTime'] = pd.to_datetime(df['DateTime'])
df['Date'] = df['DateTime'].dt.strftime('%Y-%m-%d')

# Convertir las columnas 'Id' y 'Date' a tipo string y eliminar espacios en blanco
df['Id'] = df['Id'].astype(str).str.strip()

# Funcion para crear los graficos de los puntos que queramos (Usarla para puntos que sean antes de la exit, y en la carretera que queremos que cojan)
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

# Función para crear el gráfico porcentual de Toll vs Exit After Split
def plot_toll_exit_after_percentage(df, site_ids, dates, title=None, filename_prefix="toll_exit_after_percentage"):
    # Función para crear un gráfico de pastel semanal o diario mostrando el porcentaje de vehículos que tomaron el peaje vs la salida,
    # usando los totales de tráfico de dos puntos después de la bifurcación.
    # site_ids: [id_peaje, id_salida]
    # dates: lista de fechas a analizar
    
    # Filtrar el DataFrame por los Ids y las fechas seleccionadas
    df_period = df[(df['Id'].isin(site_ids)) & (df['Date'].isin(dates))]
    # Agrupar por Id y sumar el tráfico total
    totals = df_period.groupby('Id')['TotalTraffic'].sum()
    toll = int(totals.get(site_ids[0], 0))
    exit_ = int(totals.get(site_ids[1], 0))
    total_cars = toll + exit_

    # Preparar datos para el gráfico
    values = [toll, exit_]
    labels = [
        f'Toll ({site_ids[0]})\n{toll:,}',
        f'Exit ({site_ids[1]})\n{exit_:,}'
    ]
    colors = ['#2196F3', '#FF5722']

    # Crear el gráfico de pastel
    plt.figure(figsize=(6, 6))
    wedges, texts, autotexts = plt.pie(
        values, labels=labels, autopct='%1.1f%%', colors=colors,
        startangle=90, wedgeprops=dict(width=0.4)
    )
    
    # Mostrar el total en el centro del gráfico
    plt.text(0, 0, f'Total:\n{int(total_cars):,}', ha='center', va='center', fontsize=14, fontweight='bold')
    # Título automático si no se proporciona
    if not title:
        if len(dates) == 1:
            title = f'Percentage: Toll vs Exit After Split\n{dates[0]}'
        else:
            title = f'Percentage: Toll vs Exit After Split\n{dates[0]} to {dates[-1]}'
    plt.title(title)
    # Guardar el gráfico
    filename = f"{filename_prefix}_{'_'.join(site_ids)}_{dates[0]}_{dates[-1] if len(dates)>1 else dates[0]}.png"
    plt.savefig(filename)
    plt.close()

def plot_weekly_exit_percentage_by_size(df, site_ids, week_dates, size_col, title=None, filename_prefix="exit_percentage_by_size"):
    # Función para crear un gráfico de pastel semanal mostrando el porcentaje de vehículos que tomaron la salida vs los que no,
    # segmentado por tamaño de vehículo (columna size_col).
    # site_ids: [id_peaje, id_total]
    # week_dates: lista de fechas de la semana
    # size_col: columna de tamaño de vehículo a analizar
    
    # Filtrar el DataFrame por los Ids y las fechas seleccionadas
    df_week = df[(df['Id'].isin(site_ids)) & (df['Date'].isin(week_dates))]
    # Agrupar por Id y sumar la columna de tamaño seleccionada
    totals = df_week.groupby('Id')[size_col].sum()
    # Calcular los que tomaron la salida y los que no
    took_toll = totals.get(site_ids[0], 0)
    total = totals.get(site_ids[1], 0)
    took_exit = total - took_toll if total > took_toll else 0

    # Preparar datos para el gráfico
    values = [took_exit, took_toll]
    labels = [
        f'Took Exit\n{took_exit:,}',
        f'Did Not Take Exit\n{took_toll:,}'
    ]
    colors = ['#FF5722', '#2196F3']

    # Crear el gráfico de pastel
    plt.figure(figsize=(6, 6))
    wedges, texts, autotexts = plt.pie(
        values, labels=labels, autopct='%1.1f%%', colors=colors,
        startangle=90, wedgeprops=dict(width=0.4)
    )
    # Mostrar el total en el centro del gráfico
    plt.text(0, 0, f'Total:\n{int(total):,}', ha='center', va='center', fontsize=14, fontweight='bold')
    # Título automático si no se proporciona
    if not title:
        title = f'Exit vs No Exit ({size_col})\n{week_dates[0]} to {week_dates[-1]}'
    plt.title(title)
    filename = f"{filename_prefix}_{size_col.replace(' ', '_')}_{'_'.join(site_ids)}_{week_dates[0]}_{week_dates[-1]}.png"
    plt.savefig(filename)
    plt.close()

# Función para crear el gráfico porcentual de M6 Toll vs Exit
def plot_toll_percentage(df, site_ids, dates, title=None, filename_prefix="toll_percentage"):
    # Filter for the given dates and sites
    df_period = df[(df['Id'].isin(site_ids)) & (df['Date'].isin(dates))]
    totals = df_period.groupby('Id')['TotalTraffic'].sum()
    m6_toll = totals.get(site_ids[0], 0)
    total = totals.get(site_ids[1], 0)
    exit_count = total - m6_toll if total > m6_toll else 0
    total_cars = m6_toll + exit_count

    values = [m6_toll, exit_count]
    labels = [
        f'M6 Toll ({site_ids[0]})\n{m6_toll:,}',
        f'Exit ({site_ids[1]})\n{exit_count:,}'
    ]
    colors = ['#4CAF50', '#FFC107']

    plt.figure(figsize=(6, 6))
    wedges, texts, autotexts = plt.pie(
        values, labels=labels, autopct='%1.1f%%', colors=colors,
        startangle=90, wedgeprops=dict(width=0.4)
    )
    # Add total in the center
    plt.text(0, 0, f'Total:\n{int(total_cars):,}', ha='center', va='center', fontsize=14, fontweight='bold')
    # Title
    if not title:
        if len(dates) == 1:
            title = f'Percentage of Vehicles: M6 Toll vs Exit\n{dates[0]}'
        else:
            title = f'Percentage of Vehicles: M6 Toll vs Exit\n{dates[0]} to {dates[-1]}'
    plt.title(title)
    # Save
    filename = f"{filename_prefix}_{'_'.join(site_ids)}_{dates[0]}_{dates[-1] if len(dates)>1 else dates[0]}.png"
    plt.savefig(filename)
    plt.close()

# Función para crear todos los gráficos de una semana    
def crear_todos_los_graficos(df, site_ids, week_dates, peak_ranges, prefix=""):
    # 1. Daily line and percentage graphs
    for date in week_dates:
        # Line graph
        plot_traffic_by_hour(df, site_ids, date, f'Traffic Volume by Hour for Sites {site_ids} on {date}')
        # Daily percentage pie
        plot_toll_exit_after_percentage(df, site_ids, [date], f'Percentage: Toll vs Exit After Split\n{date}', filename_prefix=f"{prefix}toll_exit_after_percentage")
    
    # 2. Gráfico semanal de porcentaje de peaje vs salida
    plot_toll_exit_after_percentage(df, site_ids, week_dates, f'Percentage: Toll vs Exit After Split\n{week_dates[0]} to {week_dates[-1]}', filename_prefix=f"{prefix}toll_exit_after_percentage_week")
    
    # 3. Gráficos de porcentaje de salida horas pico
    plot_toll_percentage_peak(df, site_ids, week_dates, peak_ranges, f'Peak Hour %: Toll vs Exit After Split\n{week_dates[0]} to {week_dates[-1]}', filename_prefix=f"{prefix}toll_exit_after_percentage_peak")

def plot_toll_percentage_peak(df, site_ids, dates, peak_ranges, title=None, filename_prefix="toll_percentage_peak"):
    # Filter for the given dates and sites
    df_period = df[(df['Id'].isin(site_ids)) & (df['Date'].isin(dates))]
    # Filter for peak hours
    df_peak = df_period[df_period['Hour'].between(peak_ranges[0][0], peak_ranges[0][1]) | df_period['Hour'].between(peak_ranges[1][0], peak_ranges[1][1])]
    totals = df_peak.groupby('Id')['TotalTraffic'].sum()
    m6_toll = int(totals.get(site_ids[0], 0))
    total = int(totals.get(site_ids[1], 0))
    exit_count = total - m6_toll if total > m6_toll else 0

    values = [m6_toll, exit_count]
    labels = [
        f'M6 Toll ({site_ids[0]})\n{m6_toll:,}',
        f'Exit ({site_ids[1]})\n{exit_count:,}'
    ]
    colors = ['#4CAF50', '#FFC107']

    plt.figure(figsize=(6, 6))
    wedges, texts, autotexts = plt.pie(
        values, labels=labels, autopct='%1.1f%%', colors=colors,
        startangle=90, wedgeprops=dict(width=0.4)
    )
    plt.text(0, 0, f'Total:\n{int(total):,}', ha='center', va='center', fontsize=14, fontweight='bold')
    if not title:
        if len(dates) == 1:
            title = f'Peak Hour %: M6 Toll vs Exit\n{dates[0]}'
        else:
            title = f'Peak Hour %: M6 Toll vs Exit\n{dates[0]} to {dates[-1]}'
    plt.title(title)
    filename = f"{filename_prefix}_{'_'.join(site_ids)}_{dates[0]}_{dates[-1] if len(dates)>1 else dates[0]}.png"
    plt.savefig(filename)
    plt.close()

def crear_grafico(site_ids, Date):
    plot_traffic_by_hour(df, site_ids, Date, f'Traffic Volume by Hour for Site s {site_ids} on {Date}')
    
def filter_peak_hours(df, peak_ranges):
    # peak_ranges: list of tuples, e.g. [('06:00:00', '08:00:00'), ('15:00:00', '17:00:00')]
    return df[df['Hour'].between(peak_ranges[0][0], peak_ranges[0][1]) | df['Hour'].between(peak_ranges[1][0], peak_ranges[1][1])]

# Uso de la función para crear gráficos con los puntos que queramos 
#plot_traffic_by_hour(df, ['9236', '9237'], '2025-03-01', 'Traffic Volume by Hour for Sites 9236 and 9237 on 2025-03-01')
#plot_traffic_by_hour(df, ['10308', '10559'], '2025-03-01', 'Traffic Volume by Hour for Sites 10308 and 10559 on 2025-03-01')


df['TimeInterval'] = pd.to_numeric(df['TimeInterval'], errors='coerce')
df['TotalTraffic'] = pd.to_numeric(df['TotalTraffic'], errors='coerce')
df['Hour'] = df['TimeInterval'].apply(lambda x: f"{int(x)//4:02d}:00:00" if pd.notnull(x) else None)
# Define peak hour ranges as tuples (start, end)
peak_ranges = [('06:00:00', '08:00:00'), ('15:00:00', '17:00:00')]

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

df_week_site = df[(df['Id'] == '10464') | (df['Id'] == '10654') & (df['Date'].isin(abril))]
p50 = df_week_site['TotalTraffic'].quantile(0.50)
p75 = df_week_site['TotalTraffic'].quantile(0.75)
p95 = df_week_site['TotalTraffic'].quantile(0.95)
print(f"Percentiles for TotalTraffic on M6 Toll (Id 10464 and 10654) in January 2025:\n"
      f"50th Percentile: {p50}\n"
      f"75th Percentile: {p75}\n"
      f"95th Percentile: {p95}")

"""
crear_grafico(['9236', '9237'], '2025-03-01')
crear_grafico(['10308', '10559'], '2025-03-01')
crear_grafico(['10464', '10654'], '2025-03-01')
crear_grafico(['9238', '9239'], '2025-03-01')

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

plot_toll_percentage(df, ['10464', '10654'], enero, 'M6 Toll vs Exit (Enero 13-19, 2025)')
plot_toll_percentage(df, ['10464', '10654'], febrero, 'M6 Toll vs Exit (Febrero 10-16, 2025)')
plot_toll_percentage(df, ['10464', '10654'], marzo, 'M6 Toll vs Exit (Marzo 10-16, 2025)')
plot_toll_percentage(df, ['10464', '10654'], abril, 'M6 Toll vs Exit (Abril 7-13, 2025)')

# For a week
plot_toll_percentage_peak(df, ['10464', '10654'], enero, peak_ranges, 'M6 Toll vs Exit (Enero 13-19, 2025) Peak Hours')
plot_toll_percentage_peak(df, ['10464', '10654'], febrero, peak_ranges, 'M6 Toll vs Exit (Febrero 10-16, 2025) Peak Hours')
plot_toll_percentage_peak(df, ['10464', '10654'], marzo, peak_ranges, 'M6 Toll vs Exit (Marzo 10-16, 2025) Peak Hours')
plot_toll_percentage_peak(df, ['10464', '10654'], abril, peak_ranges, 'M6 Toll vs Exit (Abril 7-13, 2025) Peak Hours')

plot_weekly_exit_percentage_by_size(df, ['10464', '10654'], abril, 'Cars 0 - 520 cm')
plot_weekly_exit_percentage_by_size(df, ['10464', '10654'], abril, 'Cars 521 - 660 cm')
plot_weekly_exit_percentage_by_size(df, ['10464', '10654'], abril, 'Cars 661 - 1160 cm')
plot_weekly_exit_percentage_by_size(df, ['10464', '10654'], abril, 'Cars 1160+ cm')

#crear_todos_los_graficos(df, ['9235', '9234'], abril, peak_ranges, prefix="m6toll_")
"""
