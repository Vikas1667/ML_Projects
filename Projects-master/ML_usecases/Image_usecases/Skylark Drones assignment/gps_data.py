from utils import dms_to_dd
import glob
from itertools import groupby
import piexif


def get_gps_data_from_images():
    imagesData = {}

    
    for img in glob.glob('/home/vicky/Desktop/Skylark_Drones/images/*.JPG'):
        
        img_dict = piexif.load(img)
        GPS_data =img_dict.get('GPS')
        try:
            GPS_latitude  = GPS_data[2]
            GPS_longitude = GPS_data[4]
        except:
            print("Key 2 is not found")
        latitude=dms_to_dd(GPS_latitude)
        longitude=dms_to_dd(GPS_longitude)
        imagesData[img[20:]]= [longitude, latitude]
    return imagesData

def srt():
       
    with open('/home/vicky/Desktop/Skylark_Drones/videos/DJI_0301.SRT') as file:
        results = [list(f)
               for t, f in groupby(file, lambda x: bool(x.strip())) if t]

    return results
