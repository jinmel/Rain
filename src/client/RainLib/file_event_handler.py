from watchdog.events import FileSystemEventHandler

class RainFileSystemEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        pass

    def on_deleted(self, event):
        pass

    def on_modified(self, event):
        pass

    def on_moved(self, event):
        pass

    def on_any_event(self, event):
        pass