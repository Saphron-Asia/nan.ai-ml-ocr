# Nan.ai Optical Character Recognition (OCR)

Nan.ai  is an open source machine learning service that extracts data from form images with handwritten inputs. This ML service is created to support Nan.ai, a grassroots agent platform for microinsurance. Nan.ai OCR ML service can be used for other use cases such as (insert examples here) and trained using the nan.ai OCR Open Data. This ML service is tailor fit for optimizing the workflow for Saphron.asia, however, as a public good it can be reused for other  scenarios in need of OCR service.

nan.ai OCR ML service has three components:

1. Validation - pre-processing component that adjusts image quality and identification of regions of interest
2. Extraction - data extraction workflow that segregates region of interest into input fields then recognizing and recording form inputs from handwriting
3. Encoding - annotation workflow that aids labelling datasets to improve the OCR model. Encoding inputs are used to improve autocorrect suggestions.

You can participate by (1) reporting bugs or (2) suggesting improvements on implementation. To explore our ML service, you can use the existing notebooks available here or export model by ``(insert instructions here)``.

Alongside our open source initiative, we are also open sourcing related datasets, nan.ai OCR Open [`Data`](https://github.com/Saphron-Asia/nan.ai-opendata-ocr), to help you explore and train this model.

## Description of the model

* **Data**

[![](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggVERcbiAgICBBWy9SYXcgSW1hZ2UvXSAtLT4gQlsqUm9JIG1vZHVsZV1cbiAgICBCIC0tPiB8RXh0cmFjdHMgcmVnaW9ucyBvZiBpbnRlcmVzdHwgQ1tXb3JkIERlY3RlY3RvciBOTl1cbiAgICBDIC0tPiB8RXh0cmFjdHMgc2luZ2xlIHdvcmRzfCBEW0hhbmR3cml0dGVuIFRleHQgUmVjb2duaXRpb24gTk5dXG4gICAgRCAtLT4gRVsvUmVjb2duaXplZCB3b3Jkcy9dIiwibWVybWFpZCI6eyJ0aGVtZSI6ImRlZmF1bHQifSwidXBkYXRlRWRpdG9yIjpmYWxzZSwiYXV0b1N5bmMiOnRydWUsInVwZGF0ZURpYWdyYW0iOmZhbHNlfQ)](https://mermaid-js.github.io/mermaid-live-editor/edit#eyJjb2RlIjoiZ3JhcGggVERcbiAgICBBWy9SYXcgSW1hZ2UvXSAtLT4gQlsqUm9JIG1vZHVsZV1cbiAgICBCIC0tPiB8RXh0cmFjdHMgcmVnaW9ucyBvZiBpbnRlcmVzdHwgQ1tXb3JkIERlY3RlY3RvciBOTl1cbiAgICBDIC0tPiB8RXh0cmFjdHMgc2luZ2xlIHdvcmRzfCBEW0hhbmR3cml0dGVuIFRleHQgUmVjb2duaXRpb24gTk5dXG4gICAgRCAtLT4gRVsvUmVjb2duaXplZCB3b3Jkcy9dIiwibWVybWFpZCI6IntcbiAgXCJ0aGVtZVwiOiBcImRlZmF1bHRcIlxufSIsInVwZGF0ZUVkaXRvciI6ZmFsc2UsImF1dG9TeW5jIjp0cnVlLCJ1cGRhdGVEaWFncmFtIjpmYWxzZX0)

We started with an initial model that is more generic and has been trained with the IAM dataset. This has been discussed further [here](https://github.com/Saphron-Asia/nan.ai-ml-ocr/tree/main/OCR/handwritten_text_recognition#train-model-with-iam-dataset). 
To tailor fit the model to our use case, we annotated our own data and used that to retrain the model. The input data is an image-text pair where the text is manually transcribed from the scanned image. Each image is in grayscale, 128 x 32 pixels, and contains a word. 
If the cropped image exceeds in size, it will be resized (without distortion) until it has a height of 128 px or a width of 32 px. All word images are then placed into an empty white canvas<sup>[1](https://towardsdatascience.com/build-a-handwritten-text-recognition-system-using-tensorflow-2326a3487cd5) </sup>. 

Moving forward, the model should be trainable with any kind of data. A detailed guide for annotating your data can be found here: [1.2 Create IAM-compatible dataset and train model](https://towardsdatascience.com/faq-build-a-handwritten-text-recognition-system-using-tensorflow-27648fb18519). 

* **Evaluation**

The **Connectionist Temporal Classification** (CTC) loss function is used to evaluate the output of the model (both training and inferring). 
Upon training, the CTC receives the RNN output matrix and the ground truth text from which the loss value is computed<sup>[1](https://towardsdatascience.com/build-a-handwritten-text-recognition-system-using-tensorflow-2326a3487cd5) </sup>. While inferring, the CTC only gets the character probability matrix and the final text is transcribed. The loss value is the negative log-likelihood of seeing the given text i.e. L=-log(P). 
If we feed the character-probability matrix and the recognized text to the loss function and afterward undo the log and the minus, we get the probability P of the recognized text: 
P=exp(-L)<sup>[2](https://towardsdatascience.com/faq-build-a-handwritten-text-recognition-system-using-tensorflow-27648fb18519) </sup>.

For the pre-trained model, evaluation is done using the IAM and Bentham HTR datasets. We also evaluated our model using our data.

* **Setup**

1. Clone this repository.
2. Install Python 3.8 + and dependencies from requirements.txt
    1. Tensorflow 2.4.0 or 2.6.0 
    1. Opencv-python 4.4.0.46 
    1. Opencv-contrib-python 4.5.1.48
    1. Pytesseract 0.3.8
    1. Tesseract 5.x
        1. Install tesseract on your environment: 
            1. https://tesseract-ocr.github.io/tessdoc/Compiling.html
        1. Install custom Python library (Word Beam Search) for the Handwritten Text Recognition model.
            1. https://github.com/githubharald/CTCWordBeamSearch
3. Download pre-trained models as instructed: 
    1. [Word Detector NN](https://github.com/Saphron-Asia/nan.ai-ml-ocr/tree/main/OCR/word_detector_nn#run-demo) 
    1. [HTR](https://github.com/Saphron-Asia/nan.ai-ml-ocr/tree/main/OCR/handwritten_text_recognition#run-demo) 
4. (Optional) For extracting regions of interest (RoI), you will need to provide a template (e.g. a form template). Provide three directories for the script: the **data**, **template**, and **output** directories. For a detailed description of these parameters, please refer [here](https://github.com/Saphron-Asia/nan.ai-ml-ocr/tree/main/data%20cleaning%20and%20normalization/regions_of_interest/roi_SIFT).
5. For the Word Neural Net (WNN):
    1. If you used the RoI, use the RoI’s output directory as input for the WNN.
    1. Otherwise, put image/s containing words/text inside a directory. Create a separate directory for the output.
6. For the Handwritten Text Recognition (HTR), pass the output from (5). After execution, each subdirectory will contain a `dataDump.json` file and all the results will be summarized in a single log file at the parent directory.


## Navigate this project
* [How this works](https://github.com/Saphron-Asia/nan.ai-ml-ocr/blob/main/HOWTO.md)
* [Sample data](https://github.com/Saphron-Asia/nan.ai-opendata-ocr/tree/main/sample%20data)
* [Contributing guidelines](https://github.com/Saphron-Asia/nan.ai-ml-ocr/blob/main/CONTRIBUTE.md) 
* [Code of conduct](https://github.com/Saphron-Asia/nan.ai-ml-ocr/blob/main/CODEOFCODUCT.md)

## Resources
* Documentation
* [Issue tracking](https://github.com/Saphron-Asia/nan.ai-ml-ocr/issues)
* [How to contribute data](https://github.com/Saphron-Asia/nan.ai-opendata-ocr/blob/main/CONTRIBUTE.md) 
* [nan.ai OCR Open Data](https://github.com/Saphron-Asia/nan.ai-opendata-ocr)

## References
<sup>1</sup>[Build a Handwritten Text Recognition System using TensorFlow](https://towardsdatascience.com/build-a-handwritten-text-recognition-system-using-tensorflow-2326a3487cd5) <br>
<sup>2</sup>[FAQ: Build a Handwritten Text Recognition System using TensorFlow](https://towardsdatascience.com/faq-build-a-handwritten-text-recognition-system-using-tensorflow-27648fb18519) <br>
<sup>3</sup>[Word Beam Search: A Connectionist Temporal Classification Decoding Algorithm](https://repositum.tuwien.ac.at/obvutwoa/download/pdf/2774578) <br>
<sup>4</sup>[Handwritten Word Detector](https://githubharald.github.io/word_detector.html)

## License
nanai-ml-ocr is licensed under the Apache License 2.0
