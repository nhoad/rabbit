#!/usr/bin/env python
import sys

def usage():
    print('olo')

class RabbitConsole:
    def __init__(self):
        self.rabbit = Rabbit()

        command = sys.argv[1]

        if command == 'add':
            pass
        elif command == 'list':
            pass
        elif command == 'detail':
            pass
        elif command == 'comment':
            pass
        elif command == 'rm':
            pass
        elif command == 'update':
            pass
        elif command == 'close':
            pass
        elif command == 'open':
            pass
        elif command == 'help':
            pass
        else:
            raise IllegalCommandError(command)

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
    except IllegalCommandError as e:
        print('rabbit:', e)
