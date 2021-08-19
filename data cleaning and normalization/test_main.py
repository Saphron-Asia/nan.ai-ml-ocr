import unittest
from file_handler import FileHandler
from roi import RegionsOfInterest as RoI
from abc import ABCMeta, abstractproperty
import imutils
import sys
import os

class AbstractTestData:
    __metacles__ = ABCMeta

    def __init__(self):
        pass
    
    @abstractproperty
    def csv_path(self):
        return NotImplemented

    @abstractproperty
    def raw_files_path(self):
        return NotImplemented
    
    @abstractproperty
    def templates_path(self):
        return NotImplemented

class TestData(AbstractTestData):
    csv_path = 'raw copy/roi-third-batch-again.csv'
    raw_files_path = 'raw/filtered/'
    templates_path = 'raw copy/templates'

class TestMain(unittest.TestCase):
    ENV_KEY = 'TEST_DATA_CLASS'
    DEFAULT_TEST_DATA_CLASS_NAME = 'TestData'

    TEST_DATA = None

    def setUp(self):
        # Initialize instance of test data class
        test_data_class_name = os.getenv(TestMain.ENV_KEY,
                                         TestMain.DEFAULT_TEST_DATA_CLASS_NAME)
        test_data_class = getattr(sys.modules[__name__], test_data_class_name)
        self.TEST_DATA = test_data_class()

    def test_read_csv(self):
        loader = FileHandler(csvPath=self.TEST_DATA.csv_path, debug=False)
        roi = RoI(files=loader.files)
        total_objects = loader.read_csv()
        self.assertGreater(total_objects,0)

    def test_create_dir(self):
        loader = FileHandler(csvPath=self.TEST_DATA.csv_path, debug=False)
        roi = RoI(files=loader.files)
        loader.create_dir()
        dir_1 = os.path.isdir('output')
        self.assertTrue(dir_1)
        dir_2 = os.path.isdir('sorted')
        self.assertTrue(dir_2)
            

if __name__ == '__main__':
    unittest.main() 
