from ppadb.client import Client
from PIL import Image
import statistics
import numpy
import os
import time
import logging
import requests
import json
import math

logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s', datefmt='%M:%S', level=logging.INFO)
prev_distance = 0
loop = 0

def cherry_wait(target, distance):
    if distance < 200:
        time.sleep(.48)
    else:
        time.sleep(.5)
    device.shell('input touchscreen swipe 200 200 200 200 10')
    logging.info('after tap 1')
    if target < 150:
        time.sleep(.005)   
    elif target < 250:
        time.sleep(.05)
    elif target < 300:
        time.sleep(.15)
    elif target < 250:
        time.sleep(.15)
    elif target < 450:
        time.sleep(.3)
    elif target < 500:
        time.sleep(.45)
    elif target < 550:
        time.sleep(.5)
    elif target < 600:
        time.sleep(.6)
    elif target < 650:
        time.sleep(.65)
    elif target < 700:
        time.sleep(.8)
    elif target < 750:
        time.sleep(.75)
    else:
        time.sleep(.8)

        
    logging.info('before tap 2')
    device.shell('input touchscreen swipe 200 200 200 200 10')
    logging.info('after tap 2')
while True:
    loop += 1
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

    pixels = [list(i[:3]) for i in image[1735]]

    transitions = []
    ignore = True
    black = True
    red = True
    cherry = []

    for i, pixel in enumerate(pixels):
        r, g, b = [int(i) for i in pixel]

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
    

    # calculate distance to perfect vault
    start, target1, target2 = transitions
    gap = target1 - start
    target = target2 - target1 
    distance = (gap + target / 2) 
    if distance < 300:
        distance = distance
    elif distance < 500:
        distance = distance * .978
    else:
        distance = distance * .982

    print(cherry)
    if len(cherry) != 0:
        cherry_target = statistics.mean(cherry) - start
        cherry_possible = True
        logging.info('cherry possible: ' + str(cherry_target))

    else:
        cherry_possible = False
        
    logging.info('before adb swipe')
    device.shell(f'input touchscreen swipe 500 500 500 500 {int(distance)}')
    logging.info('after adb swipe')

    if cherry_possible:
        cherry_wait(cherry_target, distance)  

    print()
    print('Loop number: ' + str(loop))
    print()
    
    if loop == 1 and cherry_possible:
        prev_distance = cherry_target
    if loop > 1:     
        image = device.screencap()

        with open('screen.png', 'wb') as f:
            f.write(image)

        image = Image.open('screen.png')
        image = numpy.array(image)
        
        pixels = [list(i[:3]) for i in image[1350]]
        for i, pixel in enumerate(pixels):
            r, g, b = [int(i) for i in pixel]
            if (r+g+b) == 383:
                device.shell('input touchscreen swipe 850 1620 850 1620 10')
                if prev_distance != 0:
                    with open('cherry_distance.txt', 'a') as f:
                        f.write(str(prev_distance) + ' ')
                        print('write')
                break
        if cherry_possible:
            prev_distance = cherry_target
        else:
            prev_distance = 0
        
    time.sleep(2.6)

