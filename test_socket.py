#!/usr/bin/env python

import json
import socket


EXPECTED_BOT_NAME = 'Airbot'
TIMEOUT = 1


def _connect():
    return socket.create_connection(('localhost','9001'), timeout=TIMEOUT)


def _send_and_recv(msg):
    c = _connect()
    size = c.send(msg.encode('utf-8') + b'\n')
    retval = c.recv(size+1)
    return retval.decode()

def test_uptime():
    retval = _send_and_recv('UPTIME')
    assert int(retval)


def test_name():
    retval = _send_and_recv('NAME')
    assert retval == EXPECTED_BOT_NAME


def test_json():
    data = {
        'gamePlan': [
            '   ',
            ' 1 ',
            '   ',
        ],
        'yourBotId': 1,
        'botIds': [1],
        'liveBotIds': [1],
    }
    data_json = json.dumps(data)
    retval = _send_and_recv(data_json)
    assert retval == 'RR'


if __name__ == '__main__':
    print('please use py.test to run this file')
