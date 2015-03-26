import mock

from librarian.app import in_pkg
from librarian.lib import squery
from librarian.utils import migrations


def transaction_test(func):
    def _transaction_test(*args, **kwargs):
        with mock.patch('bottle.request') as bottle_request:
            conn = squery.Connection()
            db = squery.Database(conn)
            config = {'content.contentdir': '/tmp'}
            migrations.migrate(db,
                               in_pkg('migrations'),
                               'librarian.migrations',
                               config)
            bottle_request.db = db

            return func(*args, **kwargs)

    return _transaction_test
