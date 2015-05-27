#!/usr/bin/env python

import xml.etree.ElementTree as ET
from RainLib.ports.dropbox import DropBox
from RainLib.ports.googledrive import GoogleDrive
from RainLib.ports.box import Box
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from RainLib.file_event_handler import RainFileSystemEventHandler
from RainLib.utils import RainMetaFileAdapter
from RainLib.raindrive import RainDrive
import logging
import time

SUPPORTED_CLOUDS = [DropBox.name, GoogleDrive.name, Box.name]

if __name__ == "__main__":
    #TODO: Read metafile.xml initialize cloud drive instances
    mfa = RainMetaFileAdapter('metafile.xml')

    print "=== Rain - Cloud Unification ==="
    print "1. Add Cloud Drives"
    print "2. Start Rain Daemon"
    print "3. Debug"
    choice = int(raw_input('select > '))
    #choice = 3

    if choice == 1:
        #TODO: open meta file and check what clouds are registered
        cloud_registered = mfa.get_all_cloud_name()
        cloud_not_registered = list(set(SUPPORTED_CLOUDS) - set(cloud_registered))
        menu = {}
        for i in xrange(len(cloud_not_registered)):
            menu[i + 1] = cloud_not_registered[i]
        print "Select the cloud drive you want to add"
        for k, v in menu.iteritems():
            print str(k) + '. ' + v

        choice = int(raw_input('select > '))
        #Authentification for each clouds
        access_token = ''
        if menu[choice] == DropBox.name:
            access_token = DropBox.auth()
        elif menu[choice] == GoogleDrive.name:
            access_token = GoogleDrive.auth()
        elif menu[choice] == Box.name:
            access_token = Box.auth()

        mfa.add_cloud(menu[choice], access_token)
        mfa.write()
        print 'Metafile updated'
    elif choice == 2:
        rdrive = RainDrive(mfa)
        cloud_names = mfa.get_all_cloud_name()
        for cloud_name in cloud_names:
            if cloud_name == DropBox.name:
                rdrive.add_cloud(DropBox(mfa.get_cloud_access_token(cloud_name)))
            elif cloud_name == GoogleDrive.name:
                rdrive.add_cloud(GoogleDrive(mfa.get_cloud_access_token(cloud_name)))
            elif cloud_name == Box.name:
                rdrive.add_cloud(Box(mfa.get_cloud_access_token(cloud_name)))
            else:
                raise Exception('Unknown cloud service name: ' + cloud_name)

        observer = Observer()
        event_handler = RainFileSystemEventHandler(rdrive)
        observer.schedule(event_handler, ".", recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
    elif choice == 3:
        mfa.add_file('DropBox', './data3.txt', '/Rain/data3.txt', '1024')
        print mfa.get_local_file_list('DropBox')
        print mfa.get_remote_file_list('DropBox')
        print mfa.get_cloud_name_by_local_filename('./data3.txt')
        print mfa.get_all_cloud_name()
        print mfa.get_file_map('DropBox')
