from rabbit import *
import sys

def usage():
    print('olo')

class RabbitConsole:
    def __init__(self):
        self.rabbit = Rabbit()

    def display_all(self):
        issues = rabbit.issues()

        for i in issues:
            print(issue)

    def display_detail(self, issue_id):
        pass


if len(sys.argv) == 1:
    usage()
    exit(1)

if sys.argv[1] == 'init':
    Rabbit.init()
else:
    try:
        RabbitConsole()
    except MissingRepositoryError as e:
        print('FATAL:', e)
