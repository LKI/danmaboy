# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import sys

from danmu import DanMuClient


def pp(msg):
    print(msg.encode(sys.stdin.encoding, 'ignore').decode(sys.stdin.encoding))


client = DanMuClient('http://www.douyu.com/lisp')
if not client.isValid():
    print('Url not valid')


@client.danmu
def danmu_fn(msg):
    pp('[%s] %s' % (msg['NickName'], msg['Content']))


@client.gift
def gift_fn(msg):
    pp('[%s] sent a gift!' % msg['NickName'])


@client.other
def other_fn(msg):
    print('[Other] {}'.format(msg))


if __name__ == '__main__':
    client.start(blockThread=True)
