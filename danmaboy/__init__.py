# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import time
from enum import Enum

import danmu
import keyboard

default_url = 'http://www.douyu.com/lisp'
default_key = 'alt+8'
default_keys = ['b', 'w', 's', 'a', 'd', 'g', 'h', 't', 'y', 'u']


class KeyStrokes(Enum):
    def __new__(cls, chinese, number, english):
        obj = object.__new__(cls)
        obj._value_ = int(number)
        obj.chinese = chinese  # type: str
        obj.number = number  # type: str
        obj.english = english  # type: str
        return obj

    UP = ('上', '1', 'up')
    DOWN = ('下', '2', 'down')
    LEFT = ('左', '3', 'left')
    RIGHT = ('右', '4', 'right')
    A = ('a', '5', 'a')
    B = ('b', '6', 'b')
    L = ('l', '7', 'l')
    R = ('r', '8', 'r')
    SELECT = ('select', '9', 'select')
    START = ('start', '0', 'start')

    def real_key(self):
        keys = default_keys
        return keys[self.value]


joypad = {}
for _key in KeyStrokes:
    joypad.update({
        _key.chinese: _key,
        _key.number: _key,
        _key.english: _key,
    })


class DanmaBoyException(Exception):
    """ 所有弹幕相关的异常类 """


class Gamer(object):
    def __init__(self, url=default_url, switch_key=default_key):
        self.url = url
        self.client = danmu.DanMuClient(self.url)
        if not self.client.isValid():
            raise Exception('直播间获取失败')
        self.hint('弹幕已连接，直播间地址：{}'.format(self.url))
        self.receive = self.client.danmu(self.receive)

        self.switch_key = switch_key
        self.started = False

    def hint(self, message=None, system=True):
        if message is None:
            print('-' * 42)
            return
        prefix = '[系统] ' if system else ''
        print('{}{}'.format(prefix, message))

    def switch(self):
        self.hint('按下 <{}> 键可{}'.format(self.switch_key, self.next_state(self.started)))
        keyboard.wait(self.switch_key)
        self.hint()
        self.hint('游戏已{}'.format(self.next_state(self.started)))
        if self.started:
            self.client.stop()
        else:
            self.client.start()
        self.started = not self.started

    def ready(self):
        while True:
            self.switch()

    def receive(self, danmaku):
        if not self.started:
            return
        nickname, content = danmaku['NickName'], str(danmaku['Content']).lower()
        if content not in joypad:
            return
        key = joypad[content]  # type: KeyStrokes
        self.hint('{}: {} ({})'.format(nickname, key.chinese.upper(), content), system=False)
        keyboard.press(key.real_key())
        time.sleep(0.04)
        keyboard.release(key.real_key())

    def next_state(self, state):
        return '结束' if state else '开始'


if __name__ == '__main__':
    Gamer().ready()
