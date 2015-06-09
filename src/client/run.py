#!/usr/bin/env python

import xml.etree.ElementTree as ET
from RainLib.ports.dropbox import DropBox
from RainLib.ports.googledrive import GoogleDrive
from RainLib.ports.box import Box
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from RainLib.file_event_handler import RainFileSystemEventHandler
from RainLib.utils import RainMetaFileAdapter
from RainLib.rainprotocol import RainPacketBuilder
from RainLib.raindrive import RainDrive
from threading import Thread
from socket import *
import logging
import time
import os
import sys


SUPPORTED_CLOUDS = [DropBox.name, GoogleDrive.name, Box.name]
DEFAULT_METAFILE = "<Rain><username>#username</username></Rain>"


def sync_thread(*args):
    rdrive = args[0]
    while True:
        time.sleep(5)
        rdrive.sync()


if __name__ == "__main__":
    if not os.path.exists("./metafile.xml"):
        # create default metafile.xml
        username = raw_input("Enter username:")
        mfdata = DEFAULT_METAFILE.replace("#username",username)
        f = open("./metafile.xml","wb")
        f.write(mfdata)
        f.close()

    mfa = RainMetaFileAdapter()
    mfa.set_metafile("./metafile.xml")
    if len(sys.argv) != 2:
        print "Usage : %s <watch_directory>" % sys.argv[0]
        exit()
    watch_dir = sys.argv[1]
    rdrive = RainDrive(mfa,watch_dir)
    print mfa.get_all_cloud_name()
    print rdrive.get_cloud_num()
    rdrive.login()
    rdrive.sync()

    print "=== Rain - Cloud Unification ==="
    print "1. Add Cloud Drives"
    print "2. Start Rain Daemon"
    choice = int(raw_input('select > '))

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
        mfa.dump()
        print 'Metafile updated'
    elif choice == 2:
        if rdrive.get_cloud_num() == 0:
            raise Exception('No cloud registered')
        sync_t = Thread(target=sync_thread, args=(rdrive,))
        sync_t.start()
        observer = Observer()
        event_handler = RainFileSystemEventHandler(rdrive,watch_dir)
        observer.schedule(event_handler, watch_dir, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
