# encoding=utf8

import serial
import subprocess
import time

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
        try:
            line = ser.readline()
            if "GPGGA" in line:
                gps=line.split(",")
                if gps[2]:
                    latitude,longitude = convert_gpgga_to_dd(gps)
                    return  "%s, -%s" % ( str(latitude), str(longitude))
                else:
                    return "unable to read gps"
        except OSError:
            subprocess.call("reboot",shell=True)
        except:
            time.sleep(2)
            output = readgps()
            return output

if __name__ == "__main__":
        output = readgps()
        print output

