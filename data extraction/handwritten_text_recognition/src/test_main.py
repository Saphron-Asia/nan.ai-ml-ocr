import unittest
from main import write_summary
from main import infer
from main import FilePaths
from main import train

import pathlib
import os
from path import Path
import json
import cv2

from DataLoaderIAM import DataLoaderIAM, Batch
from Model import Model, DecoderType
from abc import ABCMeta, abstractproperty
import sys
from SamplePreprocessor import preprocess
from FileLoader import FileLoader

class AbstractTestData:
    __metacles__ = ABCMeta

    def __init__(self):
        pass
    
    @abstractproperty
    def textpath(self):
        return NotImplemented
    
    @abstractproperty
    def decoderType(self):
        return NotImplemented
    
    @abstractproperty
    def imgPath(self):
        return NotImplemented


class TestData(AbstractTestData):
    textpath = '../model/charList.txt'
    decoderType = DecoderType.BestPath
    imgPath = '../../word_detector_nn/output'

class TestHTRModel(unittest.TestCase):
    ENV_KEY = 'TEST_DATA_CLASS'
    DEFAULT_TEST_DATA_CLASS_NAME = 'TestData'

    TEST_DATA = None

    def setUp(self):
        # Initialize instance of test data class
        test_data_class_name = os.getenv(TestHTRModel.ENV_KEY,
                                         TestHTRModel.DEFAULT_TEST_DATA_CLASS_NAME)
        test_data_class = getattr(sys.modules[__name__], test_data_class_name)
        self.TEST_DATA = test_data_class()
    

    def test_write_summary(self):
        charErrorRates = 10
        wordAccuracies = 10
        result = write_summary(charErrorRates,wordAccuracies)
        expected_result = None
        self.assertEqual(expected_result,result)
    
    def test_infer(self):
        model = Model(open(self.TEST_DATA.textpath).read(), self.TEST_DATA.decoderType, mustRestore=True, dump='store_true')
        parent_dirs = [f.name for f in os.scandir(self.TEST_DATA.imgPath) if f.is_dir()]
        for parent_dir in parent_dirs:
            sub_dirs = [f.name for f in os.scandir(self.TEST_DATA.imgPath + '/' + parent_dir) if f.is_dir()]
            dir_progress = 0

            for subDir in sub_dirs:
                curr_dir =  self.TEST_DATA.imgPath + '/' + parent_dir + '/' + subDir
                imgLoader = FileLoader(Path(curr_dir))
                numImages = len(imgLoader.getImages())
                i = 0
                cumSum = 0

                for imgPath in imgLoader.getImages():
                    word, proby = infer(model, imgPath)

                    #check image in grayscale mode
                    check_img = preprocess(cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE), (128, 32))
                    batch = Batch(None, [check_img])
                    rec_result, prob_result = model.inferBatch(batch, True, imagePath=imgPath)
                    self.assertTrue(rec_result,word)
                    self.assertTrue(prob_result,proby)


                    imgLoader.appendResToJson(i, imgPath, word, proby)
                    cumSum += proby
                    i += 1

                dir_progress += 1
                model.averages[curr_dir] = cumSum/i
                imgLoader.dumpToJson(curr_dir)


            # check if dumpJson file not empty and saved properly
            with open(curr_dir + '/dataDump.json') as f:
                data = json.load(f)
                self.assertTrue(data)
            if not data:
                print("File is an empty structure") # empty dict or empty list

            # Compute overall average and dump logs to json file
            model.log(self.TEST_DATA.imgPath)
            with open(self.TEST_DATA.imgPath + '/logs.json') as l:
                logs = json.load(l)
                self.assertTrue(logs)
            if not logs:
                print("File is an empty structure")


    
if __name__ == '__main__':
    unittest.main() 
