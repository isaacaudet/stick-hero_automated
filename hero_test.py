from http_touch import AndroidTouch
import logging

touch = AndroidTouch()

def test_touch_timing():
    assert touch.double_tap() != None
