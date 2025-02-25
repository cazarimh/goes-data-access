from netCDF4 import Dataset             # Read / Write NetCDF4 files
import datetime                         # Basic Dates and time types
import os                               # Miscellaneous operating 
import shutil                           #  system interfaces
import boto3                            # Amazon Web Services (AWS) SDK for Python
from botocore import UNSIGNED           # boto3 config
from botocore.config import Config      # boto3 config
import math                             # Mathematical functions

#######################################################################

input_archive = "samples"; os.makedirs(input_archive, exist_ok=True)
output_archive = "output"; os.makedirs(output_archive, exist_ok=True)

bucket_name = 'noaa-goes16'

# no dicionario acho melhor trocar as chaves e reduzir a quantidade de produtos, não usaríamos todos
products = {'11': 'ABI-L1b-RadF',
            '12': 'ABI-L2-CMIPF', 
            '13': 'ABI-L2-MCMIPF',
            '14': 'ABI-L2-ACHAF',
            '15': 'ABI-L2-ACF',
            '16': 'ABI-L2-ACMF',
            '17': 'ABI-L2-ACTPF',
            '18': 'ABI-L2-CTPF',
            '19': 'ABI-L2-CODF',
            '1A': 'ABI-L2-CPSF',
            '1C': 'ABI-L2-ADPF',
            '1D': 'ABI-L2-AODF',
            '1E': 'ABI-L2-BRFF',
            '1F': 'ABI-L2-DMWF',
            '1G': 'ABI-L2-DMWVF',
            '1H': 'ABI-L2-TPWF',
            '1I': 'ABI-L2-DSIF',
            '1J': 'ABI-L2-LVMPF',
            '1K': 'ABI-L2-LVTPF',
            '1L': 'ABI-L2-DSRF',
            '1M': 'ABI-L2-FDCF',
            '1N': 'ABI-L2-FSCF',
            '1O': 'ABI-L2-LSAF',
            '1P': 'ABI-L2-LSTF',
            '1Q': 'ABI-L2-RRQPEF',
            '1R': 'ABI-L2-RSRF',
            '1S': 'ABI-L2-SSTF',
            '2': 'GLM-L2-LCFA'}

days_in_yearA = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
days_in_yearB = [0, 31, 60, 91, 121, 152, 182, 213, 243, 274, 305, 335]

utc = datetime.timezone(datetime.timedelta(hours=0))
date = datetime.datetime.now(utc)

#######################################################################

def latlon2xy(lat, lon):
    # goes_imagery_projection:semi_major_axis
    req = 6378137 # meters
    #  goes_imagery_projection:inverse_flattening
    invf = 298.257222096
    # goes_imagery_projection:semi_minor_axis
    rpol = 6356752.31414 # meters
    e = 0.0818191910435
    # goes_imagery_projection:perspective_point_height + goes_imagery_projection:semi_major_axis
    H = 42164160 # meters
    # goes_imagery_projection: longitude_of_projection_origin
    lambda0 = -1.308996939

    # Convert to radians
    latRad = lat * (math.pi/180)
    lonRad = lon * (math.pi/180)

    # (1) geocentric latitude
    Phi_c = math.atan(((rpol * rpol)/(req * req)) * math.tan(latRad))
    # (2) geocentric distance to the point on the ellipsoid
    rc = rpol/(math.sqrt(1 - ((e * e) * (math.cos(Phi_c) * math.cos(Phi_c)))))
    # (3) sx
    sx = H - (rc * math.cos(Phi_c) * math.cos(lonRad - lambda0))
    # (4) sy
    sy = -rc * math.cos(Phi_c) * math.sin(lonRad - lambda0)
    # (5)
    sz = rc * math.sin(Phi_c)

    # x,y
    x = math.asin((-sy)/math.sqrt((sx*sx) + (sy*sy) + (sz*sz)))
    y = math.atan(sz/sx)

    return x, y

def geo2grid(lat, lon, nc):

    # Apply scale and offset 
    xscale, xoffset = nc.variables['x'].scale_factor, nc.variables['x'].add_offset
    yscale, yoffset = nc.variables['y'].scale_factor, nc.variables['y'].add_offset
    
    x, y = latlon2xy(lat, lon)
    col = (x - xoffset)/xscale
    lin = (y - yoffset)/yscale
    return int(lin), int(col)

#######################################################################

def main():

    # coord = (-22.852158, -47.127280) # CTI

    # data = get_lightning(coord, date)

    return 0

def get_info(key: str, date: object, band: int = 0) -> list[str]:
    """Get all the necessary info to find a archive on aws"""
    
    product_name = products[key]

    year = date.year
    month = date.month
    day = date.day
    hour = date.hour
    minutes = date.minute

    minutes -= minutes % 3
    if (minutes >= 3):
        minutes -= 3
    else:
        minutes += 57
        hours -= 1

    month -= 1

    days_in_year = days_in_yearB[:] if (year % 4 == 0) else days_in_yearA[:]
    day_of_year = days_in_year[month] + day

    if (band != 0):
        prefix = f'{product_name}/{year}/{day_of_year:03.0f}/{hour:02.0f}/OR_{product_name}-M6C{band:02.0f}_G16_s{year}{day_of_year:03.0f}{hour:02.0f}{minutes:02.0f}'
    else:
        if (key == '2'):
            prefix = f'{product_name}/{year}/{day_of_year:03.0f}/{hour:02.0f}/OR_{product_name}_G16_s{year}{day_of_year:03.0f}{hour:02.0f}{minutes:02.0f}'
        else:
            prefix = f'{product_name}/{year}/{day_of_year:03.0f}/{hour:02.0f}/OR_{product_name}-M6_G16_s{year}{day_of_year:03.0f}{hour:02.0f}{minutes:02.0f}'

    
    cloud_mask = f'ABI-L2-ACMF/{year}/{day_of_year:03.0f}/{hour:02.0f}/OR_ABI-L2-ACMF-M6_G16_s{year}{day_of_year:03.0f}{hour:02.0f}{minutes:02.0f}'

    return [prefix, cloud_mask]

def download_aws(prefix: str, product: str):
    """Download a file from aws"""

    s3_client = boto3.client('s3', config=Config(signature_version=UNSIGNED))
    s3_result = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix, Delimiter = "/")

    if ('Contents' in s3_result):
        s3_client.download_file(bucket_name, s3_result['Contents'][0]['Key'],f'{input_archive}/current_{product}.nc')
        shutil.copy(f'{input_archive}/current_{product}.nc', f'{input_archive}/last_{product}.nc')

        return f'{input_archive}/current_{product}.nc'

    return f'{input_archive}/last_{product}.nc'

def get_lightning(coord: tuple, date: object) -> int:
    """Return the number of flashes in a radius of 100km approximately"""

    key = '2'
    prefix, cloud_mask_prefix = get_info(key, date)
    file_path = download_aws(prefix, products[key])
    file = Dataset(file_path)

    lightning_lat = file['flash_lat'][:]
    lightning_lon = file['flash_lon'][:]
    lightning_count = 0

    for i in range(len(lightning_lat)):
        if math.fabs(lightning_lat[i] - coord[0]) <= 1 and math.fabs(lightning_lon[i] - coord[1]) <= 1:
            if file['flash_quality_flag'][i] == 0:
                lightning_count += 1
    
    return lightning_count

main()
