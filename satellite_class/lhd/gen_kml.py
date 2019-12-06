import os
import argparse
import pynmea2 as NmeaHandle

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-path', type=str, help='Enter the NMEA.txt directory.')
    parser.add_argument('--output-path', type=str, help='Enter the PATH.kml directory.')
    args = parser.parse_args()
    print ("parse args complete")
    return args

if __name__ == '__main__':
    my_args = parseArgs()
    # read nmea file and save the coordinates
    output_list = []
    nmea_file = open(my_args.input_path, 'r')
    for nmea_line in nmea_file:
        if nmea_line.startswith('$GPRMC') or nmea_line.startswith('$GPGGA'):  # this line contains the information we need
            record = NmeaHandle.parse(nmea_line)
            s = str(record.longitude) + ',' + str(record.latitude) + ',' + '1' + '\n'
            output_list.append(s)
    nmea_file.close()
    # write all the coordinates into the .kml
    kml_file = open(my_args.output_path, 'w')
    kml_file.writelines(output_list)
    kml_file.close()
    print('finished all.')
    