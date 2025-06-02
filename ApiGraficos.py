import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

df = pd.read_csv('traffic_data_full.csv')

df['DateTime'] = pd.to_datetime(df['DateTime'])
df['Date'] = df['DateTime'].dt.strftime('%Y-%m-%d')

# Convertir las columnas 'Id' y 'Date' a tipo string y eliminar espacios en blanco
df['Id'] = df['Id'].astype(str).str.strip()

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

monday = ['2025-01-13', '2025-02-10', '2025-03-10', '2025-04-07']
tuesday = ['2025-01-14', '2025-02-11', '2025-03-11', '2025-04-08']
wednesday = ['2025-01-15', '2025-02-12', '2025-03-12', '2025-04-09']
thursday = ['2025-01-16', '2025-02-13', '2025-03-13', '2025-04-10']
friday = ['2025-01-17', '2025-02-14', '2025-03-14', '2025-04-11']
saturday = ['2025-01-18', '2025-02-15', '2025-03-15', '2025-04-12']
sunday = ['2025-01-19', '2025-02-16', '2025-03-16', '2025-04-13']

peak_ranges = [('06:00:00', '08:00:00'), ('15:00:00', '17:00:00')]


def modePoints(df, site_ids, dates, mode, value_col='TotalTraffic'):
    # Funcion para calcular la cantidad de trafico segun como estan posicionados los puntos
    """
    Returns (exit_count, stayed_count, before_exit_count) for the given mode.
    Modes:
        1: site_ids = [m6_toll_after_exit, before_exit]
           exit = before_exit - m6_toll_after_exit
           stayed = m6_toll_after_exit
           before_exit = before_exit
        2: site_ids = [exit, m6_toll_after_exit]
           exit = exit
           stayed = m6_toll_after_exit
           before_exit = exit + m6_toll_after_exit
        3: site_ids = [before_exit, exit]
           exit = exit
           stayed = before_exit - exit
           before_exit = before_exit
    """
    totals = df[(df['Id'].isin(site_ids)) & (df['Date'].isin(dates))].groupby('Id')[value_col].sum()
    if mode == 1:
        before_exit = totals.get(site_ids[1], 0)
        m6_toll = totals.get(site_ids[0], 0)
        exit_ = before_exit - m6_toll
        stayed = m6_toll
    elif mode == 2:
        exit_ = totals.get(site_ids[0], 0)
        m6_toll = totals.get(site_ids[1], 0)
        stayed = m6_toll
        before_exit = exit_ + m6_toll
    elif mode == 3:
        before_exit = totals.get(site_ids[0], 0)
        exit_ = totals.get(site_ids[1], 0)
        stayed = before_exit - exit_
    else:
        raise ValueError("Invalid mode")
    return max(exit_, 0), max(stayed, 0), max(before_exit, 0)

def plot_traffic_by_hour_mode(df, site_ids, date, mode, value_col='TotalTraffic', title=None):
    """
    Plots hourly traffic using modePoints to calculate exit, stayed, and before_exit counts.
    site_ids: list of site IDs as required by modePoints
    date: single date string (YYYY-MM-DD)
    mode: integer (1, 2, or 3) as per modePoints
    """
    # Prepare DataFrame for the selected date and sites
    df_day = df[(df['Id'].isin(site_ids)) & (df['Date'] == date)].copy()
    df_day['TimeInterval'] = pd.to_numeric(df_day['TimeInterval'], errors='coerce')
    
    # Aplicar la función lambda para convertir el TimeInterval a horas
    # Divide el TimeInterval entre 4 y convierte a entero para obtener la hora (cogiendo el valor del primer intervalo)
    # Formatea la hora como una cadena de 2 dígitos y añade ":00:00" al final
    df_day['Hour'] = df_day['TimeInterval'].apply(lambda x: f"{int(x)//4:02d}:00:00" if pd.notnull(x) else None)

    hours = sorted(df_day['Hour'].dropna().unique())
    exit_counts, stayed_counts, before_exit_counts = [], [], []

    # Asegurarse de que las horas están en el formato correcto
    # Usar función modePoints para cada hora
    for hour in hours:
        df_hour = df_day[df_day['Hour'] == hour]
        # Use modePoints for each hour
        exit_, stayed, before_exit = modePoints(df_hour, site_ids, [date], mode, value_col)
        exit_counts.append(exit_)
        stayed_counts.append(stayed)
        before_exit_counts.append(before_exit)

    # Crear grafico
    plt.figure(figsize=(12, 6))
    plt.plot(hours, exit_counts, marker='o', label='Exit')
    plt.plot(hours, stayed_counts, marker='o', label='Stayed')
    plt.plot(hours, before_exit_counts, marker='o', label='Before Exit')
    plt.xlabel('Hour')
    plt.ylabel('Traffic')
    plt.title(title or f'Traffic by Hour (mode {mode}) for {site_ids} on {date}')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    filename = f"traffic_mode_{mode}_{'_'.join(site_ids)}_{date}.png"
    plt.savefig(filename)
    plt.close()
       
def plot_exit_vs_stayed_pie(df, site_ids, date, mode, value_col='TotalTraffic', title=None, filename_prefix="exit_vs_stayed"):
    """
    Plots a pie chart for a single day showing the percentage and total of vehicles that took the exit vs stayed,
    using modePoints for the calculation.
    """
    
    # Usar funcion modePoints para calcular los valores
    exit_count, stayed_count, before_exit_count = modePoints(df, site_ids, [date], mode, value_col)
    total = exit_count + stayed_count

    # Crear el grafico de pastel
    values = [exit_count, stayed_count]
    labels = [
        f'Took Exit\n{exit_count:,}',
        f'Stayed\n{stayed_count:,}'
    ]
    colors = ['#FFC107', '#4CAF50']

    plt.figure(figsize=(6, 6))
    wedges, texts, autotexts = plt.pie(
        values, labels=labels, autopct='%1.1f%%', colors=colors,
        startangle=90, wedgeprops=dict(width=0.4)
    )
    plt.text(0, 0, f'Total:\n{int(total):,}', ha='center', va='center', fontsize=14, fontweight='bold')
    if not title:
        title = f'Exit vs Stayed\n{date}'
    plt.title(title)
    filename = f"{filename_prefix}_mode{mode}_{'_'.join(site_ids)}_{date}.png"
    plt.savefig(filename)
    plt.close()

def plot_weekly_exit_vs_stayed_pie(df, site_ids, week_dates, mode, value_col='TotalTraffic', title=None, filename_prefix="exit_vs_stayed_week"):
    """
    Plots a pie chart for a week showing the percentage and total of vehicles that took the exit vs stayed,
    using modePoints for the calculation.
    """
    exit_count, stayed_count, before_exit_count = modePoints(df, site_ids, week_dates, mode, value_col)
    total = exit_count + stayed_count

    values = [exit_count, stayed_count]
    labels = [
        f'Took Exit\n{exit_count:,}',
        f'Stayed\n{stayed_count:,}'
    ]
    colors = ['#FFC107', '#4CAF50']

    plt.figure(figsize=(6, 6))
    wedges, texts, autotexts = plt.pie(
        values, labels=labels, autopct='%1.1f%%', colors=colors,
        startangle=90, wedgeprops=dict(width=0.4)
    )
    plt.text(0, 0, f'Total:\n{int(total):,}', ha='center', va='center', fontsize=14, fontweight='bold')
    if not title:
        title = f'Exit vs Stayed\n{week_dates[0]} to {week_dates[-1]}'
    plt.title(title)
    filename = f"{filename_prefix}_mode{mode}_{'_'.join(site_ids)}_{week_dates[0]}_{week_dates[-1]}.png"
    plt.savefig(filename)
    plt.close()

def filter_peak_hours(df, peak_ranges):
    """Return a DataFrame filtered to only include rows within the given peak hour ranges (inclusive, like .between())."""
    # Variable para almacenar el filtro
    mask = False
    # Iterar sobre los rangos de horas pico y aplicar el filtro
    for start, end in peak_ranges:
        mask |= df['Hour'].between(start, end, inclusive='both')
    # Devolver el DataFrame filtrado
    return df[mask]

def plot_weekly_exit_vs_stayed_pie_peak(df, site_ids, week_dates, mode, peak_ranges, value_col='TotalTraffic', title=None, filename_prefix="exit_vs_stayed_week_peak"):
    """
    Plots a pie chart for a week showing the percentage and total of vehicles that took the exit vs stayed,
    using modePoints for the calculation, but only for peak hours.
    """
    df_week = df[df['Date'].isin(week_dates) & df['Id'].isin(site_ids)].copy()
    # Ensure 'Hour' column exists
    if 'Hour' not in df_week.columns:
        df_week['TimeInterval'] = pd.to_numeric(df_week['TimeInterval'], errors='coerce')
        df_week['Hour'] = df_week['TimeInterval'].apply(lambda x: f"{int(x)//4:02d}:00:00" if pd.notnull(x) else None)
    df_week = filter_peak_hours(df_week, peak_ranges)
    exit_count, stayed_count, before_exit_count = modePoints(df_week, site_ids, week_dates, mode, value_col)
    total = exit_count + stayed_count

    values = [exit_count, stayed_count]
    labels = [
        f'Took Exit\n{exit_count:,}',
        f'Stayed\n{stayed_count:,}'
    ]
    colors = ['#FFC107', '#4CAF50']

    plt.figure(figsize=(6, 6))
    wedges, texts, autotexts = plt.pie(
        values, labels=labels, autopct='%1.1f%%', colors=colors,
        startangle=90, wedgeprops=dict(width=0.4)
    )
    plt.text(0, 0, f'Total:\n{int(total):,}', ha='center', va='center', fontsize=14, fontweight='bold')
    if not title:
        title = f'Exit vs Stayed (Peak)\n{week_dates[0]} to {week_dates[-1]}'
    plt.title(title)
    filename = f"{filename_prefix}_mode{mode}_{'_'.join(site_ids)}_{week_dates[0]}_{week_dates[-1]}.png"
    plt.savefig(filename)
    plt.close()

def crearPercentilesStayed(df, site_ids, dates, mode):
    """
    Calculates percentiles for the number of vehicles that stayed in the M6 Toll after the exit,
    using the 'stayed' value from modePoints for each date.
    """
    stayed_counts = []
    for date in dates:
        _, stayed, _ = modePoints(df, site_ids, [date], mode)
        stayed_counts.append(stayed)
    p50 = pd.Series(stayed_counts).quantile(0.50)
    p75 = pd.Series(stayed_counts).quantile(0.75)
    p95 = pd.Series(stayed_counts).quantile(0.95)
    print(f"Percentiles for vehicles that STAYED in M6 Toll ({site_ids}) in selected period:\n"
          f"50th Percentile: {p50}\n"
          f"75th Percentile: {p75}\n"
          f"95th Percentile: {p95}")
    
def crearGraficos(df, site_ids, dates, mode):
    """
    Crea todos los graficos necesarios para analizar el trafico de las carreteras.
    site_ids: Lista de IDs de sitios a analizar
    dates: Lista de fechas a analizar (formato YYYY-MM-DD)
    mode: Como se deben interpretar los puntos de trafico
    """
    
    for date in dates:
        plot_traffic_by_hour_mode(df, site_ids, date, mode)
        plot_exit_vs_stayed_pie(df, site_ids, date, mode)
    
    plot_weekly_exit_vs_stayed_pie(df, site_ids, dates, mode)
    plot_weekly_exit_vs_stayed_pie_peak(df, site_ids, dates, mode, peak_ranges)

def plot_stayed_exit_by_hour_for_weekdays(df, site_ids, dates, mode, value_col='TotalTraffic', weekday_name='Monday'):
    """
    Plots a line graph with one line per date in `dates`, showing the hourly 'Stayed' and 'Exit' values.
    Each line is a different day (e.g., each Monday).
    """
    plt.figure(figsize=(14, 7))
    for date in dates:
        df_day = df[(df['Id'].isin(site_ids)) & (df['Date'] == date)].copy()
        df_day['TimeInterval'] = pd.to_numeric(df_day['TimeInterval'], errors='coerce')
        df_day['Hour'] = df_day['TimeInterval'].apply(lambda x: f"{int(x)//4:02d}:00:00" if pd.notnull(x) else None)
        hours = sorted(df_day['Hour'].dropna().unique())
        stayed_counts = []
        exit_counts = []
        for hour in hours:
            df_hour = df_day[df_day['Hour'] == hour]
            exit_, stayed, _ = modePoints(df_hour, site_ids, [date], mode, value_col)
            stayed_counts.append(stayed)
            exit_counts.append(exit_)
        plt.plot(hours, stayed_counts, marker='o', label=f'Stayed {date}')
        plt.plot(hours, exit_counts, marker='x', linestyle='--', label=f'Exit {date}')
    plt.xlabel('Hour')
    plt.ylabel('Vehicles')
    plt.title(f'Hourly Stayed and Exit Vehicles on {weekday_name}s')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'stayed_exit_by_hour_{weekday_name}.png')
    
def plot_stayed_exit_by_hour_for_weekdays_same_colors(df, site_ids, dates, mode, value_col='TotalTraffic', weekday_name='Monday'):
    """
    For each date in `dates`, plots 'Stayed' (solid) and 'Exit' (dashed) lines in the same unique color.
    """
    plt.figure(figsize=(14, 7))
    colors = cm.get_cmap('tab10', len(dates))
    for idx, date in enumerate(dates):
        df_day = df[(df['Id'].isin(site_ids)) & (df['Date'] == date)].copy()
        df_day['TimeInterval'] = pd.to_numeric(df_day['TimeInterval'], errors='coerce')
        df_day['Hour'] = df_day['TimeInterval'].apply(lambda x: f"{int(x)//4:02d}:00:00" if pd.notnull(x) else None)
        hours = sorted(df_day['Hour'].dropna().unique())
        stayed_counts = []
        exit_counts = []
        for hour in hours:
            df_hour = df_day[df_day['Hour'] == hour]
            exit_, stayed, _ = modePoints(df_hour, site_ids, [date], mode, value_col)
            stayed_counts.append(stayed)
            exit_counts.append(exit_)
        color = colors(idx)
        plt.plot(hours, stayed_counts, marker='o', color=color, linestyle='-', label=f'Stayed {date}')
        plt.plot(hours, exit_counts, marker='x', color=color, linestyle='--', label=f'Exit {date}')
    plt.xlabel('Hour')
    plt.ylabel('Vehicles')
    plt.title(f'Hourly Stayed and Exit Vehicles on {weekday_name}s')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'stayed_exit_by_hour_{weekday_name}.png')
    plt.show() 

def plot_avg_captation_and_stayed_per_hour(df, site_ids, dates, mode, value_col='TotalTraffic', weekday_name='Monday'):
    import numpy as np
    import matplotlib.pyplot as plt

    # Get all hours present in the data
    all_hours = set()
    for date in dates:
        df_day = df[(df['Id'].isin(site_ids)) & (df['Date'] == date)].copy()
        df_day['TimeInterval'] = pd.to_numeric(df_day['TimeInterval'], errors='coerce')
        df_day['Hour'] = df_day['TimeInterval'].apply(lambda x: f"{int(x)//4:02d}:00:00" if pd.notnull(x) else None)
        all_hours.update(df_day['Hour'].dropna().unique())
    hour_labels = sorted([h.strip() for h in all_hours])

    percentages_by_hour = {hour: [] for hour in hour_labels}
    stayed_counts_by_hour = {hour: [] for hour in hour_labels}

    for date in dates:
        df_day = df[(df['Id'].isin(site_ids)) & (df['Date'] == date)].copy()
        df_day['TimeInterval'] = pd.to_numeric(df_day['TimeInterval'], errors='coerce')
        df_day['Hour'] = df_day['TimeInterval'].apply(lambda x: f"{int(x)//4:02d}:00:00" if pd.notnull(x) else None)
        for hour in hour_labels:
            df_hour = df_day[df_day['Hour'] == hour]
            if not df_hour.empty:
                exit_, stayed, _ = modePoints(df_hour, site_ids, [date], mode, value_col)
                total = stayed + exit_
                if total > 0:
                    percent = stayed / total * 100
                    percentages_by_hour[hour].append(percent)
                stayed_counts_by_hour[hour].append(stayed)

    avg_percentages = [np.mean(percentages_by_hour[hour]) if percentages_by_hour[hour] else 0 for hour in hour_labels]
    avg_stayed_counts = [np.mean(stayed_counts_by_hour[hour]) if stayed_counts_by_hour[hour] else 0 for hour in hour_labels]

    fig, ax1 = plt.subplots(figsize=(14, 6))

    bars = ax1.bar(range(len(hour_labels)), avg_percentages, color='skyblue', label='Avg % Stayed')
    ax1.set_xlabel('Hour')
    ax1.set_ylabel('Average % Stayed on M6 Toll', color='skyblue')
    ax1.tick_params(axis='y', labelcolor='skyblue')
    ax1.set_ylim(0, 100)

    ax2 = ax1.twinx()
    ax2.plot(range(len(hour_labels)), avg_stayed_counts, color='orange', marker='o', label='Avg # Stayed')
    ax2.set_ylabel('Average # Vehicles Stayed', color='orange')
    ax2.tick_params(axis='y', labelcolor='orange')

    ax1.set_xticks(range(len(hour_labels)))
    ax1.set_xticklabels(hour_labels, rotation=45)

    plt.title(f'Average Hourly Captation (% Stayed) and Stayed Count on M6 Toll - {weekday_name}s')
    fig.tight_layout()
    plt.savefig(f'avg_captation_and_stayed_per_hour_{weekday_name}.png')
    plt.show()

plot_stayed_exit_by_hour_for_weekdays_same_colors(df, ['10464', '10654'], monday, mode=1, weekday_name='Monday')
plot_stayed_exit_by_hour_for_weekdays_same_colors(df, ['10464', '10654'], tuesday, mode=1, weekday_name='Tuesday')
plot_stayed_exit_by_hour_for_weekdays_same_colors(df, ['10464', '10654'], wednesday, mode=1, weekday_name='Wednesday')
plot_stayed_exit_by_hour_for_weekdays_same_colors(df, ['10464', '10654'], thursday, mode=1, weekday_name='Thursday')
plot_stayed_exit_by_hour_for_weekdays_same_colors(df, ['10464', '10654'], friday, mode=1, weekday_name='Friday')
plot_stayed_exit_by_hour_for_weekdays_same_colors(df, ['10464', '10654'], saturday, mode=1, weekday_name='Saturday')
plot_stayed_exit_by_hour_for_weekdays_same_colors(df, ['10464', '10654'], sunday, mode=1, weekday_name='Sunday')

#crearGraficos(df, ['9238', '9239'], abril, mode=2)
#crearPercentilesStayed(df, ['10464', '10654'], abril, mode=1)
#plot_avg_captation_and_stayed_per_hour(df, ['10464', '10654'], monday, mode=1, weekday_name='Monday')

# TODO Graficos lineares comparando todas las semanas por días (Lunes, Martes, etc.) mostrando las tendencias e un mismo grafico 
# TODO Dentro de esos graficos mirar si se puedehacer un prmedio, y sacar la mediana (P50) para incluirla 
# TODO Porcentaje de captacion de vehiculo que se quedan en la toll, gráfico de barras
# TODO Mirar si podemos incluir las barras y las lineares en el mismo grafico 
