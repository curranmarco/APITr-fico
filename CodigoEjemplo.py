import pandas as pd
import requests # to pull data from the API
from datetime import datetime 
import pytz
import pyodbc 

locations= [
    {'Region':'Mexico','Country':'Mexico','Business Unit':'Circuito Exterior Mexiquense','Plaza':'T-0 Jorobas','Latitude':'19.819800000', 'Longitude':'-99.239900000'},
    {'Region':'Mexico','Country':'Mexico','Business Unit':'Circuito Exterior Mexiquense','Plaza':'T-1 Tultepec','Latitude':'19.693908470', 'Longitude':'-99.080522610'},
    {'Region':'Mexico','Country':'Mexico','Business Unit':'Circuito Exterior Mexiquense','Plaza':'T-2 Conmex','Latitude':'19.575363000', 'Longitude':'-99.020846000'},
    {'Region':'Mexico','Country':'Mexico','Business Unit':'Circuito Exterior Mexiquense','Plaza':'T-3 Nabor Carrillo','Latitude':'19.435800000', 'Longitude':'-98.998000000'},
    {'Region':'Mexico','Country':'Mexico','Business Unit':'Circuito Exterior Mexiquense','Plaza':'T-4 Chalco','Latitude':'19.300206050', 'Longitude':'-98.875591110'},
    {'Region':'Mexico','Country':'Mexico','Business Unit':'Circuito Exterior Mexiquense','Plaza':'T-5 Tultitlan','Latitude':'19.638088890', 'Longitude':'-99.164458330'},
    {'Region':'Mexico','Country':'Mexico','Business Unit':'Circuito Exterior Mexiquense','Plaza':'T-6 Cuautitlán','Latitude':'19.635597220','Longitude':'-99.205244440'},
    {'Region':'Mexico','Country':'Mexico','Business Unit':'Circuito Exterior Mexiquense','Plaza':'T-7 Texcoco','Latitude':'19.450410000', 'Longitude':'-98.903430000'},
    {'Region':'Mexico','Country':'Mexico','Business Unit':'Autopista Urbana Norte','Plaza':'San Antonio','Latitude':'19.382504930', 'Longitude':'-99.19170675'},
    {'Region':'Mexico','Country':'Mexico','Business Unit':'Viaducto Bicentenario','Plaza':'Toreo','Latitude':'19.456921000', 'Longitude':'-99.22059400'},
    {'Region':'Mexico','Country':'Mexico','Business Unit':'Viaducto Bicentenario','Plaza':'Tepalcapa','Latitude':'19.630146120', 'Longitude':'-99.19340163'},
    {'Region':'Mexico','Country':'Mexico','Business Unit':'Viaducto Bicentenario','Plaza':'Lomas Verdes','Latitude':'19.488037030', 'Longitude':'-99.23945889'},
    {'Region':'Mexico','Country':'Mexico','Business Unit':'Supervía','Plaza':'Poetas','Latitude':'19.346366670', 'Longitude':'-99.253272220'},
    {'Region':'Mexico','Country':'Mexico','Business Unit':'Supervía','Plaza':'Periférico','Latitude':'19.321900000', 'Longitude':'-99.221800000'},
    {'Region':'Mexico','Country':'Mexico','Business Unit':'Grupo Autopistas Nacionales','Plaza':'Amozoc','Latitude':'19.063619440', 'Longitude':'-98.068789850'},
    {'Region':'Mexico','Country':'Mexico','Business Unit':'Grupo Autopistas Nacionales','Plaza':'Perote','Latitude':'19.551216670', 'Longitude':'-97.289433330'},
    {'Region':'Mexico','Country':'Mexico','Business Unit':'Libramiento Elevado de Puebla','Plaza':'Periferico','Latitude':'19.133933330', 'Longitude':'-98.27085000'},
    {'Region':'Mexico','Country':'Mexico','Business Unit':'Libramiento Elevado de Puebla','Plaza':'Cuauhtémoc','Latitude':'19.076300000', 'Longitude':'-98.14746667'},
    {'Region':'South America','Country':'Colombia','Business Unit':'Autopista Río Magdalena','Plaza':'Peaje Puerto Berrio','Latitude':'6.496715069', 'Longitude':'-74.500984192'},
    {'Region':'South America','Country':'Peru','Business Unit':'Autopista del Norte','Plaza':'VIRÚ','Latitude':'-8.377378010', 'Longitude':'-78.86070348'},
    {'Region':'South America','Country':'Peru','Business Unit':'Autopista del Norte','Plaza':'VESIQUE','Latitude':'-9.174480080', 'Longitude':'-78.48115953'},
    {'Region':'South America','Country':'Peru','Business Unit':'Autopista del Norte','Plaza':'HUARMEY','Latitude':'-10.103000000', 'Longitude':'-78.13910000'},
    {'Region':'South America','Country':'Peru','Business Unit':'Autopista del Norte','Plaza':'Peaje Fortaleza','Latitude':'-10.602451230', 'Longitude':'-77.87085994'},
    {'Region':'South America','Country':'Chile','Business Unit':'Autopista Vespucio Oriente','Plaza':'P109 Pte. Centenario','Latitude':'-33.390710', 'Longitude':'-70.596056'},
    {'Region':'South America','Country':'Chile','Business Unit':'Autopista Vespucio Oriente','Plaza':'P101 Bilbao','Latitude':'-33.429650', 'Longitude':'-70.574860'},
    {'Region':'South America','Country':'Chile','Business Unit':'Autopista Nogales-Puchuncaví','Plaza':'Nogales','Latitude':'-32.752885199', 'Longitude':'-71.253032684'},
    {'Region':'Europe','Country':'United Kingdom','Business Unit':'M6Toll','Plaza':'Great Wyrley','Latitude':'52.667800820', 'Longitude':'-2.000204950'},
    {'Region':'Europe','Country':'United Kingdom','Business Unit':'M6Toll','Plaza':'Weeford Park','Latitude':'52.623159970', 'Longitude':'-1.800693850'},
    {'Region':'Europe','Country':'Spain','Business Unit':'M45 Euroglosa','Plaza':'PM001','Latitude':'40.359085083', 'Longitude':'-3.764394045'},
    {'Region':'Europe','Country':'Spain','Business Unit':'M45 Euroglosa','Plaza':'PM009','Latitude':'40.329341888', 'Longitude':'-3.721638918'},
    {'Region':'Europe','Country':'Spain','Business Unit':'Autovia de Aragón','Plaza':'PM001','Latitude':'40.446868896', 'Longitude':'-3.654227972'},
    {'Region':'Europe','Country':'Italy','Business Unit':'A35 Brebemi','Plaza':'Chiari Est','Latitude':'45.504741594', 'Longitude':'9.446916580'},
    {'Region':'Europe','Country':'Italy','Business Unit':'A35 Brebemi','Plaza':'Chiari Ovest','Latitude':'45.514839172', 'Longitude':'9.916866302'}
]


API_KEY='489bcef15217bda76eb2d1bce48106dc'


# Time zones
mexico_tz=pytz.timezone('America/Mexico_City')
chile_tz=pytz.timezone('America/Santiago')
colombia_tz=pytz.timezone('America/Bogota')
peru_tz=pytz.timezone('America/Lima')
uk_tz=pytz.timezone('Europe/London')
spain_tz=pytz.timezone('Europe/Madrid')
italy_tz=pytz.timezone('Europe/Rome')

# CURRENT DATA

def get_weather_data(lat,lon):
    url=f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response=requests.get(url)
    if response.status_code == 200: # checks that the response was successful and handles errors with the else block
        return response.json()
    else:
        return None


data=[]
for loc in locations:
    weather=get_weather_data(loc['Latitude'], loc['Longitude'])
    print(weather)
    if weather:
       main_weather=weather['main']
       wind=weather['wind']
       weather_desc=weather['weather'][0]['description']
       #rain=weather['rain']['1h']
       #snow=weather['snow']['1h']
       # Fecha de auditoría
       dt_audition=datetime.fromtimestamp(weather['dt']).strftime('%Y-%m-%d %H:%M:%S')
       # Fecha local: Si no se ejecuta desde España hay que cambiar spain_tz por el país correspondiente
       dt_execution=spain_tz.localize(datetime.fromtimestamp(weather['dt']))
       if loc['Country']=='Mexico':
          dt_local=dt_execution.astimezone(mexico_tz).strftime("%Y-%m-%d %H:%M:%S")
       elif loc['Country']=='Chile':
          dt_local=dt_execution.astimezone(chile_tz).strftime("%Y-%m-%d %H:%M:%S")
       elif loc['Country']=='Colombia':
          dt_local=dt_execution.astimezone(colombia_tz).strftime("%Y-%m-%d %H:%M:%S")
       elif loc['Country']=='Peru':
          dt_local=dt_execution.astimezone(peru_tz).strftime("%Y-%m-%d %H:%M:%S")
       elif loc['Country']=='United Kingdom':
          dt_local=dt_execution.astimezone(uk_tz).strftime("%Y-%m-%d %H:%M:%S") 
       elif loc['Country']=='Spain':
          dt_local=dt_execution.astimezone(spain_tz).strftime("%Y-%m-%d %H:%M:%S")
       elif loc['Country']=='Italy':
          dt_local=dt_execution.astimezone(italy_tz).strftime("%Y-%m-%d %H:%M:%S")   
       else: 
          None     
       
       data.append({
            'region':loc['Region'],
            'country':loc['Country'],
            'business_unit':loc['Business Unit'],
            'location':loc['Plaza'],
            'latitude':loc['Latitude'],
            'longitude':loc['Longitude'],
            'local_datetime':dt_local,
            'aud_datetime': dt_audition,
            'temperature':main_weather['temp'],
            'feels_like':main_weather['feels_like'],
            'temperature_min':main_weather['temp_min'],
            'temperature_max':main_weather['temp_max'],
            'pressure':main_weather['pressure'],
            'humidity':main_weather['humidity'],
            'sea_level':main_weather['sea_level'],
            'ground_level':main_weather['grnd_level'],
            'visibility':weather['visibility'],
            'wind_speed':wind['speed'],
            'clouds':weather['clouds']['all'],
            'weather_description':weather_desc
            #'rain':rain,
            #'snow':snow
        })

df=pd.DataFrame(data)
print(df)

# Export the dataframe to SQL server
server = 'operacionesaleatica.database.windows.net' 
database = 'Weather' 
username = 'weather_db' 
password = 'W34th3r%4L3' 
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)
cursor = cnxn.cursor()
# SQL Operation
operation = "INSERT INTO mesurements (region, country, business_unit, location, latitude, longitude, local_datetime, temperature, feels_like, temperature_min, temperature_max, pressure, humidity, sea_level, ground_level, visibility, wind_speed, clouds, weather_description, aud_datetime) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"

for _, row in df.iterrows():
    cursor.execute(operation, row['region'],row['country'],row['business_unit'],row['location'],row['latitude'],row['longitude'],row['local_datetime'],row['temperature'],row['feels_like'],row['temperature_min'],row['temperature_max'],row['pressure'],row['humidity'],row['sea_level'],row['ground_level'],row['visibility'],row['wind_speed'],row['clouds'],row['weather_description'],row['aud_datetime'])

# Save the data permanently
cnxn.commit() 
# Close the connection
cursor.close() 
cnxn.close()

# HISTORICAL DATA

start=spain_tz.localize(datetime.strptime('2024-11-07 00:00:00', '%Y-%m-%d %H:%M:%S'))
start=int(start.timestamp()) # Convertimos a formato Unix
end=spain_tz.localize(datetime.strptime('2024-11-08 00:00:00', '%Y-%m-%d %H:%M:%S'))
end=int(end.timestamp()) # Convertimos a formato Unix

def get_historical_data(lat,lon):
    url=f"https://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lon}&type=hour&start={start}&end={end}&appid={API_KEY}"
    response=requests.get(url)
    if response.status_code == 200: # checks that the response was successful and handles errors with the else block
        return response.json()
    else:
        return None

def get_historical_data(lat, lon): 
   url = f"https://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lon}&type=hour&start={start}&end={end}&appid={API_KEY}" 
   response = requests.get(url)
   print(f"URL: {url}") 
   print(f"Response status code: {response.status_code}") 
   print(f"Response content: {response.content}") 
   if response.status_code == 200: return response.json()
   else: print("Error occurred: ", response.status_code) 
   return None

weather=get_historical_data('19.635451536187006','-99.20509718791541')