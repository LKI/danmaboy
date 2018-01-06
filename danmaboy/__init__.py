# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import danmu
import keyboard

default_url = 'http://www.douyu.com/lisp'
default_key = 'alt+8'
default_joypad = {
    'w': {'1', 'up', '上', '↑'},
    's': {'2', 'down', '下', '↓'},
    'a': {'3', 'left', '左', '←'},
    'd': {'4', 'right', '右', '→'},
    'g': {'5', 'a'},
    'h': {'6', 'b'},
    't': {'7', 'l'},
    'y': {'8', 'r'},
    'u': {'9', 'select', '选择'},
    'b': {'0', 'start', '开始'},
}
reversed_joypad = {}
for key, texts in default_joypad.items():
    reversed_joypad.update({text: key for text in texts})


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
        if content not in reversed_joypad:
            return
        keystroke = reversed_joypad[content]
        self.hint('{}: {} ({})'.format(nickname, keystroke, content), system=False)

    def next_state(self, state):
        return '结束' if state else '开始'


if __name__ == '__main__':
    Gamer().ready()
