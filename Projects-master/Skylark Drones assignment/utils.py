from geopy.distance import vincenty


def dms_to_dd(gps_data):
    
    ##GPS data is in Deg min sec to be converted in Degrees
    Degrees = float(gps_data[0][0]) / float(gps_data[0][1])

    Minutes = float(gps_data[1][0]) / float(gps_data[1][1])

    Seconds = float(gps_data[2][0]) / float(gps_data[2][1])

    return Degrees + (Minutes / 60.0) + (Seconds / 3600.0)


def calculate_distance_on_earth(strt_lat_dec_deg,strt_long_dec_deg,stp_lat_dec_deg,stp_long_dec_deg):
    #Enter the start and stop lattitude and Longitude in Decimal Degrees 
    start=(strt_lat_dec_deg,strt_long_dec_deg)
    stop=(stp_lat_dec_deg,stp_long_dec_deg)
    dist_in_meters=vincenty(start,stop).meters
    return dist_in_meters 


