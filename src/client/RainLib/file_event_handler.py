from watchdog.events import FileSystemEventHandler
from os.path import relpath


class RainFileSystemEventHandler(FileSystemEventHandler):
    #TODO: implement this according to metafile.xml

    def __init__(self, rain_drive,watch_dir):
        self.rain_drive = rain_drive
        self.watch_dir = watch_dir

    def on_created(self, event):
        if not event.is_directory and not self.rain_drive.is_locked():
            event_path = relpath(event.src_path,self.watch_dir)
            self.rain_drive.new_file(event_path)

    def on_deleted(self, event):
        if not event.is_directory and not self.rain_drive.is_locked():
            event_path = relpath(event.src_path,self.watch_dir)
            self.rain_drive.remove_file(event_path)
