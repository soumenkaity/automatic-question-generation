FROM python:3.7.5

ADD . /pythonapp

RUN pip3 install nltk && \
	pip3 install Wikipedia-API && \
	python3 -m nltk.downloader punkt

WORKDIR /pythonapp

CMD [ "python3", "question.py"]