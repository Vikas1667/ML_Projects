
from utils import calculate_distance_on_earth
from gps_data import get_gps_data_from_images
from gps_data import srt
import csv


def csv_file(frame_no, image_list):
    
    with open('/home/vicky/Desktop/Skylark_Drones/video.csv', 'a') as outfile:
        outfile.write(frame_no.replace(',', '.'))
        outfile.write(',')
        outfile.write('15:'.join(image_list))
        outfile.write('\n')


def get_images(images_data, longitude, latitude, req_distance):
    """
    Retrieves images lying within the radius of a 
    frame location using haversine formulae.
    """

    image_list = []
    
    for image_name, image_data in images_data.items():
        longitude1, latitude1= map(float, image_data)

        distance = calculate_distance_on_earth(longitude, latitude, longitude1, latitude1)

          
        if distance < req_distance:
            image_list.append(image_name)

    return image_list

def check_frames(frames, images_data):
    """Get the images from 35meters"""
    for frame in frames:
        lon2, lat2, alt2 = frame[2].strip('\n').split(',')
        image_list = get_images(images_data, lon2, lat2, 35)
        csv_file(frame[1].split('-->')[0], image_list)

def check_poi(filename, images_data):
    """
    Adds all images lying 50m near to Point of interests. 
    """

    with open(filename, 'r') as rfile, open('/home/vicky/Desktop/Skylark_Drones/spread_sheet.csv', 'w') as wfile:

        reader = csv.DictReader(rfile)

        fieldnames = ['asset_name', 'longitude', 'latitude', 'image_names']
        writer = csv.DictWriter(wfile, fieldnames=fieldnames)

        writer.writeheader()

        for row in reader:
            lon2 = row['longitude']
            lat2 = row['latitude']
            image_list = get_images(images_data, lon2, lat2, 50)

            row['image_names'] = ':'.join(image_list)
            writer.writerow(row)




def main():
    """
    Driver function
    """
    images_data = get_gps_data_from_images()
    frames = srt()

    check_frames(frames, images_data)
    check_poi('/home/vicky/Desktop/Skylark_Drones/assets.csv', images_data)

    #trace_drone_path(frames)

if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   main()


