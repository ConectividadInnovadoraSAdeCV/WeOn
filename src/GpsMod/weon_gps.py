# encoding=utf8

import serial

def convert_gpgga_to_dd(gps):
    minutes=60
    lat_degree = float(gps[2][:2])
    lat_min = float(gps[2][2:])
    long_degree = float(gps[4][:3])
    long_min = float(gps[4][3:])
    lat = ( lat_min / minutes ) + lat_degree
    longi = ( long_min / minutes ) + long_degree
    return  (lat, longi)

def readgps():
    ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)
    """Read the GPG LINE using the NMEA standard"""
    latitude=''
    longitude=''
    while True:
        line = ser.readline()
        if "GPGGA" in line:
            print line
            gps=line.split(",")
            latitude,longitude = convert_gpgga_to_dd(gps)
            print "%s, %s " % (latitude, longitude)
            if gps[0][4] == 'M':
                latitude = '0000.0000'
                longitude = '0000.0000'
            return(latitude, '-'+longitude)

if __name__ == "__main__":
        output = readgps()
        print output

