import unittest
import os

os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
os.environ['AWS_SECURITY_TOKEN'] = 'testing'
os.environ['AWS_SESSION_TOKEN'] = 'testing'
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
os.environ['AWS_REGION'] = 'us-east-1'

# Discover tests in the "tests" folder (or any folder you want)
# The pattern "*.py" will discover all Python files in the folder
test_loader = unittest.defaultTestLoader
test_suite = test_loader.discover('.', pattern='*.py')

# Run all the tests in the discovered suite
test_runner = unittest.TextTestRunner(verbosity=2)
test_runner.run(test_suite)
