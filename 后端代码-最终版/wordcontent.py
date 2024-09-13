import nltk
from nltk.corpus import wordnet as wn
from datetime import date, datetime
from nltk.corpus import sentiwordnet as swn
from text_model import process_text
import os
os.environ['NLTK_DATA'] = 'nltk_data'


def get_word_data(word):
    # Ensure the word is in English for compatibility with WordNet
    word = word if isinstance(word, str) and word.isascii() else ''

    word_data = {
        'antonyms': [],
        'definitions': [],
        'hypernyms': [],
        'hyponyms': [],
        'mean': [],
        'part_of_speech': [],
        'synonyms': []
    }

    # Check if the word exists in WordNet
    if not wn.synsets(word):
        return word_data

    # Get the first synset to extract the data
    synset = wn.synsets(word)[0]

    # Extract definitions
    word_data['definitions'] = [synset.definition()]

    # Extract part of speech
    word_data['part_of_speech'] = [synset.pos()]

    # Extract synonyms
    synonyms = set()
    for lemma in synset.lemmas():
        synonyms.add(lemma.name())
        if lemma.antonyms():
            word_data['antonyms'].append(lemma.antonyms()[0].name())
    word_data['synonyms'] = list(synonyms)

    # Extract hypernyms and hyponyms
    word_data['hypernyms'] = [hypernym.name() for hypernym in synset.hypernyms()]
    word_data['hyponyms'] = [hyponym.name() for hyponym in synset.hyponyms()]

    # Add the Chinese meaning if provided
    word_data['mean'] = process_text(word, "zh")
    # current_date = date.today()
    # now_time = datetime.combine(current_date, datetime.min.time())
    # insert_translation(word, word_data['mean'], now_time)

    return word_data


def format_output(data):
    # Helper function to format the list as a comma-separated string without brackets
    def format_list(lst):
        return ', '.join(lst) if lst else ''

    # Format each key in the dictionary
    formatted_data = {
        '中文释义:': data['mean'][0] if data['mean'] else '',
        '反义词:': format_list(data['antonyms']),
        '定义:': data['definitions'][0] if data['definitions'] else '',
        '上位词:': format_list(data['hypernyms']),
        '下位词:': format_list(data['hyponyms']),
        '词性:': data['part_of_speech'][0] if data['part_of_speech'] else '',
        '同义词:': format_list(data['synonyms'])
    }

    formatted_string = "\n".join(f"{key} {value}" for key, value in formatted_data.items())
    return formatted_string
