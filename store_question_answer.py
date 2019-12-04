import csv
# from pymongo import MongoClient
from nltk.corpus import stopwords
from datetime import datetime
from options_generator import *

# client = MongoClient(port=27017)
# db = client.aqe

stop_words = set(stopwords.words('english'))

def store_qa(questions, page_name, url, db):
	with open('question_answer.csv', 'w') as writeFile:
		all_questions = []
		all_answers = []
		answer_phrases = []
		all_scores = []

		for i in questions:
			values = []
			for key, value in i.items():
				values.append(value)
			all_questions.append(values[0])
			all_answers.append(values[1])
			answer_phrases.append(values[2])
			all_scores.append(values[3])
		
		all_options = generate_options(answer_phrases)

		topic_data = {
			'name': page_name,
			'link': url,
			'createdAt': str(datetime.now())
		}

		db.topic.insert_one(topic_data)
		
		count = 0
		for i in range(len(all_questions)):

			if count >= 0 and count < 66:
				difficulty = 'E'
			elif count >= 66 and count < 132:
				difficulty = 'M'
			elif count >= 132 and count < 200:
				difficulty = 'H'
			else:
				break


			if answer_phrases[i] == 'i. e.':
				continue

			lower_answer_phrase = answer_phrases[i].lower()
			answer_words = set(lower_answer_phrase.split(" "))
			if(answer_words.issubset(stop_words)):
				continue

			row = []
			row.append(all_questions[i])
			row.append(answer_phrases[i])
			row.append(all_answers[i])
			row.append(all_scores[i])
			row.append(all_options[i])

			print(row)
			
			writer = csv.writer(writeFile)
			writer.writerow(row)

			each_data = {
				'question': all_questions[i],
				'answer': answer_phrases[i],
				'sentence': all_answers[i],
				'score': all_scores[i],
				'choices': all_options[i],
				'difficulty': difficulty,
				'correctAttempts': 0,
				'totalOccurrences': 0
			}

			result=db[page_name].insert_one(each_data)

			count = count + 1