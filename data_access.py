import aws_access as aws
import numpy as np
from netCDF4 import Dataset

def main():

    coord = (-22.852158, -47.127280) # CTI Renato Archer coordinates

    key = int(input('''Choose a data type:
    1. Lightning Events (coordinates, energy)
    2. Fire Spot Count
    3. Rainfall Rate (mm/h)
    '''))

    match key:
        case 1:
            new_data = get_lightning_data(coord)
            key = 'lightning_data' 
        case 2:
            new_data = get_fireSpot_data(coord)
            key = 'fireSpot_count'
        case 3:
            new_data = get_rainfallRate_data(coord)
            key = 'rainfall_rate'
        case _:
            new_data = 0
            key = 'null'
        
    print(f'{new_data}, {key}')

    return 0
    
def get_lightning_data(coord: tuple, dist: int =100) -> tuple:
    """Returns the events of flashes in a radius of 100km approximately by default"""

    file_path = aws.awsAccessGOES.download_aws('Lightning')
    file = Dataset(file_path)

    lightning_lat = file['flash_lat'][:]
    lightning_lon = file['flash_lon'][:]
    lightning_count = 0
    lightning_events = []
    
    latlondiff = dist/111
    (lat, lon) = coord

    for i in range(len(lightning_lat)):
        if (np.abs(lightning_lat[i] - lat) <= latlondiff and np.abs(lightning_lon[i] - lon) <= latlondiff):
            if (file['flash_quality_flag'][i] == 0):
                lightning_events.append(tuple(map(float, (lightning_lat[i], lightning_lon[i], file['flash_energy'][i]/1e-12))))
                lightning_count += 1

    file.close()
    
    return (lightning_events, lightning_count)

def get_fireSpot_data(coord: tuple) -> int:
    """Returns the number of fire spots in a radius of 100km approximately"""

    file_path = aws.awsAccessGOES.download_aws('Firespot')
    file = Dataset(file_path)

    (lat, lon) = coord

    i, j = aws.awsAccessGOES.geo2grid(lat, lon, file)

    data = file['DQF'][:]
    data = [line[j - 12 : j + 13] for line in data[i - 12 : i + 13]]

    fireSpot_count = 0

    for i in range(len(data)):
        for j in range(len(data[i])):
            if (data[i][j] == 0):
                fireSpot_count += 1

    file.close()
    
    return fireSpot_count

def get_rainfallRate_data(coord: tuple) -> int:
    """Returns the Rainfall Rate in a specific location"""

    file_path = aws.awsAccessGOES.download_aws('Rainfall Rate')
    file = Dataset(file_path)

    (lat, lon) = coord

    i, j = aws.awsAccessGOES.geo2grid(lat, lon, file)

    rain_data = float(file['RRQPE'][i][j])
    rain_data = float(file['RRQPE'][:][i][j])
    max_rain = float(file['maximum_rainfall_rate'][0])

    file.close()

    return int(rain_data) if rain_data <= max_rain else 0

main()
