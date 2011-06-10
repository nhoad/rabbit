import time
import os
import sqlite3
_filename = '.rabbit'

class MissingRepositoryError(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return 'Rabbit repository is missing or could not be found'


class IllegalCommandError(Exception):
    def __init__(self, command):
        self.command = command

    def __str__(self):
        return "'{0}' is not a Rabbit command. See 'rabbit help'.".format(self.command)


class RepositoryExistsError(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return 'There already exists a Rabbit repository in this directory'


class NonexistentIssueError(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return 'The specified Issue does not exist'


class Issue:

    def __init__(self, i_id=None, type='unknown', status='open', priority='medium', summary='', date=time.strftime('%Y-%m-%d'), description=''):
        self.i_id = i_id
        self.type = type
        self.status = status
        self.priority = priority
        self.summary = summary
        self.date = date
        self.description = description

    def generate_update(self):
        """Generate the SQL update statement to update this issue

        This does not generate SQL for comments, or persist the object."""

        if i_id is None:
            raise NonexistentIssueError()

        return """update Issue set type = '{0}', date='{1}', status='{2}',
                  priority='{3}', summary='{4}', description='{5}'
                  where id = {6};)""".format(self.type, self.status,
                  self.priority, self.summary, self.date,
                  self.description, self.i_id).replace('\n', '')

    def generate_insert(self):
        """Generate the SQL insert statement to save this issue

        This does not generate the SQL necessary for saving the comments, nor does it actually persist the object."""

        return """insert into Issue(type, date, status, priority, summary,
                  description) values('{0}', '{1}', '{2}', '{3}', '{4}',
                  '{5}');""".format(self.type, self.date, self.status, self.priority,
                  self.summary, self.description).replace('\n', '')

    def __str__(self):
        return '| {:>2} | {:>11} | {} | {:>6} | {:>6} | {} |' .format(
            self.i_id, self.type, self.date, self.status, self.priority, self.summary)

"""Rabbit class, for managing bugs in the rabbit repository"""
class Rabbit:
    def __init__(self):
        """Create the Rabbit object.

        Will raise MissingRepositoryError if you haven't initialised a
        repository in the working directory

        """

        if not os.path.isfile(_filename):
            raise MissingRepositoryError()

        self.conn = sqlite3.connect(_filename)

    def __del__(self):
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
        self.conn.execute(issue.generate_insert())
        self.conn.commit()

    def close(self, issue_ids):
        """Update the status of an issue to 'closed'

        Keyword arguments:
        issue_ids -- set of integer ids to be closed

        """

        for i_id in issue_ids:
            self.conn.execute("update Issue set status='closed' where id = {0};".format(i_id))

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

        self.conn.execute("Insert into Comment(issueID, description) values({}, '{}')".format(issue_id, comment))
        self.conn.commit()

    def issues(self, status_filter='all'):
        """Return a list of all Issues in the repository.

        TODO: Add comment retrieval in as well.

        Keyword arguments:
        status_filter -- status to filter. Default results in all open bugs being returned. Pass all to return all

        """

        cursor = self.conn.cursor()

        query = "select id, type, status, priority, summary, date, description from Issue where status = '{0}'".format(status_filter)

        if status_filter in ('all', ''):
            query = "select id, type, status, priority, summary, date, description from Issue"

        cursor.execute(query)

        issues = []
        for r in cursor:
            issues.append(Issue(r[0], r[1], r[2], r[3], r[4], r[5], r[6]))

        return issues
