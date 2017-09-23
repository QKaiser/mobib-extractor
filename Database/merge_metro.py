#!/usr/bin/env python
import csv

stops = []
metros = []

if __name__ == "__main__":
    outfile = open("metro_new.csv", "wb")
    outfile.write('"Type","Zone","Sous-zone","Station","Ligne","Arret","Coord_x","Coord_y"\n')
    with open("Metro.csv") as f:
        lines = csv.reader(f, delimiter=',', quotechar='"')
        next(lines, None)
        for line in lines:
            metros.append(line)
    with open("stops.txt") as f:
        for line in f.readlines()[1:]:
            stops.append(line.strip().split(","))

    #"00000","000111","0011","1000001","1B","Alma","2255","1295"
    for metro in metros:
        found = False
        #8142,,"ALMA",,  50.849991,   4.453400,,,0
        for stop in stops:
            if not found and metro[5].upper() == stop[2].replace('"', ''):
                print "[+] Matched %s with %s " % (metro[5], stop[2])
                found = True
                outfile.write('"%s","%s","%s","%s","%s","%s","%s","%s"\n' % (metro[0], metro[1], metro[2], metro[3], metro[4], metro[5], stop[4].replace(" ", ""), stop[5].replace(" ", "")))
        if not found:
            print "[!] No match for %s" % (metro[5])
            outfile.write('"%s","%s","%s","%s","%s","%s",0.0","0.0"\n' % (metro[0], metro[1], metro[2], metro[3], metro[4], metro[5]))
