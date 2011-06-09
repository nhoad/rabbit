#!/usr/bin/env python
import sys

def usage():
    print('olo')

class RabbitConsole:
    def __init__(self):
        self.rabbit = Rabbit()

    def display(self):
        issues = rabbit.issues()

        for i in issues:
            print(issue)

    def display_detail(self, issue_id):
        pass


if len(sys.argv) == 1:
    usage()
    exit(1)

from rabbit import *

if sys.argv[1] == 'init':
    try:
        Rabbit.init()
    except RepositoryExistsError as e:
        print('FATAL:', e)
else:
    try:
        RabbitConsole()
    except MissingRepositoryError as e:
        print('FATAL:', e)
