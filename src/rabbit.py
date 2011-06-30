#!/usr/bin/env python3
import time
import os
import sqlite3
_filename = '.rabbit'

class MissingSummaryError(Exception):
    'You must provide a summary'

    def __str__(self):
        return self.__doc__


class MissingRepositoryError(Exception):
    'Rabbit repository is missing or could not be found. Try running rabbit init'
    def __str__(self):
        return self.__doc__


class MissingArgumentError(Exception):
    'No arguments supplied'
    def __str__(self):
        return self.__doc__


class IllegalCommandError(Exception):
    "'{0}' is not a Rabbit command. See 'rabbit help'."

    def __init__(self, command):
        self.command = command

    def __str__(self):
        return self.__doc__.format(self.command)


class RepositoryExistsError(Exception):
    'There already exists a Rabbit repository in this directory'
    def __str__(self):
        return self.__doc__


class NonexistentIssueError(Exception):
    'The specified Issue does not exist'

    def __str__(self):
        return self.__doc__


class Issue:

    def __init__(self, i_id=None, type='unknown', status='open', priority='medium', summary='', date=time.strftime('%Y-%m-%d'), description=''):
        self.i_id = i_id
        self.type = type
        self.status = status
        self.priority = priority
        self.summary = summary
        self.date = date
        self.description = description

        self.comments = []

    def generate_update(self):
        """Generate the SQL update statement to update this issue

        This does not generate SQL for comments, or persist the object."""

        if self.i_id is None:
            raise NonexistentIssueError()

        return """update Issue set type = '{0}', date='{1}', status='{2}',
                  priority='{3}', summary='{4}', description='{5}'
                  where id = {6}""".format(self.type, self.date,
                  self.status, self.priority, self.summary,
                  self.description, self.i_id).replace('\n', '')

    def generate_insert(self):
        """Generate the SQL insert statement to save this issue

        This does not generate the SQL necessary for saving the comments, nor does it actually persist the object."""

        return """insert into Issue(type, date, status, priority, summary,
                  description) values('{0}', '{1}', '{2}', '{3}', '{4}',
                  '{5}');""".format(self.type, self.date, self.status, self.priority,
                  self.summary, self.description).replace('\n', '')

    def __str__(self):
        text = 'Issue ID: {}\nSummary: {}\nType: {}\nDate: {}\nStatus: {}\nPriority: {}\nDescription: {}'.format(
            self.i_id, self.summary, self.type, self.date, self.status, self.priority, self.description)

        return text

    def __repr__(self):
        """Returns the same text as __str__, but html formatted."""
        text = '<b>Issue ID:</b> {}<br><b>Summary:</b> {}<br><b>Type:</b> {}<br><b>Date:</b> {}<br><b>Status:</b> {}<br><b>Priority:</b> {}<br><b>Description:</b> {}'.format(
            self.i_id, self.summary, self.type, self.date, self.status, self.priority, self.description)

        comments = self.comments

        if len(comments) > 0:
            text += "<br><br><b>Comments:</b><br>"
            text += "<br><br>".join([c[1] for c in self.comments])

        return text


"""Rabbit class, for managing bugs in the rabbit repository"""
class Rabbit:
    conn = None

    def __init__(self):
        """Create the Rabbit object.

        Will raise MissingRepositoryError if you haven't initialised a
        repository in the working directory

        """

        if not os.path.isfile(_filename):
            raise MissingRepositoryError()

        self.conn = sqlite3.connect(_filename)

    def __del__(self):
        if self.conn:
            self.conn.close()

    @staticmethod
    def init():
        """Create the database file and create the tables."""

        if os.path.isfile(_filename):
            raise RepositoryExistsError()

        conn = sqlite3.connect(_filename)

        issue_table = """create table Issue(id INTEGER PRIMARY KEY,
                         type varchar(500),
                         date varchar(10),
                         status varchar(10),
                         priority varchar(500),
                         summary varchar(500),
                         description varchar(500))"""

        comment_table = """create table Comment(id INTEGER PRIMARY KEY,
                           issueID INTEGER,
                           description varchar(500))"""

        conn.execute(issue_table)
        conn.execute(comment_table)
        conn.close()
        print('Empty Rabbit repository created')

    def add(self, issue):
        """Add a new issue to the repository

        Keyword arguments:
        issue -- Issue object to be stored

        """

        if not issue.summary:
            raise MissingSummaryError()

        self.conn.execute(issue.generate_insert())
        self.conn.commit()

    def close(self, issue_ids):
        """Update the status of an issue to 'closed'

        Keyword arguments:
        issue_ids -- set of integer ids to be closed

        """

        for i_id in issue_ids:
            self.conn.execute("update Issue set status='closed' where id = {0}".format(i_id))

        self.conn.commit()

    def open(self, issue_ids):
        """Update the status of an issue to 'open'

        Keyword arguments:
        issue_ids -- set of integers ids to be opened

        """

        for i_id in issue_ids:
            self.conn.execute("update Issue set status='open' where id = {0}".format(i_id))

        self.conn.commit()

    def update(self, issue):
        """Update an issue in the database

        Keyword arguments:
        issue -- Issue object to be updated in the database

        """

        if not issue.summary:
            raise MissingSummaryError()

        self.conn.execute(issue.generate_update())
        self.conn.commit()

    def delete(self, issue_id):
        """Delete an issue and all associated comments.

        Keyword arguments:
        issue_id -- integer id of the Issue to be removed.

        """

        self.conn.execute('delete from Comment where issueID = {}'.format(issue_id))
        self.conn.execute('delete from Issue where id = {}'.format(issue_id))
        self.conn.commit()

    def comment(self, issue_id, comment):
        """Add a comment to an issue

        Keyword arguments:
        issue_id -- issue id to add a comment to
        comment -- string containing the comment.

        """

        self.conn.execute("Insert into Comment(issueID, description) values({}, '{}')".format(issue_id, comment.replace("'", "''")))
        self.conn.commit()

    def issue(self, issue_id):
        """Return a specific Issue

        TODO: Add comment retrieval in as well.

        Keyword arguments:
        issue_id -- id of the issue to return

        """

        cursor = self.conn.cursor()

        query = "select id, type, status, priority, summary, date, description from Issue where id = {}".format(issue_id)

        cursor.execute(query)
        r = cursor.fetchone()

        if r is None:
            raise NonexistentIssueError()

        i = Issue(r[0], r[1], r[2], r[3], r[4], r[5], r[6])

        query = "select id, description from Comment where issueID = {}".format(issue_id)
        cursor.execute(query)

        for row in cursor:
            i.comments.append((row[0], row[1]))

        return i

    def issues(self, status_filter='all'):
        """Return a list of all Issues in the repository.

        TODO: Add comment retrieval in as well.

        Keyword arguments:
        status_filter -- status to filter. Default results in all open bugs being returned. Pass all to return all

        """

        cursor = self.conn.cursor()
        comments = self.conn.cursor()

        query = "select id, type, status, priority, summary, date, description from Issue where status = '{0}'".format(status_filter)

        if status_filter in ('all', ''):
            query = "select id, type, status, priority, summary, date, description from Issue"

        cursor.execute(query)

        issues = []
        for r in cursor:
            comments.execute('select id, description from Comment where issueID = {}'.format(r[0]))

            i = Issue(r[0], r[1], r[2], r[3], r[4], r[5], r[6])

            for c in comments:
                i.comments.append((c[0], c[1]))

            issues.append(i)

        return issues


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
            i.i_id, prettify(i.type, 11), i.date, i.status, i.priority)) - 4

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
                i.i_id, prettify(i.type, 11), i.date, i.status, i.priority)

            final_line = first_half + '{' + summary + '}'
            print(final_line.format(prettify(i.summary, available_width)), '|')

        print(nice_bars)

    def display_detail(self, issue_id):
        issue = self.rabbit.issue(issue_id)

        print(issue)

        print('Comments:')
        for c in issue.comments:
            print(c[1])

if __name__ == '__main__':
    if len(sys.argv) == 1:
        usage()
        sys.exit(1)

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
        except (IllegalCommandError, MissingArgumentError, NonexistentIssueError, MissingSummaryError) as e:
            print('rabbit:', e)

    # if it makes it here, then an error occured
    sys.exit(1)
