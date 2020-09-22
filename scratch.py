import sys
import cryptography
import signxml as sx
from xml.etree.ElementTree import Element, SubElement, ElementTree
from lxml import etree
import os
import collections
import dateutil.parser
from datetime import datetime

tree = etree.parse('resources/signed_permission_artefact_1.xml')

# print (tree)
root = tree.getroot()
# print(root)

for params in root.iter('FlightParameters'):
    time_slot = (dateutil.parser.parse(params.get("flightEndTime")), dateutil.parser.parse(params.get("flightStartTime")))

time_now = dateutil.parser.parse(datetime.now().astimezone().isoformat())
time_now2 = dateutil.parser.parse(datetime.now().astimezone().isoformat())

print(time_now == time_now2)

if time_slot[0] > time_now > time_slot[1]:
    print(True)

else :
    print(False)
# print(type(t
# ime_slot))
# print(time_slot[0])    

# true_geofence = [[77.609316, 12.934158],[77.610646, 12.934183], [77.610100, 12.933551], [77.609316,12.934158], [77.609852, 12.934796]]

# if (len(true_geofence) == len(pa_geofence)) and all( coords in pa_geofence for coords in true_geofence):
#     print(True)

# else :
#     print(False)
