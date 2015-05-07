#!/usr/bin/env python

import xml.etree.ElementTree as ET
import RainLib.clouddrive


META_FILENAME = 'metafile.xml'
SUPPORTED_CLOUDS = ['DropBox', 'Box', 'Google Drive']

if __name__ == "__main__":
    print "=== Rain - Cloud Unification ==="
    print "1. Add Cloud Drives"
    print "2. Start Rain Daemon"
    choice = raw_input('select>')

    if choice == '1':
        #TODO: open meta file and check what clouds are registered
        tree = ET.parse(META_FILENAME)
        root = tree.getroot()
        cloud_registered = []
        for cloud in root.findall('cloud'):
            name = cloud.find('name')
            cloud_registered.append(name.text)

        cloud_remaining = list(set(SUPPORTED_CLOUDS).difference(set(cloud_registered)))

        menu = {}
        for i in xrange(len(cloud_remaining)):
            menu[i+1] = cloud_remaining[i]
        print "Select the cloud drive you want to add"
        for k, v in menu.iteritems():
            print str(k) + '. ' + v

        choice = raw_input('select>')
        #Authentification for each clouds



