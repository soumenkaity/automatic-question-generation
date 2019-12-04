import gensim
from gensim.test.utils import datapath, get_tmpfile
from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
import string
import numpy as np
import math
import random
import re

nltk.download('maxent_ne_chunker')
nltk.download('words')

glove_file = '/home/cgi/Project/question-generation/glove.6B/glove.6B.300d.txt'
tmp_file = '/home/cgi/Project/question-generation/glove.6B/word2vec-glove.6B.300d.txt'

glove2word2vec(glove_file, tmp_file)
model = KeyedVectors.load_word2vec_format(tmp_file)

stop_words = set(stopwords.words('english'))
stop_words.add("'s")
punctuations = list(str(string.punctuation))

person = ['John Thomas', 'Robert Clinton', 'William Maxwell', 'Charles Page', 'David Hyland', 'James Hockey', 'Richard Mccullam', 'Johann Carry', 'George Flank', 'Paul Sernoty']
gpe = ['Boston', 'Texas', 'Bahrain', 'Phoenix', 'Michigan', 'Colombia', 'San Antonio', 'Montana', 'America', 'Germany']
organization = ['PeopleSoft', 'IBM', 'SAP', 'Sillicon Graphics', 'Red Hat Software', 'Intel', 'AMD', 'Nvidia', 'Best Buy', 'Apple']
programming_languages = ["Java", "C", "C++", "Python", "JavaScript", "VB .NET", "R", "PHP", "MATLAB", "COBOL", "Angular", "Angular JS", "Node JS"]

def generate_options(answer_phrases):
    all_options = []
    for answer in answer_phrases:
        all_options.append(creating_options(answer))
    return all_options
    

def creating_options(answer_phrase):
    word_tokens = word_tokenize(answer_phrase)
    stop_filtered_sentence = [w for w in word_tokens if not w in stop_words]
    filtered_sentence = [w for w in stop_filtered_sentence if not w in punctuations]

    part_of_speech_tags = nltk.pos_tag(filtered_sentence)
    named_ent = nltk.ne_chunk(part_of_speech_tags)

    named_entities = []
    for tagged_tree in named_ent:
        if hasattr(tagged_tree, 'label'):
            entity_name = ' '.join(c[0] for c in tagged_tree.leaves()) #
            entity_type = tagged_tree.label() # get NE category
            named_entities.append((entity_name, entity_type))

    replaced_words = {}
    for (x, y) in named_entities:
        for each_programming_language in programming_languages:
            if x.lower() == each_programming_language.lower():
                # filtered_sentence.remove(x)
                named_entities.remove((x,y))
                options_for_programming_language = []
                count = 0
                for p in programming_languages:
                    if count < 3:
                        if p != each_programming_language:
                            options_for_programming_language.append(p)
                            count = count + 1
                    else:
                        break
                replaced_words[x] = options_for_programming_language

    
    for (x, y) in named_entities:
        if y == 'PERSON':
            random.shuffle(person)
            replaced_words[x] = person[:3]
        elif y == 'GPE':
            random.shuffle(gpe)
            replaced_words[x] = gpe[:3]
        elif y == 'ORGANIZATION':
            random.shuffle(organization)
            replaced_words[x] = organization[:3]

    remaining_word_tokens = filtered_sentence
    for each_named_entity in replaced_words.keys():
        words_of_each_named_entity = word_tokenize(each_named_entity)
        for each_word_of_each_named_entity in words_of_each_named_entity:
            if each_word_of_each_named_entity in remaining_word_tokens:
                remaining_word_tokens.remove(each_word_of_each_named_entity)

    for w in remaining_word_tokens:
        for p in programming_languages:
            if w.lower() == p.lower():
                remaining_word_tokens.remove(w)
                options_for_programming_language = []
                count = 0
                for each_programming_language in programming_languages:
                    if count < 3:
                        if p != each_programming_language:
                            options_for_programming_language.append(each_programming_language)
                            count = count + 1
                    else:
                        break
                replaced_words[w] = options_for_programming_language

    for each_word in remaining_word_tokens:
        replaced_words[each_word] = create_distractors(each_word)

    # print(replaced_words)

    options = []
    options.append(answer_phrase)
    for i in range(3):
        new_option = answer_phrase
        for key, value in replaced_words.items():
            new_option = new_option.replace(key, value[i])
        options.append(new_option)

    random.shuffle(options)
    # print(options)
    return options


def create_distractors(answer, count=3):
    lower_cased_answer = answer.lower()
    
    ##Extracting closest words for the answer. 
    try:
        closestWords = model.most_similar(positive=[lower_cased_answer], topn=10)
    except:
        #In case the word is not in the vocabulary, or other problem not loading embeddings
        return [answer, answer, answer]

    #Return count many distractors
    distractors = list(map(lambda x: x[0], closestWords))[0:10]

    actual_distractors = []
    number_count = 0
    for each_distractor in distractors:
        if number_count < 3:
            if answer == each_distractor:
                continue
            else:
                out_each_distractor = re.sub('[%s]' % re.escape(string.punctuation), '', each_distractor)
                print(out_each_distractor)
                
                out_answer = re.sub('[%s]' % re.escape(string.punctuation), '', answer)
                out_answer_with_s = out_answer+'s'
                print(out_answer_with_s)

                if out_answer == out_each_distractor:
                    continue
                elif out_answer_with_s == out_each_distractor:
                    continue
                else:
                    actual_distractors.append(each_distractor)
                    number_count = number_count + 1
        else:
            break

    return actual_distractors

