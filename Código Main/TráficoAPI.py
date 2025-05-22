import pandas as pd
import requests

locations_df = pd.read_csv('locationsSinComa.csv')
locations = locations_df.to_dict(orient='records')

# TODO Terminar lista de locations de la M6 hacia el norte 

StartDate = '01012025'
EndDate = '30042025'
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


# Función para obtener el Id de M6
def get_Id_M6(Site):
    found_inactive = False
    site = Site.strip().upper()
    # Verificar si la clave 'sites' está en la respuesta
    if 'sites' in dataSites:
        # Iterar sobre los sitios y buscar el Id correspondiente
        for row in dataSites['sites']:
            desc = row.get('Description', '').strip().upper()
            
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
                    return site_id, direction
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
        site_id, direction = get_Id_M6(site_name)
        location['Id'] = str(site_id) if site_id is not None else ''
        location['Direction'] = direction  
    

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

# Guardar el DataFrame en un archivo CSV
df.to_csv('traffic_data_full.csv', index=False)


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
