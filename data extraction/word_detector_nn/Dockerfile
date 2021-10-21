FROM python:3.7-stretch
LABEL MAINTAINER="jvillanueva@agsx.net"

# install build utilities
RUN apt-get update && \
	apt-get install -y gcc make apt-transport-https ca-certificates build-essential

# set the working directory for containers
WORKDIR  /usr/src/WordDetectorNN

# Installing python dependencies
COPY OCR/word_detector_nn/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY OCR/word_detector_nn/ word_detector_nn/
RUN ls -la word_detector_nn/*

# Running Python Application
# args --data_dir, --output_dir
CMD ["python3", "OCR/word_detector_nn/src/infer.py"]
