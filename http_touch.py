import requests
import json
import math
import logging


logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s', datefmt='%M:%S', level=logging.INFO)


class AndroidTouch:
    def __init__(self):
        # super().__init__()
        self.DOUBLE_TAP = [
            {"type": "down", "contact": 0, "x": 500, "y": 500, "pressure": 50},
            {"type": "commit"},
            {"type": "up", "contact": 0},
            {"type": "commit"},
            {"type": "delay", "value": 100},
            {"type": "down", "contact": 0, "x": 525, "y": 525, "pressure": 50},
            {"type": "commit"},
            {"type": "up", "contact": 0},
            {"type": "commit"},
        ]

    def send_command(self, command):
        req = requests.post("http://localhost:9889", data=json.dumps(command))

    def double_tap(self):
        req = requests.post("http://localhost:9889", data=json.dumps(self.DOUBLE_TAP))


def main():
    touch = AndroidTouch()
    logging.info('before')
    touch.double_tap
    logging.info('after')


if __name__ == "__main__":
    main()
