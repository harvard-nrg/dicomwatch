import pydicom
import logging
from pubsub import pub
from pynetdicom import AE, StoragePresentationContexts

logger = logging.getLogger('sender')

class Sender:
    def __init__(self, hostname, port, ae_title='ANY-SCP'):
        self._hostname = hostname
        self._ae_title = ae_title
        self._port = port
        self._ae = AE()
        self._ae.requested_contexts = StoragePresentationContexts
        self._association = None
        pub.subscribe(self.listener, 'send')

    def associate(self):
        if self._association and self._association.is_established:
            return
        logger.info(f'establishing association to host={self._hostname}, port={self._port}, ae_title={self._ae_title}')
        self._association = self._ae.associate(
            self._hostname,
            self._port,
            ae_title=self._ae_title
        )
        self._association.network_timeout = None
        self._association.acse_timeout = None
        self._association.dimse_timeout = None

    def listener(self, ds):
        self.associate()
        logger.info(f'sending series={ds.SeriesNumber}, instance={ds.InstanceNumber}')
        status = self._association.send_c_store(ds)
        if status:
            logger.info(f'c-store succeeded')
        else:
            raise StoreSCUError(f'c-store failed')

class StoreSCUError(Exception):
    pass
