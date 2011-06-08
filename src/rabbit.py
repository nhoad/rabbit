_filename = '.rabbit'

import time
import sqlite3
import sys

class Issue:
    type = 'unknown'
    status = 'open'
    priority = 'medium'
    summary = ''
    date = time.strftime('%Y-%m-%d')
    description = ''

    def __init__(self):
        pass

    def generate_update(self):
        """Generate the SQL update statement to update this issue"""
        pass

    def generate_insert(self):
        """Generate the SQL insert statement to save this issue

        This does not generate the SQL necessary for saving the comments."""
        pass


class MissingRepositoryError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Rabbit:
    def __init__(self):
        if not os.path.isfile(_filename) and sys.argv[1].lower() != 'init':
            raise MissingRepositoryError()

        self.conn = sqlite3.connect(_filename)

    def _create_database(self):
        """Create the database file and create the tables"""
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

        self.conn.execute(issue_table)
        self.conn.execute(comment_table)

    def init(self):
        self._create_database()
        # add example issue?

    def add(self, issue):
        self.conn.execute(issue.generate_insert())

    def close(self, issue_id):
        self.conn.execute("update Issue set status='closed' where id = {0}".format(issue_id)
        pass

    def open(self, issue_id):
        """Update the status of an issue to 'open'

        Keyword arguments:
        issue_id -- integer value for the id to be updated

        """

        self.conn.execute("update Issue set status='open' where id = {0}".format(issue_id)

    def update(self, issue):
        """Update an issue in the database

        Keyword arguments:
        issue -- Issue object to be updated in the database

        """

        self.conn.execute(issue.generate_update())

    def delete(self, issue):
        """Delete an issue an all associated comments"""

        self.conn.execute('delete from Comment where issueID = {0}'.format(issue.i_id))
        self.conn.execute('delete from Issue where id = {0}'.format(issue.i_id))

    def add_comment(self, issue_id, comment):
        """Add a comment to an issue

        Keyword arguments:
        issue_id -- issue id to add a comment to
        comment -- string containing the comment.

        """

        self.conn.execute("Insert into Comment(issueID, description) values({0}, '{1}').format(issue_id, comment)
