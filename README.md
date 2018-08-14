# MOBIB Card Reader - 2017 Edition

Read data stored on your MOBIB card (STIB/MIVB, SNCB/NMBS, TEC).

My objective with this project is to:

- get rid of this bloated Tk GUI and have a simple CLI tool
- use valid APDUs for recent smartcards and adapt parsing code
- rewrite parsing code in a Pythonic way
- clean install & packaging

Supports both contacted and contactless smart card readers.

# Installation

## on Linux

```
apt-get install libpcsclite1 libpcsclite1-dev python python-virtualenv
virtualenv ve
source ve/bin/activate
pip install -r requirements.txt
```

## on Mac OS X

TODO

## on Microsoft Windows

TODO

# Background Information

If you want to know about new APDUs and format, check the [documentation](Documentation.md)

Two scripts are available at the moment:

- extract.py that reads owner details and last three known locations
- test.py that emulates commands sent by the STIB plugin

# Credits

Initial research project was performed by Tania Marting <tania.martin@uclouvain.be> and Jean-Pierre Szikora <jean-pierre.Szikora@uclouvain.be> from UCL GIS. All credits goes to them for their amazing work with this :)

# Original License

(c) 2009 MOBIB Extractor project. This software is provided 'as-is',
without any express or implied warranty. In no event will the authors be held
liable for any damages arising from the use of this software.

Permission is granted to anyone to use this software for any purpose,
including commercial applications, and to alter it and redistribute it
freely, subject to no restriction.
