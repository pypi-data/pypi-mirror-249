#!/usr/bin/env python
#-*- coding: utf-8 -*-

import subprocess

def sendmessage(message):
    subprocess.Popen(['notify-send', message])
    return

def main():
    command = input(">> ")

    result = subprocess.run(command.split(" "), stdout=subprocess.PIPE)
    print(result.stdout.decode("utf-8"))

    sendmessage('Your command is ready')


if __name__ == '__main__':
    main()

