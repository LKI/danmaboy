# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import keyboard

if __name__ == '__main__':
    print('Link start')
    while True:
        keyboard.wait('1')
        print('hey, you press 1')
        keyboard.send('alt+4')
