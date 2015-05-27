from watchdog.events import FileSystemEventHandler


class RainFileSystemEventHandler(FileSystemEventHandler):
    #TODO: implement this according to metafile.xml

    def __init__(self, rain_drive):
        self.rain_drive = rain_drive

    def on_created(self, event):
        print 'create', event.src_path
        pass

    def on_deleted(self, event):
        print 'delete', event.src_path
        pass

    def on_modified(self, event):
        print 'modify', event.src_path
        pass

    def on_moved(self, event):
        print 'move', event.src_path
        pass

    def on_any_event(self, event):
        print event.event_type
        pass







