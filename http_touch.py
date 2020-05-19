import requests
import json
import math
import logging
from ppadb.client import Client


logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s', datefmt='%M:%S', level=logging.INFO)


class AndroidTouch:
    def __init__(self):
        # super().__init__()
        self.ip = 'http://localhost:9889'
        
        # touch types
        self.DOUBLE_TAP = [
            {"type": "down", "contact": 0, "x": 500, "y": 500, "pressure": 50},
            {"type": "commit"},
            {"type": "up", "contact": 0},
            {"type": "commit"},
            {"type": "delay", "value": 10},
            {"type": "down", "contact": 0, "x": 525, "y": 525, "pressure": 50},
            {"type": "commit"},
            {"type": "up", "contact": 0},
            {"type": "commit"},
        ]
        
        self.SINGLE_TAP = [
            {"type": "down", "contact": 0, "x": 100, "y": 100, "pressure": 50},
            {"type": "commit"},
            {"type": "up", "contact": 0},
            {"type": "commit"}
        ]
        
        self.SWIPE = [
            {"type": "down", "contact": 0, "x": 100, "y": 100, "pressure": 50},
            {"type": "commit"},
            {"type": "move", "contact": 0, "x": 100, "y": 400, "pressure": 50},
            {"type": "commit"},
            {"type": "up", "contact": 0},
            {"type": "commit"}
        ]


    def send_command(self, command):
        req = requests.post(self.ip, data=json.dumps(command))

    def double_tap(self):
        req = requests.post(self.ip, data=json.dumps(self.DOUBLE_TAP))

    def single_tap(self):
        req = requests.post(self.ip, data=json.dumps(self.SINGLE_TAP))

    def swipe_tap(self):
        req = requests.post(self.ip, data=json.dumps(self.SWIPE))
def main():
    logging.info('before adb')

    adb = Client(host='127.0.0.1', port=5037)
    devices = adb.devices()
    logging.info('after adb')

    if len(devices)  == 0:
        print('no device attached')
        quit()

    device = devices[0]
    
    
    logging.info('before adb swipe')
    device.shell('input touchscreen swipe 500 500 500 500 10')
    logging.info('after adb swipe')
    
    logging.info('before adb swipe2')
    device.shell('input touchscreen swipe 200 200 200 200 10')
    logging.info('after adb swipe2')
    
    logging.info('before touch')

    # touch = AndroidTouch()
    
    # logging.info('b double')
    # touch.double_tap()
    # logging.info('a double')

    # logging.info('b single')
    # touch.double_tap()
    # logging.info('a single')

    # logging.info('b swipe')
    # touch.double_tap()
    # logging.info('a swipe')
if __name__ == "__main__":
    main()
