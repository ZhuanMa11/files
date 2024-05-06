import time
from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler

class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            print(f"File {event.src_path} has been modified")

if __name__ == "__main__":
    # 监控的目录
    monitored_dir = "/data"

    # 创建监控器
    event_handler = FileChangeHandler()
    observer = PollingObserver()
    observer.schedule(event_handler, monitored_dir, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
