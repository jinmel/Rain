from watchdog.events import FileSystemEventHandler


class RainFileSystemEventHandler(FileSystemEventHandler):
    #TODO: implement this according to metafile.xml

    def __init__(self, rain_drive):
        self.rain_drive = rain_drive

    def on_created(self, event):
        if not event.is_directory:
            print 'create file' + event.src_path
            self.rain_drive.new_file(event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            print 'delete file' + event.src_path
            self.rain_drive.remove_file(event.src_path)






