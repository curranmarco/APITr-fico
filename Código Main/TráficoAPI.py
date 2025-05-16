import pandas as pd
import requests


locations = [
    {'Highway' : 'M6Toll', 'Id': '9228', 'Site' : '7671/1' },
    {'Highway' : 'M6Toll', 'Id': '9229', 'Site' : '7671/2' },
    {'Highway' : 'M6Toll', 'Id': '9230', 'Site' : '7672/1' },
    {'Highway' : 'M6Toll', 'Id': '9231', 'Site' : '7672/2' },
    {'Highway' : 'M6Toll', 'Id': '9232', 'Site' : '7673/1' },
    {'Highway' : 'M6Toll', 'Id': '9233', 'Site' : '7673/2' },
    {'Highway' : 'M6Toll', 'Id': '9234', 'Site' : '7674/1' },
    {'Highway' : 'M6Toll', 'Id': '9235', 'Site' : '7674/2' },
    {'Highway' : 'M6Toll', 'Id': '9236', 'Site' : '7675/1' },
    {'Highway' : 'M6Toll', 'Id': '9237', 'Site' : '7675/2' },
    {'Highway' : 'M6Toll', 'Id': '9238', 'Site' : '7676/1' },
    {'Highway' : 'M6Toll', 'Id': '9239', 'Site' : '7676/2' },
    {'Highway' : 'M6Toll', 'Id': '9240', 'Site' : '7677/1' },
    {'Highway' : 'M6Toll', 'Id': '9241', 'Site' : '7678/1' },
    {'Highway' : 'M6Toll', 'Id': '9242', 'Site' : '7678/2' },
    {'Highway' : 'M6Toll', 'Id': '9243', 'Site' : '7679/1' },
    {'Highway' : 'M6Toll', 'Id': '9244', 'Site' : '7679/2' },
    {'Highway' : 'M6Toll', 'Id': '9245', 'Site' : '7680/1' },
    {'Highway' : 'M6Toll', 'Id': '9246', 'Site' : '7680/2' },
    {'Highway' : 'M6Toll', 'Id': '9247', 'Site' : '7681/1' },
    {'Highway' : 'M6Toll', 'Id': '9248', 'Site' : '7681/2' },
    {'Highway' : 'M6Toll', 'Id': '9249', 'Site' : '7682/1' },
    {'Highway' : 'M6Toll', 'Id': '9250', 'Site' : '7682/2' }    
]
StartDate = '01012025'
EndDate = '30042025'
PageSize = 39990 # Hay 96 intervalos de 15 minutos en un día, con lo que 39990 intervalos cubren desde el 1 de enero de 2025 hasta el 31 de marzo de 2025

def get_traffic_data(Id):
    url = f'https://webtris.nationalhighways.co.uk/api/v1.0/reports/daily?sites={Id}&start_date={StartDate}&end_date={EndDate}&page=1&page_size={PageSize}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def get_quality_traffic_data(Id):
    url = f'https://webtris.nationalhighways.co.uk/api/v1.0/quality/daily?siteid={Id}&start_date={StartDate}&end_date={EndDate}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

# Lista para almacenar los datos
data=[]
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
        print(f"No quality data found for {location['Site']} with Id {Id}")


    #print(traffic_data)
    # Verificar si se obtuvo la respuesta y si contiene datos
    if traffic_data and 'Rows' in traffic_data:
        # Extraer los datos que nos interesan
        for row in traffic_data['Rows']:
            Date = row.get('Report Date')
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
        print(f"No data found for {location['Site']} with Id {Id}")
    
    """
    if quality_data and 'Qualities' in quality_data:
        # Extraer los datos de calidad
        for row in quality_data['Qualities']:
            Quality = row.get('Quality')
            data.append({
                'Quality' : Quality
            })
    else :
        print(f"No quality data found for {location['Site']} with Id {Id}")   
    """        
    
# Convertir la lista de datos a un DataFrame de pandas
df = pd.DataFrame(data)
#print(df)
# Guardar el DataFrame en un archivo CSV
#df.to_csv('traffic_data.csv', index=False)
# Guardar el DataFrame en un archivo Excel
df.to_excel('traffic_data.xlsx', index=False)