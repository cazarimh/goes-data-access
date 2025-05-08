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

def get_lightning_data(coord: tuple) -> tuple:
    """Returns the events of flashes in a radius of 100km approximately"""

    file_path = aws.awsAccessGOES.download_aws('2')
    file = Dataset(file_path)

    lightning_lat = file['flash_lat'][:]
    lightning_lon = file['flash_lon'][:]
    lightning_count = 0
    lightning_event = []

    for i in range(len(lightning_lat)):
        if (np.fabs(lightning_lat[i] - coord[0]) <= 1 and np.fabs(lightning_lon[i] - coord[1]) <= 1):
            if (file['flash_quality_flag'][i] == 0):
                lightning_event.append(tuple(map(float, (lightning_lat[i], lightning_lon[i], file['flash_energy'][i]/1e-12))))
                lightning_count += 1

    file.close()
    
    return (lightning_event, lightning_count)

def get_fireSpot_data(coord: tuple) -> int:
    """Returns the number of fire spots in a radius of 100km approximately"""

    file_path = aws.awsAccessGOES.download_aws('1M')
    file = Dataset(file_path)

    i, j = aws.awsAccessGOES.geo2grid(coord[0], coord[1], file)

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

    file_path = aws.awsAccessGOES.download_aws('1Q')
    file = Dataset(file_path)

    i, j = aws.awsAccessGOES.geo2grid(coord[0], coord[1], file)

    rain_data = float(file['RRQPE'][i][j])

    file.close()

    return int(rain_data)

main()
