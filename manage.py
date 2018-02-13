

import unittest
import coverage

from flask import current_app
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from secret_config import Config

from app.server import create_app, db, models, bcrypt


# code coverage
COV = coverage.coverage(
    branch=True,
    include='app/*',
    omit=[
        'app/tests/*',
        'app/server/config.py',
        'app/server/*/__init__.py'
    ]
)
COV.start()

app = create_app()
migrate = Migrate(app, db)
manager = Manager(app)

# migrations
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('app/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('app/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1


@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()

@manager.command
def drop_db():
    """Drops the db tables."""
    db.drop_all()


@manager.command
def create_admin():
    """Creates the admin user."""
    admin = models.User(username= Config().ADMIN_USERNAME, email=Config().ADMIN_EMAIL, password =Config().ADMIN_PASSWORD, admin=True)
    db.session.add(admin)
    db.session.commit()


if __name__ == '__main__':
    manager.run()
