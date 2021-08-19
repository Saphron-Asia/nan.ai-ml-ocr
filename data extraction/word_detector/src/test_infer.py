import unittest
from dataloader import DataLoaderImgFile
from eval import evaluate
from net import WordDetectorNet
from path import Path
from visualization import visualize_and_save
import os.path
from abc import ABCMeta, abstractproperty
import sys

class AbstractTestData:
    __metacles__ = ABCMeta

    def __init__(self):
        pass
    
    @abstractproperty
    def device(self):
        return NotImplemented
    
    @abstractproperty
    def data_dir(self):
        return NotImplemented
    
    @abstractproperty
    def output_dir(self):
        return NotImplemented
    
    @abstractproperty
    def model_dir(self):
        return NotImplemented
    @abstractproperty
    def decoderType(self):
        return NotImplemented

class TestCardcareData(AbstractTestData):
    device  = 'cpu'
    data_dir = '../data/Cardcare'
    output_dir = '../'
    model_dir =  '../model/weights'
   
class TestSagipData(AbstractTestData):
    device  = 'cpu'
    data_dir = '../data/Sagip'
    output_dir = '../'
    model_dir =  '../model/weights'

class TestKabklodData(AbstractTestData):
    device  = 'cpu'
    data_dir = '../data/Kabuklod'
    output_dir = '../'
    model_dir =  '../model/weights'


class WordDetectorTest(unittest.TestCase):
    ENV_KEY = 'TEST_DATA_CLASS'
    DEFAULT_TEST_DATA_CLASS_NAME = 'TestSagipData'

    TEST_DATA = None

    def setUp(self):
        # Initialize instance of test data class
        test_data_class_name = os.getenv(WordDetectorTest.ENV_KEY,
                                         WordDetectorTest.DEFAULT_TEST_DATA_CLASS_NAME)
        test_data_class = getattr(sys.modules[__name__], test_data_class_name)
        self.TEST_DATA = test_data_class()

    def test_worddetector(self):
        loader = DataLoaderImgFile(Path(self.TEST_DATA.data_dir),WordDetectorNet().input_size, self.TEST_DATA.device)
        res_result = evaluate(WordDetectorNet(), loader, max_aabbs=1000)
        total_imgs = len(res_result.batch_imgs)
        for i, (img, aabbs) in enumerate(zip(res_result.batch_imgs, res_result.batch_aabbs)):
            f = loader.get_scale_factor(i)
            aabbs = [aabb.scale(1 / f, 1 / f) for aabb in aabbs]
            img = loader.get_original_img(i)
            form_type = loader.fn_imgs[i].split("\\")[0]
            form_type = form_type.split("/")[2]
            filename = loader.fn_imgs[i].split("/")[1]
            folder_name = filename.split(".jpeg")[0]
            visualize_and_save(img, aabbs, form_type, folder_name, self.TEST_DATA.output_dir)

            #check if the output dir is not empty
            isdir = os.path.isdir('../output')
            self.assertTrue(isdir)

    def test_loader_get_scale_factor(self):
        loader = DataLoaderImgFile(Path(self.TEST_DATA.data_dir),WordDetectorNet().input_size, self.TEST_DATA.device)
        i = 0
        result = loader.get_scale_factor(i)
        expected_result = 1
        self.assertGreaterEqual(expected_result,result)
    
    def test_loader_get_original_img(self):
        loader = DataLoaderImgFile(Path(self.TEST_DATA.data_dir),WordDetectorNet().input_size, self.TEST_DATA.device)
        i = 0
        result = loader.get_original_img(i)
        self.assertTrue(len(result))
    
       


if __name__ == '__main__':
    unittest.main() 
