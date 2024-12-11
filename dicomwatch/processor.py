import time
import tarfile
import logging
import pydicom
from pubsub import pub
from pynetdicom import AE
from pydicom.errors import InvalidDicomError
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger('processor')

class Timer(object):
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.tstart = time.time()

    def __exit__(self, type, value, traceback):
        elapsed = time.time() - self.tstart
        logger.info(f'{self.name} elapsed: {elapsed}')

class Processor:
    def __init__(self):
        pub.subscribe(self.listener, 'incoming')
        self.pool = ThreadPoolExecutor(max_workers=1)

    def listener(self, path):
        logger.info(f'calling self.process with {path}')
        self.pool.submit(self.process, path)

    def process(self, path):
        with Timer('dicom-send'):
            logger.info(f'opening file {path}')
            with tarfile.open(path) as tar:
                for member in tar.getmembers():
                    if not member.isfile():
                        continue
                    logger.info(f'inspecting {member.name}')
                    f = tar.extractfile(member)
                    try:
                        ds = pydicom.dcmread(f)
                        logger.info(f'publishing message to send topic with data set {member.name}')
                        pub.sendMessage('send', ds=ds)
                    except InvalidDicomError:
                        logger.debug(f'not dicom {member.name}')
                        pass
                logger.info(f'done processing {path}')
            self.finish(path)

    def finish(self, path):
        target = Path(path.parent, 'COMPLETE', path.name)
        target.parent.mkdir(exist_ok=True)
        logger.info(f'renaming {path} to {target}')
        path.rename(target)
