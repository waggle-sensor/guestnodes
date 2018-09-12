#!/usr/bin/env python3
import waggle.pipeline
import time
import sys
import os
from coresense import create_connection, NoPacketError


device = os.environ.get('CORESENSE_DEVICE', '/dev/waggle_coresense')

class CoresensePlugin(waggle.pipeline.Plugin):

    plugin_name = 'coresense'
    plugin_version = '3'

    def run(self):
        while True:
          try:
            print('Connecting to device: {}'.format(device), flush=True)

            with create_connection(device) as conn:
                print('Connected to device: {}'.format(device), flush=True)

                while True:
                    message = conn.recv()
                    if message is not None:
                        print('Received frame.', flush=True)
                        self.send(sensor='frame', data=message.frame)
                    time.sleep(5)
          except NoPacketError:
              print('No packets are being received. Resetting the serial connection...')

if os.path.exists(device):
    plugin = CoresensePlugin.defaultConfig()
    plugin.run()
else:
    exit(1)