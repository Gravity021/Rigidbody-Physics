# Only run code if this is the file being executed
if __name__ != "__main__":
    quit()

import unittest

# Import all files that contain test classes
from app_test.core.test_app import *
from app_test.core.test_window import *
from app_test.core.test_event_manager import *

# Perform the tests
unittest.main()