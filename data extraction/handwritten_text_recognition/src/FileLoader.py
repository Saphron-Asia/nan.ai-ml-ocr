import json
import operator

class FileLoader:

    def __init__(self, fnInferDir):
        self.fn_imgs = fnInferDir.files('*.jpeg')
        self.dumpDict = {}

    def getImages(self):
        return self.fn_imgs

    def appendResToJson(self, currIdx, imgPath, word, probability):
        self.dumpDict[currIdx] = {"Image": imgPath, "Recognized": word, "Probability": str(probability)}

    def getImageID(self, imgPath):
        filename = imgPath.split("/")[-1]
        img_id = filename.split(".")[0]
        return img_id

    def dumpToJson(self, dir):
        # Sort according to assigned image id e.g.
        # imgPath = 'data/Cardcare_1/cc-1-4/72.jpeg'
        # image id = 72
        sorted_tuples = sorted(self.dumpDict.items(), key=lambda item: int(self.getImageID(item[1]['Image'])))
        sorted_dict = {k: v for k, v in sorted_tuples}

        with open(dir + '/dataDump.json', 'w', encoding='utf-8') as f:
            json.dump(sorted_dict, f, ensure_ascii=False, indent=4)

        # Free contents of the dictionary for the next batch of images
        sorted_dict.clear()
        self.dumpDict.clear()



