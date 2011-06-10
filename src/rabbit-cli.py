#!/usr/bin/env python

import sys
import getopt

def usage():
    print('usage')

class RabbitConsole:
    def __init__(self):
        self.rabbit = Rabbit()

        command = sys.argv[1]

        if command == 'add':
            issue = self._parse_args()
            self.rabbit.add(issue)

        elif command == 'update':
            issue = self._parse_args()
            self.rabbit.add(update)

        elif command == 'list':
            try:
                self.display(sys.argv[2])
            except IndexError:
                self.display('')

        elif command == 'detail':
            pass
        elif command == 'comment':
            try:
                self.rabbit.comment(int(sys.argv[2]), sys.argv[3])
            except ValueError:
                print('Issue ID must be a number!')
                sys.exit(1)
            except IndexError:
                print('You must provide an Issue ID and a comment!')
                sys.exit(1)

        elif command == 'rm':
            try:
                self.rabbit.delete(sys.argv[2])
            except IndexError:
                print('Missing ID')
                sys.exit(1)

        elif command == 'close':
            try:
                self.rabbit.close([int(x) for x in sys.argv[2:]])
            except ValueError:
                print('IDs must be numbers!')
                sys.exit(1)

        elif command == 'open':
            try:
                self.rabbit.open([int(x) for x in sys.argv[2:]])
            except ValueError:
                print('IDs must be numbers!')
                sys.exit(1)

        elif command == 'help':
            pass
        else:
            raise IllegalCommandError(command)

    def _parse_args(self):
        sys_args = sys.argv[2:] if sys.argv[1] == 'add' else sys.argv[3:]

        opts, args = getopt.getopt(sys_args, "t:s:p:d:b:",
            ["type=", "status=", "priority=", "description=", "summary="])

        i = Issue()

        if sys.argv[1] == 'update':
            i.i_id = int(sys.argv[2])

        if not opts:
            raise MissingArgumentError()

        for opt, arg in opts:
            if opt in ('-t', '--type'):
                i.type = arg
            if opt in ('-s', '--status'):
                i.status = arg
            if opt in ('-p', '--priority'):
                i.priority = arg
            if opt in ('-d', '--description'):
                i.description = arg
            if opt in ('-b', '--brief'):
                i.summary = arg

        return i

    def display(self, status):
        issues = self.rabbit.issues(status)

        for i in issues:
            print(i)

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
        sys.exit(0)
    except MissingRepositoryError as e:
        print('FATAL:', e)
    except IllegalCommandError as e:
        print('rabbit:', e)
    except MissingArgumentError as e:
        print('rabbit:', e)

# if it makes it here, then an error occured
sys.exit(1)
