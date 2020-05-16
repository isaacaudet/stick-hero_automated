from ppadb.client import Client
from PIL import Image
import statistics
import numpy
import os
import time
import threading
import logging
import concurrent.futures
from http_touch import AndroidTouch

touch = AndroidTouch()
logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s', datefmt='%M:%S', level=logging.INFO)

while True:
    adb = Client(host='127.0.0.1', port=5037)
    devices = adb.devices()

    if len(devices)  == 0:
        print('no device attached')
        quit()

    device = devices[0]

    image = device.screencap()

    with open('screen.png', 'wb') as f:
        f.write(image)

    image = Image.open('screen.png')
    image = numpy.array(image)

    pixels = [list(i[:3]) for i in image[1740]]
    transitions = []
    ignore = True
    black = True
    red = True
    cherry = []

    for i, pixel in enumerate(pixels):
        r, g, b = [int(i) for i in pixel]
        # if something
        # cherry = i
        if ignore and (r+g+b) != 0:
            continue
        
        ignore = False

        if black and (r+g+b) != 0:
            black = not black
            transitions.append(i)
            continue

        if not black and (r+g+b) == 0:
            black = not black
            transitions.append(i)
            continue
        
        if red and 251 < (r+g+b) < 300:
            red = not red
            cherry.append(i)
            continue
            
        if not red and (r+g+b) > 400:
            red = not red
            cherry.append(i)
            continue
    
    print(cherry)

    # calculate distance to perfect vault
    start, target1, target2 = transitions
    gap = target1 - start
    target = target2 - target1 
    distance = (gap + target / 2) * .98

    # cherry
    if len(cherry) >= 2:
        cherry_target = statistics.mean(cherry) - start
        cherry_possible = True
        print(cherry_target)
        print(cherry_possible)
    else:
        cherry_possible = False
        
    logging.info('before adb swipe')
    device.shell(f'input touchscreen swipe 500 500 500 500 {int(distance)}')
    logging.info('after adb swipe')

    if cherry_possible:
        logging.info('before double tap')
        touch.double_tap()
        logging.info('after double tap')

    print()
    print()
    time.sleep(2.7)
