import pandas as pd
df = pd.read_csv('traffic_data_full.csv')

# Convertir las columnas 'Id' y 'Date' a tipo string y eliminar espacios en blanco
df['Id'] = df['Id'].astype(str).str.strip()
df['Date'] = df['Date'].astype(str).str.strip()

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

print(df3) 