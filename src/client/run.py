#!/usr/bin/env python

import xml.etree.ElementTree as ET
from RainLib.ports import *
import daemon


META_FILENAME = 'metafile.xml'
SUPPORTED_CLOUDS = [dropbox.__name__, box.__name__, googledrive.__name__]

if __name__ == "__main__":
    #TODO: Read metafile.xml initialize cloud drive instances

    dropbox_instance = dropbox.DropBox()
    box_instance = box.Box()
    googledrive_instance = googledrive.GoogleDrive()

    print "=== Rain - Cloud Unification ==="
    print "1. Add Cloud Drives"
    print "2. Start Rain Daemon"
    choice = raw_input('select>')

    if choice == '1':
        #TODO: open meta file and check what clouds are registered
        metafile = ET.parse(META_FILENAME)
        root = metafile.getroot()
        cloud_registered = []
        for cloud in root.findall('cloud'):
            name = cloud.find('name')
            cloud_registered.append(name.text)

        cloud_not_registered = list(set(SUPPORTED_CLOUDS).difference(set(cloud_registered)))

        menu = {}
        for i in xrange(len(cloud_not_registered)):
            menu[i + 1] = cloud_not_registered[i]
        print "Select the cloud drive you want to add"
        for k, v in menu.iteritems():
            print str(k) + '. ' + v

        choice = int(raw_input('select>'))
        #Authentification for each clouds
        access_token = ''
        if menu[choice] == dropbox.__name__:
            access_token = dropbox_instance.auth()
        elif menu[choice] == googledrive.__name__:
            access_token = googledrive_instance.auth()
        elif menu[choice] == box_instance.__name__:
            access_token = box_instance.auth()

        new_cloud = ET.SubElement(metafile.getroot(), 'cloud')
        ET.SubElement(new_cloud, 'name').text = menu[choice]
        ET.SubElement(new_cloud, 'access_token').text = access_token
        metafile.write(META_FILENAME)
        print 'Metafile updated'
    elif choice == '2':
        pass


