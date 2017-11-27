import datetime

class Base(object):
    """Base class for all the tables.

    Default columns:
        `created_at`: creation time of this record
         `modified_at`: modification time of this record
         `id`: unique identifier of the record, allowing the table to be indexed by this field
         `value`: column of interest for the recommender algorithm
    """

    __abstract__ = True
    def __init__(self):
        self.id = None
        self.value = None
        self.created_at = datetime.datetime.now()
        self.modified_at = self.created_at