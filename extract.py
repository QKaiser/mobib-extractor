#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# (c) 2009 MOBIB Extractor project. This software is provided 'as-is',
# without any express or implied warranty. In no event will the authors be held
# liable for any damages arising from the use of this software.
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to no restriction.
#
# Technical remarks and questions can be addressed to
# <tania.martin@uclouvain.be>
# <jean-pierre.Szikora@uclouvain.be>
#


import re
import sys
import types
import time
import datetime
import string
import os
import csv
from smartcard.System import readers
from smartcard.util import toHexString, toBytes
from smartcard.Exceptions import NoCardException

##################
## Informations ##
##################

numero = ['0','1','2','3','4','5','6','7','8','9']

###############
## Fonctions ##
###############


## Hexadecimal to binary
def hex_to_bin(h):
    return bin(int(h,16))[2:].zfill(len(h)*4)

## Binary to alphabet with offset t (on 5 bits)
def bin_to_alphabet (b, t):
    res = ''
    for i in range(t, len(b), 5):
        a = int(b[i:i+5], 2)
	res += ' ' if (a > 26 or a < 1) else chr(64+a)
    return res

## Binary to number (on the total length)
def bin_to_number (b):
    return str(int(b,2))

## Binary to number with offset t (on 4 bits)
def bin_to_number_dec (b, t):
    res = ''
    for i in range(t,len(b), 4):
        a = int(b[i:i+4], 2)
        res += "x" if a > 9 else str(a)
    return res

## Find a date from the 1st January 1997
def find_date (x):
	init = datetime.date(1997, 1, 1)
	diff = datetime.timedelta(days=x)
	d = init + diff
	if d == init:
		return "-"
	else:
		return d.strftime("%d/%m/%Y")

## Find an hour
def find_hour (x):
	min = str(int(x)%60)
	if min in numero:
		min = '0'+min
	return (int(x)/60, min)	


#########################################################################
## Find Name + Birthdate + Post code + Card number + Remaining travels ##
#########################################################################

def analyze_holder(raw_holder1, raw_holder2):
    # raw_holder1 has :
    # - bytes 0-1 : unknown data
    # - bytes 2-11 : the card number
    # - bytes 12-20 : unknown data
    # - bytes 21-24 : the birthday
    # - bytes 24-28 : the begining of the name
    # raw_holder2 has the end of the name

    ## Name

    ## Card number
    hexa_card = ''
    for i in range(2, 12):
	hexa_card = hexa_card + raw_holder1[i]
    hexa_card = hexa_card + raw_holder1[12][0]

    num_card = bin_to_number_dec(hex_to_bin(hexa_card),2) # offset = 2
    print "\033[1mCard number:\033[0m %s"%num_card

    hexa_type = raw_holder1[25][0]
    bin_type = hex_to_bin(hexa_type)[0:2]
    if bin_type == '01':
    	gender = 'Mr'
    elif bin_type == '10':
    	gender = 'Mrs'
    else:
        gender = None

    if gender is not None:
        hexa_name = raw_holder1[25][1]
        for i in range(26, 29):
            hexa_name = hexa_name + raw_holder1[i]
        for a in (raw_holder2):
            hexa_name = hexa_name + a
        bin_name = ''
        for i in range(0,len(hex_to_bin(hexa_name))):
	    bin_name = bin_name + hex_to_bin(hexa_name)[i]
        name = bin_to_alphabet(bin_name,1) # offset = 1

        print "\033[1mName:\033[0m %s %s"%(gender,name)

        ## Birthday
        birthday = raw_holder1[24] + " / " + raw_holder1[23] + " / " + raw_holder1[21] + raw_holder1[22]
        print "\033[1mBirthday:\033[0m %s"%birthday
    else:
        print "\033[1mName:\033[0m MOBIB BASIC"


def analyze_envholder(raw_envholder):
    # Zip code
    # TODO: zip code location seems to have changed. I think it is there but I
    # need another card to confirm my hypothesis.
    hexa_zipcode = raw_envholder[26] + raw_envholder[27] + raw_envholder[28][0]
    zipcode = bin_to_number(hex_to_bin(hexa_zipcode)[4:17])
    print "\033[1mZip code:\033[0m %s"%zipcode


def analyze_counter(raw_counter):
    ## Remaining travels
    hexa_counter = []
    for i in range(0,26,3):
        hexa_counter.append(raw_counter[i] + raw_counter[i+1] + raw_counter[i+2])
    c = int(0)
    for i in range(len(hexa_counter)):
        c = c + int(bin_to_number(hex_to_bin(hexa_counter[i])))

    ## Contract type
    if c == 12034:
        c = "-"
	contract_type = "Day subscription"
    else:
    	contract_type = "UNKNOWN"
    print "\033[1mContract type:\033[0m %s"%contract_type
    print "\033[1mRemaining travels:\033[0m %s"%c


def analyze_logs(raw_logs):
    ## Card total validations counter
    hexa_cp_total_log = ['','','']
    cp_total_log = ['','','']
    for i in range(3):
    	hexa_cp_total_log[i] = raw_logs[i][17] + raw_logs[i][18] + raw_logs[i][19] + raw_logs[i][20][0] 
    for i in range(3):
	r = hex_to_bin(hexa_cp_total_log[i])
	cp_total_log[i] = bin_to_number(r[3:len(r)-2])
    ## Travel connection counter
    hexa_cp_corresp_log = ['','','']
    cp_corresp_log = ['','','']
    for i in range(3):
    	hexa_cp_corresp_log[i] = raw_logs[i][20] + raw_logs[i][21] + raw_logs[i][22] + raw_logs[i][23][0]
    for i in range(3):
    	r = hex_to_bin(hexa_cp_corresp_log[i])
	cp_corresp_log[i] = bin_to_number(r[3:len(r)-2])

    ## Card validation date
    hexa_date_valid = ['','','']
    date_valid = ['','','']
    for i in range(3):
	hexa_date_valid[i] = raw_logs[i][0][1] + raw_logs[i][1] + raw_logs[i][2][0]
    for i in range(3):
	tmp_datev_bin = hex_to_bin(hexa_date_valid[i])
	date_valid[i] = find_date(int(bin_to_number(tmp_datev_bin[2:len(tmp_datev_bin)])))

    ## Card validation date of the first transit travel
    hexa_date_transit = ['','','']
    date_transit = ['','','']
    for i in range(3):
	hexa_date_transit[i] = raw_logs[i][23] + raw_logs[i][24]
    for i in range(3):
    	tmp_datet_bin = hex_to_bin(hexa_date_transit[i])
	date_transit[i] = find_date(int(bin_to_number(tmp_datet_bin[2:len(tmp_datet_bin)])))

    ## Card validation hour
    hexa_heure_valid = ['','','']
    heure_valid = ['','','']
    for i in range(3):
	hexa_heure_valid[i] = raw_logs[i][2][1] + raw_logs[i][3]
    for i in range(3):
	tmp_heurev_bin = hex_to_bin(hexa_heure_valid[i])
	heure_valid[i] = find_hour(int(bin_to_number(tmp_heurev_bin[0:len(tmp_heurev_bin)-1])))	

    ## Card validation hour of the first transit travel
    hexa_heure_transit = ['','','']
    heure_transit = ['','','']
    for i in range(3):
	hexa_heure_transit[i] = raw_logs[i][25] + raw_logs[i][26][0]
    for i in range(3):
	tmp_heuret_bin = hex_to_bin(hexa_heure_transit[i])
	heure_transit[i] = find_hour(int(bin_to_number(tmp_heuret_bin[0:len(tmp_heuret_bin)-1])))	

    ## Transit or not ?
    transit = ['','','']
    for i in range(3):
	if raw_logs[i][6][0] == '6':
		transit[i] = "YES"
	else:
		transit[i] = "NO"

    ## Number of persons travelling
    nb_persons = ['','','']
    for i in range(3):
    	bin_nb_persons = hex_to_bin(raw_logs[i][6][1] + raw_logs[i][7][0])[0:5]
	nb_persons[i] = bin_to_number(bin_nb_persons)

    ## String Logs
    string_logs = ['','','']
    for i in range(3):
    	tmp_hexa = ''
        for j in range(29):
            tmp_hexa = tmp_hexa + raw_logs[i][j]
	string_logs[i] = hex_to_bin(tmp_hexa)

    ## Station
    type_transport = ['','','']
    ligne = ['','','']
    station = ['','','']
    direction = ['','','']
    coordx = ['','','']
    coordy = ['','','']
    for i in range(3):
	# if the transport is a metro
        if string_logs[i][99:104] == '00000':
            if date_valid[i] == "-":
	        type_transport[i] = "-"
	        ligne[i] = "0"
	        station[i] = "No info"
	        direction[i] = "No info"
	        coordx[i] = "-"
	        coordy[i] = "-"
	    else:
	        type_transport[i] = 'Metro'
	        reader = csv.reader(open("Database/metro_new.csv", "rb"))
	        # Special case: a reader at the station Gare Centrale does not have the correct UID !!!!
	        if string_logs[i][104:131] == '000111001101011011011101010':
		    ligne[i] = "1A/1B"
		    station[i] = "Gare Centrale"
		    direction[i] = "No info"
		    coordx[i] = "1223"
		    coordy[i] = "1347"
		else:
		    for r in reader:
		        if string_logs[i][104:110] == r[1] and string_logs[i][110:114] == r[2] and string_logs[i][114:121] == r[3]:
			    ligne[i] = r[4]
			    station[i] = r[5]
			    direction[i] = "No info"
			    coordx[i] = r[6]
			    coordy[i] = r[7]
			# if the transport is a premetro
	elif string_logs[i][99:104] == '00111':
	    type_transport[i] = 'Premetro'
	    reader = csv.reader(open("Database/Metro.csv", "rb"))
	    for r in reader:
	        if string_logs[i][104:110] == r[1] and string_logs[i][110:114] == r[2] and string_logs[i][114:121] == r[3]:
		    ligne[i] = r[4]
		    station[i] = r[5]
		    direction[i] = "No info"
		    coordx[i] = r[6]
		    coordy[i] = r[7]
	# if the transport is a tramway
	elif string_logs[i][99:104] == '10110':
	    type_transport[i] = 'Tramway'
	    ligne[i] = "No info"
	    station[i] = "No info"
	    direction[i] = "No info"
	    coordx[i] = "-"
	    coordy[i] = "-"
	# if the transport is a bus
	elif string_logs[i][99:104] == '01111':
	    type_transport[i] = 'Bus'
	    reader = csv.reader(open("Database/bus_new.csv", "rb"))
	    for r in reader:
	    	if bin_to_number(string_logs[i][92:99]) == r[0] and bin_to_number(string_logs[i][71:83]) == r[5]:
	    	    ligne[i] = r[0]
		    station[i] = r[4] 
		    direction[i] = r[1]
		    coordx[i] = r[2]
		    coordy[i] = r[3]
		    break
		else:
		    if bin_to_number(string_logs[i][92:99]) == '0':
		        ligne[i] = "Unknown"
		    else:
		        ligne[i] = bin_to_number(string_logs[i][92:99])
			station[i] = "No info" 
			direction[i] = "No info"
			coordx[i] = "-"
			coordy[i] = "-"
        # if the transport is unknown
	else:
	    type_transport[i] = "Unknown"
	    ligne[i] = "No info"
	    station[i] = "No info"
	    direction[i] = "No info"
	    coordx[i] = "-"
	    coordy[i] = "-"


    print "\n\033[1mLast known locations:\033[0m\n"
    print "\033[4mTransport\tLine\tStation\t\tTime\t\t\t\tCoords\033[0m"
    for i in range(0,3):
        print "%s\t\t%s\t%s\t\t%s %s:%s\t\t%s;%s" % (type_transport[i], ligne[i], station[i], date_valid[i], heure_valid[i][0], heure_valid[i][1], coordx[i], coordy[i])
    print
r=readers()
if not len(r):
    print "[!] No reader detected"
    sys.exit(-1)

print "\033[92mSmartcard reader detected.\033[0m\nConnecting to \033[4m%s\033[0m...\n" % r[0]
try:
    connection = r[0].createConnection()
    connection.connect()
except NoCardException as e:
    print "[!] Connect a card, dummy."
    sys.exit(-1)

s = "00 A4 04 00 0E 31 54 49 43 2E 49 43 41 D0 56 00 01 91 01"
select_command = toBytes(s)
data,sw1,sw2 = connection.transmit(select_command)

s = "00 B2 01 3C 1D"
select_command = toBytes(s)
data,sw1,sw2 = connection.transmit(select_command)
raw_envholder = toHexString(data).split(' ')

s = "00 B2 01 CC 1D"
select_command = toBytes(s)
data,sw1,sw2 = connection.transmit(select_command)
raw_counter = toHexString(data).split(' ')
raw_logs = []
# EvLog1
s = "00 B2 01 BC 1D"
select_command = toBytes(s)
data,sw1,sw2 = connection.transmit(select_command)
raw_logs.append(toHexString(data).split(' '))

# EvLog2
s = "00 B2 02 BC 1D"
select_command = toBytes(s)
data,sw1,sw2 = connection.transmit(select_command)
raw_logs.append(toHexString(data).split(' '))

# EvLog3
s = "00 B2 03 BC 1D"
select_command = toBytes(s)
data,sw1,sw2 = connection.transmit(select_command)
raw_logs.append(toHexString(data).split(' '))

s = "00 A4 04 00 0B A0 00 00 02 91 D0 56 00 01 90 01"
select_command = toBytes(s)
data,sw1,sw2 = connection.transmit(select_command)
s = "00 B2 01 E4 1D"
select_command = toBytes(s)
data,sw1,sw2 = connection.transmit(select_command)
raw_holder1 = toHexString(data).split(' ')

s = "00 B2 02 E4 1D"
select_command = toBytes(s)
data,sw1,sw2 = connection.transmit(select_command)
raw_holder2 = toHexString(data).split(' ')

analyze_holder(raw_holder1, raw_holder2)
# if not basic card
if len(raw_envholder) > 1:
    analyze_envholder(raw_envholder)
analyze_counter(raw_counter)
analyze_logs(raw_logs)
