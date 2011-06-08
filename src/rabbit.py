_filename = '.rabbit'

import time
import sqlite3

class Issue:
    type = 'unknown'
    status = 'open'
    priority = 'medium'
    summary = ''
    date = time.strftime('%Y-%m-%d')
    description = ''

class Rabbit:
    def __init__(self):
        self.conn = sqlite3.connect(_filename)

    def _create_database(self):
        pass

    def init(self):
        self._create_database()
        # add example issue?

    def add(self, issue):
        pass

    def close(self, issue_id):
        pass

    def open(self, issue_id):
        pass

    def update(self, issue):
        pass

    def delete(self, issue):
        pass

    def add_comment(self, issue_id, comment):
        pass
