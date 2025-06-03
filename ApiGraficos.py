import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import streamlit as st


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

vehicle_size_columns = [
    'Cars 0 - 520 cm',
    #'Cars 521 - 660 cm',
    #'Cars 661 - 1160 cm',
    #'Cars 1160+ cm'
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

    fig, ax = plt.subplots(figsize=(6, 6))
    wedges, texts, autotexts = ax.pie(
        values, labels=labels, autopct='%1.1f%%', colors=colors,
        startangle=90, wedgeprops=dict(width=0.4)
    )
    ax.text(0, 0, f'Total:\n{int(total):,}', ha='center', va='center', fontsize=14, fontweight='bold')
    if not title:
        title = f'Exit vs Stayed\n{week_dates[0]} to {week_dates[-1]}'
    ax.set_title(title)
    plt.tight_layout()
    return fig
    
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

    fig, ax = plt.subplots(figsize=(6, 6))
    wedges, texts, autotexts = ax.pie(
        values, labels=labels, autopct='%1.1f%%', colors=colors,
        startangle=90, wedgeprops=dict(width=0.4)
    )
    ax.text(0, 0, f'Total:\n{int(total):,}', ha='center', va='center', fontsize=14, fontweight='bold')
    if not title:
        title = f'Exit vs Stayed (Peak)\n{week_dates[0]} to {week_dates[-1]}'
    ax.set_title(title)
    plt.tight_layout()
    return fig

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
    Returns the matplotlib figure.
    """
    fig, ax = plt.subplots(figsize=(14, 7))
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
        ax.plot(hours, stayed_counts, marker='o', color=color, linestyle='-', label=f'Stayed {date}')
        ax.plot(hours, exit_counts, marker='x', color=color, linestyle='--', label=f'Exit {date}')
    ax.set_xlabel('Hour')
    ax.set_ylabel('Vehicles')
    ax.set_title(f'Hourly Stayed and Exit Vehicles on {weekday_name}s')
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig
    #plt.savefig(f'stayed_exit_by_hour_{weekday_name}.png')

def plot_avg_captation_and_stayed_per_hour(df, site_ids, dates, mode, value_col='TotalTraffic', weekday_name='Monday'):

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
    return fig
    #plt.savefig(f'avg_captation_and_stayed_per_hour_{weekday_name}.png')


#plot_stayed_exit_by_hour_for_weekdays_same_colors(df, ['9242', '9241'], monday, mode=2, weekday_name='Monday')
#plot_avg_captation_and_stayed_per_hour(df, ['9242', '9241'], monday, mode=2, weekday_name='Monday')

# ...existing imports and code...

if __name__ == "__main__":
    st.title("Traffic Dashboard")

    dashboard_mode = st.radio(
        "Choose dashboard mode",
        ("By Weekday", "By Week/Month")
    )

    if dashboard_mode == "By Weekday":
        # --- Existing weekday dashboard ---
        weekday_map = {
            'Monday': monday,
            'Tuesday': tuesday,
            'Wednesday': wednesday,
            'Thursday': thursday,
            'Friday': friday,
            'Saturday': saturday,
            'Sunday': sunday
        }
        weekday = st.selectbox("Select a weekday", list(weekday_map.keys()))
        dates = weekday_map[weekday]
        site_ids = st.text_input("Enter site IDs (comma separated)", "9242,9241")
        site_ids = [s.strip() for s in site_ids.split(",")]
        mode = st.selectbox("Select mode", [1, 2, 3], index=1)
        st.write(f"Showing data for {weekday}s: {dates}")

        st.subheader("Line Graph: Stayed and Exit by Hour")
        fig1 = plot_stayed_exit_by_hour_for_weekdays_same_colors(df, site_ids, dates, mode, weekday_name=weekday)
        st.pyplot(fig1)

        st.subheader("Bar/Line Graph: Average Captation and Stayed per Hour")
        fig2 = plot_avg_captation_and_stayed_per_hour(df, site_ids, dates, mode, weekday_name=weekday)
        st.pyplot(fig2)

    else:
        # --- Weekly/Monthly dashboard ---
        month_map = {
            'January': enero,
            'February': febrero,
            'March': marzo,
            'April': abril
        }
        month = st.selectbox("Select a month", list(month_map.keys()))
        week_dates = month_map[month]
        site_ids = st.text_input("Enter site IDs (comma separated)", "9242,9241", key="month_site_ids")
        site_ids = [s.strip() for s in site_ids.split(",")]
        mode = st.selectbox("Select mode", [1, 2, 3], index=1, key="month_mode")
        st.write(f"Showing data for {month}: {week_dates}")

        st.subheader("Weekly Exit vs Stayed Percentage (Pie Chart)")
        fig3 = plot_weekly_exit_vs_stayed_pie(df, site_ids, week_dates, mode)
        st.pyplot(fig3)

        st.subheader("Peak Hour Exit vs Stayed Percentage (Pie Chart)")
        fig4 = plot_weekly_exit_vs_stayed_pie_peak(df, site_ids, week_dates, mode, peak_ranges)
        st.pyplot(fig4)