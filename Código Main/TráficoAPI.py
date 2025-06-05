import pandas as pd
import requests
import pyodbc

locations_df = pd.read_csv('locationsSinComa.csv')
locations = locations_df.to_dict(orient='records')

# TODO Terminar lista de locations de la M6 hacia el norte 

StartDate = '01012025'
EndDate = '31052025'
PageSize = 12000 # Hay 96 intervalos de 15 minutos en un día, con lo que 12000 intervalos cubren desde el 1 de enero de 2025 hasta el 31 de marzo de 2025

# Función para obtener los datos de tráfico
def get_traffic_data(Id):
    url = f'https://webtris.nationalhighways.co.uk/api/v1.0/reports/daily?sites={Id}&start_date={StartDate}&end_date={EndDate}&page=1&page_size={PageSize}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

# Función para obtener los datos de calidad
def get_quality_traffic_data(Id):
    url = f'https://webtris.nationalhighways.co.uk/api/v1.0/quality/daily?siteid={Id}&start_date={StartDate}&end_date={EndDate}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

url = 'https://webtris.nationalhighways.co.uk/api/v1.0/sites'
response = requests.get(url)
# Verificar si la respuesta es exitosa
if response.status_code == 200:
    dataSites = response.json()
else :
    print(f"Error: {response.status_code}")


# Función para obtener el Id, Status, Latitud y Longitud de el site correspondiente
def get_Attr(Site):
    found_inactive = False
    site = Site.strip().upper()
    # Verificar si la clave 'sites' está en la respuesta
    if 'sites' in dataSites:
        # Iterar sobre los sitios y buscar el Id correspondiente
        for row in dataSites['sites']:
            desc = row.get('Description', '').strip().upper()
            latitude = row.get('Latitude')
            longitude = row.get('Longitude')
            
            # Recogemos el status para ver si el site está activo o inactivo 
            status = row.get('Status', '').strip() 
            
            # Comparar el nombre del sitio con la descripción
            if desc == site:
                # Si se encuentra un site, comprobar su status
                # Si el status es 'Active', devolver el Id 
                if status == 'Active':
                    site_id = row.get('Id')
                    name = row.get('Name', '')
                    direction = name[-10:].strip() if len(name) > 10 else ''
                    return site_id, direction, latitude, longitude
                else:
                    found_inactive = True
        
        #! Esto solo ocurre si no se encuentra un Id activo para el site
        #! o no se encuentra un Id para el site
        if found_inactive:
            print(f'Inactive site found for {site}.')
        else: 
            print(f'Site {site} not found in API response.')
                         
    else:
        print("No 'sites' key in API response!")
            
    return None

# Apendar los Ids a la lista locations
for location in locations:
    if 'Id' not in location or not location['Id']:
        site_name = location['Site']
        site_id, direction, longitude, latitude = get_Attr(site_name)
        location['Id'] = str(site_id) if site_id is not None else ''
        location['Direction'] = direction  
        location['Longitude'] = longitude
        location['Latitude'] = latitude
    
def interval_to_time(interval):
    # Pasar el intervalo a entero por si acaso
    interval = int(interval)
    # Dividirlo entre cautro para obtener la hora
    hour = interval // 4
    # Obtener el minuto correspondiente al intervalo, que lo hace cogiendo el resto de la division entre 4
    # 0 -> 00, 1 -> 15, 2 -> 30, 3 -> 45
    minute = [14,29,44,59][interval % 4]
    # Devolver la hora y el minuto en formato HH:MM:SS, asegurandose que siempre tenga dos digitos
    return f"{hour:02d}:{minute:02d}:00"


# Lista para almacenar los datos
data=[]

# Iterar sobre cada ubicación y obtener los datos de tráfico
for location in locations:
    # Construir la URL para cada ubicación
    Id = location['Id']
    traffic_data = get_traffic_data(Id)
    quality_data = get_quality_traffic_data(Id)

    # Crear un diccionario para almacenar los datos de calidad por fecha
    qualitybyDate = {}
    # Verificar si se obtuvo la respuesta y si contiene datos
    if quality_data and 'Qualities' in quality_data:
        for q in quality_data['Qualities']:
            # Extraer los datos de calidad
            date = q.get('Date', '')[:10]
            qualitybyDate[date] = q.get('Quality', '')
    else:
        #! No hay datos de calidad
        print(f"No quality data found for {location['Site']} with Id {Id}")


    #print(traffic_data)
    # Verificar si se obtuvo la respuesta y si contiene datos
    if traffic_data and 'Rows' in traffic_data:
        # Extraer los datos que nos interesan
        for row in traffic_data['Rows']:
            Date = row.get('Report Date').strip()[:10]
            TimeInterval = row.get('Time Interval')
            AverageSpeed = row.get('Avg mph')
            TotalTraffic = row.get('Total Volume')
            Cars0520 = row.get('0 - 520 cm')
            Cars521660 = row.get('521 - 660 cm')
            Cars6611160 = row.get('661 - 1160 cm')
            Cars1161 = row.get('1160+ cm') 
            quality = qualitybyDate.get(Date[:10] if Date else None)
            
            # Agregar los datos a la lista
            data.append({
                'Highway': location['Highway'],
                'Id': location['Id'],
                'Site': location['Site'],
                'Longitude': location.get('Longitude', ''), 
                'Latitude': location.get('Latitude', ''),
                'Direction': location.get('Direction', ''),
                'Date': Date,
                'TimeInterval': TimeInterval,
                'Cars 0 - 520 cm': Cars0520,
                'Cars 521 - 660 cm': Cars521660,
                'Cars 661 - 1160 cm': Cars6611160,
                'Cars 1160+ cm': Cars1161,
                'AverageSpeed': AverageSpeed,
                'TotalTraffic': TotalTraffic,
                'Quality': quality
            })

        #print(data)
    else:
        #! No hay datos de tráfico
        print(f"No data found for {location['Site']} with Id {Id}")
    
# Convertir la lista de datos a un DataFrame de pandas
df = pd.DataFrame(data)

# Convertir la culumna de intervalo de string a numérico
df['TimeInterval'] = pd.to_numeric(df['TimeInterval'], errors='coerce')

# Utilizar la funcion para convertir el intervalo a la hora correspondiente
df['TimeString'] = df['TimeInterval'].apply(interval_to_time)
# Formatear la columna DateTime correctamente con la fehca y hora para cada intervalo
df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['TimeString'], format='%Y-%m-%d %H:%M:%S', errors='coerce')

# Drop the old Date and TimeString columns if you don't want them
df = df.drop(columns=['Date', 'TimeString', 'TimeInterval'])

# Reorder columns: put DateTime after Direction and before TimeInterval
cols = list(df.columns)
# Find the index of 'Direction'
idx = cols.index('Direction')
# Remove 'DateTime' if already present
cols.remove('DateTime')
# Insert 'DateTime' after 'Direction'
cols.insert(idx + 1, 'DateTime')
# Reorder DataFrame
df = df[cols]



dict_reemplazo = {
    '10464': 'Stayed SB Calf Heath',
    '10654': 'Total SB Calf Heath',
    '9234' : 'Exit SB T6',
    '9235' : 'Stayed SB T6',
    '9238' : 'Exit SB T5',
    '9239' : 'Stayed SB T5',
    '9250' : 'Exit SB T2',
    '9249' : 'Stayed SB T2',
    '9247' : 'Exit NB T3',
    '9248' : 'Stayed NB T3',
    '9243': 'Exit NB T4',
    '9244': 'Stayed NB T4',
    '9242': 'Exit SB T4',
    '9241': 'Stayed SB T4',
    '9237': 'Exit NB T6',
    '9236': 'Stayed NB T6',
    '9233': 'Exit NB T7',
    '9232': 'Stayed NB T7',
    '9228': 'Exit NB T8',
    '9229': 'Stayed NB T8'
}

# Crear una nueva columna 'IdLabel' con los nombres descriptivos, dejando el Id original intacto
df['IdDescription'] = df['Id'].map(dict_reemplazo).fillna(df['Id'])





"""
# Export the dataframe to SQL server
server = 'operacionesaleatica.database.windows.net' 
database = 'Nivel_de_servicio' 
username = 'uk_traffic_user' 
password = '4l3aTic4!tr4FF1c'
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)
cursor = cnxn.cursor()

existing = pd.read_sql(
    "SELECT id, datetime, site FROM [Nivel_de_servicio].[dbo].[uk_traffic_data]",
    cnxn
)
# Merge to find new rows
df = df.merge(existing, left_on=['Id', 'DateTime', 'Site'], right_on=['id', 'datetime', 'site'], how='left', indicator=True)
df = df[df['_merge'] == 'left_only'].drop(columns=['_merge', 'id', 'datetime', 'site'])


# SQL Operation
operation = "INSERT INTO [Nivel_de_servicio].[dbo].[uk_traffic_data] (highway, id, site, longitude, latitude, direction, datetime, cars_0_520_cm, cars_521_660_cm, cars_661_1160_cm, cars_1160_cm, speed_avg, total_traffic, quality) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)"

chunk_size = 100
total_rows = len(df)
for start in range(0, total_rows, chunk_size):
    end = min(start + chunk_size, total_rows)
    chunk = df.iloc[start:end]
    for _, row in chunk.iterrows():
        cursor.execute(operation, row['Highway'], row['Id'], row['Site'], row['Longitude'], row['Latitude'],
                       row['Direction'], row['DateTime'], row['Cars 0 - 520 cm'], row['Cars 521 - 660 cm'],
                       row['Cars 661 - 1160 cm'], row['Cars 1160+ cm'], row['AverageSpeed'],
                       row['TotalTraffic'], row['Quality'])
    cnxn.commit()
    print(f"Uploaded rows {start+1} to {end} of {total_rows}")

# Save the data permanently
cnxn.commit() 
# Close the connection
cursor.close() 
cnxn.close()
"""

# Guardar el DataFrame en un archivo CSV
df.to_csv('traffic_data_full_SQL.csv', index=False)


# Guardar el DataFrame en un archivo Excel
# 1,048,575 + 1 cabecero = 1,048,576 filas (límite de Excel)
"""
max_rows = 1048575  
for i, start in enumerate(range(0, len(df), max_rows)):
    end = min(start + max_rows, len(df))
    chunk = df.iloc[start:end].reset_index(drop=True)
    chunk.to_excel(f'traffic_data_part{i+1}.xlsx', index=False)
#df.to_excel('traffic_data.xlsx', index=False)
"""
