#!/usr/bin/env python
import csv

stops = []
bus = []

if __name__ == "__main__":
    outfile = open("bus_new.csv", "wb")
    outfile.write('"Bus","Direction","coord_x","coord_y","Arret","Code"\n')
    with open("Bus.csv") as f:
        lines = csv.reader(f, delimiter=',', quotechar='"')
        next(lines, None)
        for line in lines:
            bus.append(line)
    with open("stops.txt") as f:
        for line in f.readlines()[1:]:
            stops.append(line.strip().split(","))

    for b in bus:
        found = False
        for stop in stops:
            if b[5] == stop[0]:
                print "[+] Matched %s with %s " % (b[4], stop[2])
                found = True
                outfile.write('"%s","%s","%s","%s","%s","%s"\n' % (b[0], b[1], stop[4].replace(" ", ""), stop[5].replace(" ", ""), b[4], b[5]))
        if not found:
            print "[!] No match for %s" % (b[4])
            outfile.write('"%s","%s","0.0","0.0","%s","%s"\n' % (b[0], b[1], b[4], b[5]))


