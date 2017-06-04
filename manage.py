#!/usr/bin/env python
import os
from app import app
from flask_script import Manager, Shell


manager = Manager(app)


def make_shell_context():
    return dict(app=app)
manager.add_command("shell", Shell(make_context=make_shell_context))



@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
