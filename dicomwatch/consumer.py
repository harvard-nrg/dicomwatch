import os
import glob
import shutil
import logging
from pubsub import pub
from pathlib import Path
from watchdog.observers.polling import PollingObserver
from watchdog.events import PatternMatchingEventHandler


logger = logging.getLogger('consumer')

class Consumer:
    def __init__(self, directory):
        self._directory = directory
        self._observer = PollingObserver(timeout=1)
        self._observer.schedule(
            DicomHandler(
                patterns=['*.tar.gz'],
                ignore_directories=True
            ),
            directory
        )

    def start(self):
        logger.info('starting watchdog observer')
        self._directory.mkdir(parents=True, exist_ok=True)
        self._observer.start()

    def forever(self):
        self.start()
        self._observer.join()

class DicomHandler(PatternMatchingEventHandler):
    def on_created(self, event):
        path = Path(event.src_path)
        pub.sendMessage('incoming', path=path)

    def on_moved(self, event):
        path = Path(event.dest_path)
        pub.sendMessage('incoming', path=path)
