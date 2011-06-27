#!/usr/bin/env python

import sys
import getopt

def usage():
    try:
        command = sys.argv[2]
        if command not in ('add', 'list', 'detail', 'comment', 'rm', 'update', 'close', 'open'):
            raise IllegalCommandError(command)

        if command == 'add':
            print("Usage: rabbit add [OPTION]" +
                  "\nOptions:" +
                  "\n  -b, --summary=SUMMARY          brief description of the issue"+
                  "\n  -d, --description=DESCRIPTION  extended description of the issue" +
                  "\n  -t, --type=TYPE                type of issue, e.g. enhancement, bug" +
                  "\n  -s, --status=STATUS            status of the problem, e.g. open, closed" +
                  "\n  -p, --priority=PRIORITY        issue priority, e.g. high, medium, low")

        elif command == 'list':
            print("Usage: rabbit list [STATUS]" +
                  "\nList issues, filtered by STATUS." +
                  "\nExample: rabbit list open")

        elif command == 'detail':
            print("Usage: rabbit detail [ID]" +
                  "\nDetailed description of an issue, showing comments and extended info.")

        elif command == 'comment':
            print("Usage: rabbit comment [ID] [COMMENT]")
        elif command == 'rm':
            print("Usage: rabbit rm [ID]")

        elif command == 'update':
            print("Usage: rabbit update [ID] [OPTION]" +
                  "\nOptions:" +
                  "\n  -b, --summary=SUMMARY          brief description of the issue"+
                  "\n  -d, --description=DESCRIPTION  extended description of the issue" +
                  "\n  -t, --type=TYPE                type of issue, e.g. enhancement, bug" +
                  "\n  -s, --status=STATUS            status of the problem, e.g. open, closed" +
                  "\n  -p, --priority=PRIORITY        issue priority, e.g. high, medium, low")

        elif command == 'close':
            print("Usage: rabbit close [ID]..." +
                  "\nClose a set of issues.")

        else:
            print("Usage: rabbit open [ID]..." +
                  "\nRe-open a set of issues.")

    except IndexError:
        print("Usage: rabbit [COMMAND] [OPTION]..." +
          "\nExample: rabbit add --summary 'Segfault on program start' --priority high" +
          "\nCommands:" +
          "\n  add        Add an issue" +
          "\n  list       List all issues" +
          "\n  detail     Detailed info about an issue" +
          "\n  comment    Add a comment to an issue" +
          "\n  rm         Remove an issue" +
          "\n  update     Modify an issue" +
          "\n  close      Close an issue" +
          "\n  open       Re-open an issue" +
          "\n\nExtended help for any command is accessible via 'rabbit help [COMMAND]'")

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
            try:
                self.display_detail(int(sys.argv[2]))
            except ValueError:
                print('Issue ID must be a number!')
                sys.exit(1)
            except IndexError:
                print('You must provide an Issue ID')
                sys.exit(1)

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
            usage()
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
                i.type = arg.replace("'", "''")
            if opt in ('-s', '--status'):
                i.status = arg.replace("'", "''")
            if opt in ('-p', '--priority'):
                i.priority = arg.replace("'", "''")
            if opt in ('-d', '--description'):
                i.description = arg.replace("'", "''")
            if opt in ('-b', '--brief'):
                i.summary = arg.replace("'", "''")

        return i

    def display(self, status):
        issues = self.rabbit.issues(status)

        if len(issues) == 0:
            return

        if sys.platform == 'win32':
            term_width = 80
        else:
            term_width = int(os.popen('stty size', 'r').read().split()[1])


        prettify = lambda text, max_length: text[:max_length - 3].replace(
            '\n', '') + '...' if len(text) > max_length else text.replace('\n', '')

        i = issues[0]

        available_width = term_width - len("| {:>2} | {:<11} | {} | {:<6} | {:<6} | ".format(
            i.i_id, i.type, i.date, i.status, i.priority)) - 4

        # if the user is using a tiny terminal, screw them.
        # for reference, that would be a terminal width of ~20 characters.
        if available_width < 1:
            available_width = 80

        summary = ":<{}".format(available_width)

        nice_bars = "".join(['*' for i in range(term_width)])

        print(nice_bars)
        print("| {:>2} | {:<11} | {:<10} | {:<6} | {} | ".format(
            'id', 'type', 'date', 'status', 'priority') + str('{' + summary + '} |').format('summary'))
        print(nice_bars)

        # get terminal width
        for i in issues:
            first_half = "| {:>2} | {:<11} | {} | {:<6} | {:<8} | ".format(
                i.i_id, i.type, i.date, i.status, i.priority)

            final_line = first_half + '{' + summary + '}'
            print(final_line.format(prettify(i.summary, available_width)), '|')

        print(nice_bars)

    def display_detail(self, issue_id):
        issue = self.rabbit.issue(issue_id)

        print(issue)

        print('Comments:')
        for c in issue.comments:
            print(c[1])

if len(sys.argv) == 1:
    usage()
    sys.exit(1)

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
    except NonexistentIssueError as e:
        print('rabbit:', e)

# if it makes it here, then an error occured
sys.exit(1)
