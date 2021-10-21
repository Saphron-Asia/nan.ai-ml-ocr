import os
import numpy as np
import cv2


class DataProvider():
    "this class creates machine-written text for a word list. TODO: change getNext() to return your samples."

    def __init__(self, wordList):
        self.wordList = wordList
        self.idx = 0

    def hasNext(self):
        "are there still samples to process?"
        return self.idx < len(self.wordList)

    def getNext(self):
        "TODO: return a sample from your data as a tuple containing the text and the image"
        img = np.ones((32, 128), np.uint8) * 255
        word = self.wordList[self.idx]
        self.idx += 1
        cv2.putText(img, word, (2, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0), 1, cv2.LINE_AA)
        return (word, img)


def createIAMCompatibleDataset(dataProvider):
    "this function converts the passed dataset to an IAM compatible dataset"

    # create files and directories
    f = open('words.txt', 'w+')
    if not os.path.exists('sub'):
        os.makedirs('sub')
    if not os.path.exists('sub/sub-sub'):
        os.makedirs('sub/sub-sub')

    # go through data and convert it to IAM format
    ctr = 0
    while dataProvider.hasNext():
        sample = dataProvider.getNext()

        # write img
        cv2.imwrite('sub/sub-sub/sub-sub-%d.png' % ctr, sample[1])

        # write filename, dummy-values and text
        line = 'sub-sub-%d' % ctr + ' X X X X X X X ' + sample[0] + '\n'
        f.write(line)

        ctr += 1


if __name__ == '__main__':
    words = ['some', 'words', 'for', 'which', 'we', 'create', 'text-images']
    dataProvider = DataProvider(words)
    createIAMCompatibleDataset(dataProvider)