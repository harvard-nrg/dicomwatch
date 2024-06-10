import pydicom
import tarfile
import logging
from pubsub import pub
from pynetdicom import AE
from pydicom.errors import InvalidDicomError

logger = logging.getLogger('processor')

class Processor:
    def __init__(self):
        pub.subscribe(self.listener, 'incoming')
    
    def listener(self, path):
        logger.info(f'opening {path} ...this could take a while')
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
