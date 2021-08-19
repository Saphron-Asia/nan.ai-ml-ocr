import json

class FileLoader:

    def __init__(self, fnInferDir):
        self.fn_imgs = fnInferDir.files('*.jpeg')
        self.dumpDict = {}

    def getImages(self):
        return self.fn_imgs

    def appendResToJson(self, currIdx, imgPath, word, probability):
        self.dumpDict[currIdx] = {"Image": imgPath, "Recognized": word, "Probability": str(probability)}

    def dumpToJson(self, dir):
        with open(dir + '/dataDump.json', 'w', encoding='utf-8') as f:
            json.dump(self.dumpDict, f, ensure_ascii=False, indent=4)
        # Free contents of the dictionary for the next batch of images
        self.dumpDict.clear()



