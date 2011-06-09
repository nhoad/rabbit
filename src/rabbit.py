_filename = '.rabbit'

class MissingRepositoryError(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return 'Rabbit repository is missing or could not be found'


class NonexistentIssueError(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return 'The specified Issue does not exist'


class Issue:
    import time
    type = 'unknown'
    status = 'open'
    priority = 'medium'
    summary = ''
    date = time.strftime('%Y-%m-%d')
    description = ''

    def __init__(self, i_id=None):
        self.i_id = i_id

    def generate_update(self):
        """Generate the SQL update statement to update this issue

        This does not generate SQL for comments, or persist the object."""

        if i_id is None:
            raise NonexistentIssueError()

        return """update Issue set type = '{0}', date='{1}', status='{2}',
                  priority='{3}', summary='{4}', description='{5}'
                  where id = {6})""".format(self.type, self.status,
                  self.priority, self.summary, self.date,
                  self.description, self.i_id).replace('\n', '')

    def generate_insert(self):
        """Generate the SQL insert statement to save this issue

        This does not generate the SQL necessary for saving the comments, nor does it actually persist the object."""

        return """insert into Issue(type, date, status, priority, summary,
                  description) values('{0}', '{1}', '{2}', '{3}', '{4}',
                  '{5}')""".format(self.type, self.status, self.priority,
                  self.summary, self.date, self.description).replace('\n', '')

    def __str__(self):
        return '| {0} | {1} | {2} | {3} | {4} | {5} |' .format(
            self.id, self.type, self.date, self.status, self.priority, self.summary)

class Rabbit:
    """Create the Rabbit object.

    Will raise MissingRepositoryError if you haven't initialised a
    repository in the working directory

    """

    def __init__(self):
        import os

        if not os.path.isfile(_filename):
            raise MissingRepositoryError()

        import sqlite3

        self.conn = sqlite3.connect(_filename)

    @staticmethod
    def init(self):
        """Create the database file and create the tables."""
        self.conn = sqlite3.connect(_filename)

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

    def add(self, issue):
        """Add a new issue to the repository

        Keyword arguments:
        issue -- Issue object to be stored

        """
        self.conn.execute(issue.generate_insert())

    def close(self, issue_id):
        """Update the status of an issue to 'closed'

        Keyword arguments:
        issue_id -- set of integer ids to be closed

        """

        for i_id in issue_ids:
            self.conn.execute("update Issue set status='closed' where id = {0}".format(i_id))

    def open(self, issue_ids):
        """Update the status of an issue to 'open'

        Keyword arguments:
        issue_ids -- set of integers ids to be opened

        """

        for i_id in issue_ids:
            self.conn.execute("update Issue set status='open' where id = {0}".format(i_id))

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

        self.conn.execute("Insert into Comment(issueID, description) values({0}, '{1}'").format(issue_id, comment)

    def issues(self):
        """Return a list of all Issues in the repository.

        TODO: Add comments in as well.

        """

        cursor = self.conn.cursor()
        cursor.execute('select id, type, date, status, priority, summary from Issue')

        issues = []
        for r in cursor:
            issues.append(Issue(row[0], row[1], row[2], row[3], row[4], row[5]))

        return issues
