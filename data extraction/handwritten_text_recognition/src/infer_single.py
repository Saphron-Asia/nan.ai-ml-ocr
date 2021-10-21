import cv2
from DataLoaderIAM import DataLoaderIAM, Batch
from Model import Model, DecoderType
from SamplePreprocessor import preprocess
from FileLoader import FileLoader

from path import Path


def infer(model, fnImg):
    "recognize text in image provided by file path"
    img = preprocess(cv2.imread(fnImg, cv2.IMREAD_GRAYSCALE), Model.imgSize)
    batch = Batch(None, [img])
    # Pass image path as well
    (recognized, probability) = model.inferBatch(batch, True, imagePath=fnImg)
    print(f'Recognized: "{recognized[0]}"')
    print(f'Probability: {probability[0]}')

    return recognized[0], probability[0]


def main(input_dir, decoder):
    "filenames and paths to data"
    fnCharList = '../model/charList.txt'
    # fnSummary = '../model/summary.json'
    # fnCorpus = '../data/corpus.txt'

    # set chosen CTC decoder
    if decoder == 'bestpath':
        decoderType = DecoderType.BestPath
    elif decoder == 'beamsearch':
        decoderType = DecoderType.BeamSearch
    elif decoder == 'wordbeamsearch':
        decoderType = DecoderType.WordBeamSearch

    model = Model(open(fnCharList).read(), decoderType, mustRestore=True, dump=False)
    imgLoader = FileLoader(Path(input_dir))
    numImages = len(imgLoader.getImages())

    # For progress computation
    i = 0
    # For average probability computation
    cumSum = 0

    for imgPath in imgLoader.getImages():
        print("Inferring image: " + imgPath)
        word, proby = infer(model, imgPath)
        imgLoader.appendResToJson(i, imgPath, word, proby)
        print(f'Progress:  {"%.2f" % ((i+1)/numImages * 100)}% \t Processed {i+1}/{numImages} images. ')
        cumSum += proby
        i += 1

    print(f'Average Probability: {cumSum / i}')
    model.averages[input_dir] = cumSum / i
    imgLoader.dumpToJson(input_dir)
    model.log(input_dir)


if __name__ == '__main__':
    main(input_dir='/Users/joshuavillanueva/Data Analyst/Github/SAMPLE/output_wnn/output/Kabuklod_1/9.jpg',
         decoder='wordbeamsearch')
