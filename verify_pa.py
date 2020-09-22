import sys
import cryptography
import signxml as sx
from xml.etree.ElementTree import Element, SubElement, ElementTree
from lxml import etree
import os
import dateutil.parser
from datetime import datetime

MOCK_DGCA_CERTIFICATE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources", "dgca.cert")
MOCK_DGCA_PUBLIC_KEY = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Resources", "dgca_public.pem")

def verify_xml_signature(xml_file, certificate_path):
    """
    Verify the signature of a given xml file against a certificate
    :param xml_file: path to the xml file for verification
    :param certificate_path: path to the certificate to be used for verification
    :return: bool: the success of verification
    """

    tree = etree.parse(xml_file)
    # print (tree)
    root = tree.getroot()
    # print(root)
    with open(certificate_path) as f:
        certificate = f.read()
       
        try:
            verified_data = sx.XMLVerifier().verify(data=root, require_x509=True, x509_cert=certificate).signed_xml

            return True

        except cryptography.exceptions.InvalidSignature:

            return False


# def verify_xml_digest(key, ):

#     return 0

def verify_time(xml_file):
    """
    Verify the timeslot mentioned in the PA against current time
    :param xml_file: xml file for verification
    :return: bool: the success of verification
    """
    tree = etree.parse(xml_file)

    # print (tree)
    root = tree.getroot()
    # print(root)

    for params in root.iter('FlightParameters'):
        time_slot = (dateutil.parser.parse(params.get("flightEndTime")), dateutil.parser.parse(params.get("flightStartTime")))

    time_now = dateutil.parser.parse(datetime.now().astimezone().isoformat())

    if time_now < time_slot[0] and time_slot[1] < time_now:

        return  True

    else :

        return False



def verify_geofence( xml_file, true_geofence):
    """
    Verify the geofence mentioned in the PA against mission Geofence
    :param true_geofence: true geofence of the mission
    :param xml_file: xml file for verification
    :return: bool: the success of verification
    """
    tree = etree.parse(xml_file)
    # print (tree)
    root = tree.getroot()
    # print(root)

    pa_geofence = []
    for coordinate in root.iter('Coordinate'):
        # print(coordinate.get('latitude'))
        # print(coordinate.get('longitude'))
        pa_geofence.append([float(coordinate.get('longitude')), float(coordinate.get('latitude'))])

    if (len(true_geofence) == len(pa_geofence)) and all( coords in pa_geofence for coords in true_geofence):
        return True

    else :
        return False

def verify_pa(xml_file, certificate_path, true_geofence):
    xml_auth = verify_xml_signature(xml_file, certificate_path)
    geofence_auth = verify_geofence(xml_file, true_geofence)
    time_auth = verify_time(xml_file)

    if xml_auth and geofence_auth and time_auth:
        return True

    else:
        return False
    

if __name__ == "__main__":

    #Need to get proper geofence from the RPA
    true_geofence = [[77.609316, 12.934158], [77.609852, 12.934796],[77.610646, 12.934183], [77.610100, 12.933551], [77.609316,12.934158]]
    #  print("Geofence status : " + str(verify_geofence(true_geofence, sys.argv[1])))

    Auth = verify_pa(sys.argv[1], MOCK_DGCA_CERTIFICATE, true_geofence)
    
    print(Auth)

