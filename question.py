import sys
from wiki import *
import argparse
from question_generator import QuestionGenerator
from store_question_answer import *
from nltk import tokenize
from pymongo import MongoClient


def add_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '-page', type=str, help="The page from which questions are to be generated.")
    parser.add_argument('-t', '-question_type', type=str, default=['Wh', 'Are', 'Who', 'Do'], choices=['Wh', 'Are', 'Who', 'Do', 'All'], help='The types of questions to be generated.')
    return parser.parse_args()

if __name__ == '__main__':

    client = MongoClient(port=27017)
    db = client.AQE

    args = add_arguments()
    
    page_name = args.p
    q  = QuestionGenerator()

    text, url = findwiki(page_name)

    if len(list(db.topic.find({'link': url}))) == 0:
        print("Database successfully created")
        question_list = q.generate_question(text, args.t)
        store_qa(question_list, page_name, url, db)
    else:
        print("Database already exists")
        exit(2)

    # sentences = tokenize.sent_tokenize(text)
    # question_list = []
    # for sentence in sentences:
    #     questions = q.generate_question(sentence, args.t)
    #     for i in questions:
    #         question_list.append(i)

    # store_qa(question_list)
    # question_list = q.generate_question(text, args.t)
    # store_qa(question_list, page_name, url, db)
