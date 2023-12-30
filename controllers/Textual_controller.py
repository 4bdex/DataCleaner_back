import re
import pandas as pd
import json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem import SnowballStemmer
from spellchecker import SpellChecker
from langdetect import detect
from flask import request, jsonify
from imblearn.over_sampling import SMOTE
from bs4 import BeautifulSoup
from gensim.models import Word2Vec
from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from controllers.dataset_controller import get_dataset, update_dataset
import nltk




# replace string in a column data (dataset_id, column, oldString, newString) and update in mongo database
def replaceString():
    try:
        data = request.get_json()
        dataset_id = data['dataset_id']
        column = data['column']
        oldString = data['oldString']
        newString = data['newString']
        dataset = get_dataset(dataset_id)
        for item in dataset:
            item[column] = item[column].replace(oldString, newString)
        update_dataset(dataset_id, dataset)
        return jsonify({'message': 'String replaced successfully', 'dataset': dataset[:50]})
    except Exception as e:
        return jsonify({'message': str(e)})
    
    
# # Removing HTML Tags and Special Characters(dataset_id, column)
# def removeHTML():
#     try:
#         data = request.get_json()
#         dataset_id = data['dataset_id']
#         column = data['column']
#         dataset = get_dataset(dataset_id)
#         for item in dataset:
#             item[column] = re.sub(r'<.*?>', '', item[column])
#         update_dataset(dataset_id, dataset)
#         return jsonify({'message': 'HTML Tags and Special Characters removed successfully', 'dataset': dataset[:50]})
#     except Exception as e:
#         return jsonify({'message': str(e)})
    
    
#removing special characters (dataset_id, column)
def removeSpecialCharacters():
    try:
        data = request.get_json()
        dataset_id = data['dataset_id']
        column = data['column']
        dataset= get_dataset(dataset_id)
        for item in dataset:
            item[column] = re.sub(r'[^a-zA-Z0-9\s]', '', item[column])
        update_dataset(dataset_id, dataset)
        return jsonify({'message': 'Special Characters removed successfully', 'dataset': dataset[:50]})
    except Exception as e:
        return jsonify({'message': str(e)})



# tokenize column data (dataset_id, column)
def tokenize():
    try:
        data = request.get_json()
        dataset_id = data['dataset_id']
        column = data['column']
        dataset = get_dataset(dataset_id)
        nltk.download('punkt')
        for item in dataset:
            item[column] = nltk.word_tokenize(item[column])
        update_dataset(dataset_id, dataset)
        return jsonify({'message': 'Column data tokenized successfully', 'dataset': dataset[:50]})
    except Exception as e:
        return jsonify({'message': str(e)})

# Lowercase column data (dataset_id, column)
def lowercase():
    try:
        data = request.get_json()
        dataset_id = data['dataset_id']
        column = data['column']
        dataset = get_dataset(dataset_id)
        for item in dataset:
            item[column] = item[column].lower()
        update_dataset(dataset_id, dataset)
        return jsonify({'message': 'Column data converted to lowercase successfully', 'dataset': dataset[:50]})
    except Exception as e:
        return jsonify({'message': str(e)})
    
# remove stopwords (dataset_id, column, language) #language: english, french, german, spanish, arabic, russian
def removeStopwords():
    try:
        data = request.get_json()
        dataset_id = data['dataset_id']
        column = data['column']
        language = data['language']
        stop_words = set(stopwords.words(language))
        dataset= get_dataset(dataset_id)
        for item in dataset:
            item[column] = ' '.join([word for word in item[column].split() if word.lower() not in stop_words])
        update_dataset(dataset_id, dataset)
        return jsonify({'message': 'Stopwords removed successfully', 'dataset': dataset[:50]})
    except Exception as e:
        return jsonify({'message': str(e)})

#stemming column data (dataset_id, column, language)
def stemming():
    try:
        data = request.get_json()
        dataset_id = data['dataset_id']
        column = data['column']
        language = data['language']
        stemmer = SnowballStemmer(language)
        dataset = get_dataset(dataset_id)
        for item in dataset:
            stemmed_words = [stemmer.stem(word) for word in item[column].split()]
            item[column] = ' '.join(stemmed_words)
        update_dataset(dataset_id, dataset)
        return jsonify({'message': 'Column data stemmed successfully', 'dataset': dataset[:50]})
    except Exception as e:
        return jsonify({'message': str(e)})

# lemmatization column data (dataset_id, column)
def lemmatization():
    try:
        data = request.get_json()
        dataset_id = data['dataset_id']
        column = data['column']
        lemmatizer = WordNetLemmatizer()
        dataset = get_dataset(dataset_id)
        for item in dataset:
            tokenized_words = word_tokenize(item[column])
            lemmatized_words = [lemmatizer.lemmatize(word) for word in tokenized_words]
            item[column] = ' '.join(lemmatized_words)
        update_dataset(dataset_id, dataset)
        return jsonify({'message': 'Column data lemmatized successfully', 'dataset': dataset[:50]})
    except Exception as e:
        return jsonify({'message': str(e)})


# remove duplicate text (dataset_id, column) ## isnt working
def removeDuplicatesInRow():
    try:
        data = request.get_json()
        dataset_id = data['dataset_id']
        column = data['column']
        dataset = get_dataset(dataset_id)

        for row in dataset:
            words = row[column].split()  # Split the text into words
            unique_words = []

            seen_words = set()
            for word in words:
                if word not in seen_words:
                    unique_words.append(word)
                    seen_words.add(word)

            row[column] = ' '.join(unique_words)  # Join unique words back into a string

        update_dataset(dataset_id, dataset)
        return jsonify({'message': 'Duplicate words removed successfully', 'dataset': dataset[:50]})
    except Exception as e:
        return jsonify({'message': str(e)})


# Dealing with Noisy Text
# column Language Identification
def languageIdentification(dataset, column):
    pass
    
# spell checking(dataset_id, column, language) language: auto, en, fr, de, es , de, ru, ar. this doesn't work
def spellChecking():
    pass



# clean with custom patterns (dataset_id, column, pattern)
def cleanWithCustomPatterns():
    try:
        data = request.get_json()
        dataset_id = data['dataset_id']
        column = data['column']
        pattern = data['pattern']
        dataset = get_dataset(dataset_id)
        
        for item in dataset:
            item[column] = re.sub(pattern, '', item[column])
        
        update_dataset(dataset_id, dataset)
        return jsonify({'message': 'Column data cleaned with custom patterns successfully', 'dataset': dataset[:50]})
    
    except Exception as e:
        return jsonify({'message': str(e)})

    
    
# handle encoding issues (dataset_id, column, encoding,errors) #encoding: utf-8, ascii, latin-1,utf_16,utf_32 #errors: strict, ignore, replace,backslashreplace
def handleEncodingIssues():
    try:
        data = request.get_json()
        dataset_id = data['dataset_id']
        column = data['column']
        encoding = data['encoding']
        errors = data['errors']
        dataset = get_dataset(dataset_id)
        for item in dataset:
            item[column] = item[column].encode(encoding, errors=errors).decode(encoding)
        update_dataset(dataset_id, dataset)
        return jsonify({'message': 'Encoding issues handled successfully', 'dataset': dataset[:50]})
    
    except Exception as e:
        return jsonify({'message': str(e)})

    
    
# remove whitespaces (dataset_id, column)
def removeWhitespaces():
    try:
        data = request.get_json()
        dataset_id = data['dataset_id']
        column = data['column']
        dataset = get_dataset(dataset_id)
        for row in dataset:
            # Remove leading and trailing whitespaces
            row[column] = row[column].strip()
            # Replace multiple spaces with a single space
            row[column] = re.sub(r'\s+', ' ', row[column])
            
        update_dataset(dataset_id, dataset)
        return jsonify({'message': 'Whitespaces removed successfully', 'dataset': dataset[:50]})
    except Exception as e:
        return jsonify({'message': str(e)})
    
# get text from html with beatifulsoup (dataset_id, column) 
def getTextFromHTML():
    try:
        data = request.get_json()
        dataset_id = data['dataset_id']
        column = data['column']
        dataset = get_dataset(dataset_id)
        for row in dataset:
            row[column] = BeautifulSoup(row[column], 'html.parser').get_text()
        update_dataset(dataset_id, dataset)
        return jsonify({'message': 'Text extracted from HTML successfully', 'dataset': dataset[:50]})
    except Exception as e:
        return jsonify({'message': str(e)})

    
# word embedding (dataset_id, column, embedding) #embedding: word2vec, TF-IDF, bag of words
def wordEmbedding():
    try:
        data = request.get_json()
        dataset_id = data['dataset_id']
        column = data['column']
        embedding = data['embedding']
        dataset = get_dataset(dataset_id)
        
        if embedding == 'word2vec':            
            text_data = [item[column] for item in dataset]
            word_lists = [TextBlob(text).words for text in text_data]
            model = Word2Vec(word_lists, min_count=1) 
            for i, item in enumerate(dataset):
                word_vectors = []
                for word in word_lists[i]:
                    try:
                        word_vector = model.wv[word]
                        word_vectors.append(word_vector)
                    except:          
                        return {'message': '{} not in vocabulary. Consider using a different word embedding.'.format(word)}
                item[column] = word_vectors
            update_dataset(dataset_id, dataset)
            print("updated")
            return json.loads(json.dumps({'message': 'Word embedding performed successfully', 'dataset': dataset[:50]}, default=lambda x: x.tolist()))
        
        
        elif embedding == 'bag of words':
            text_data = [item[column] for item in dataset]
            vectorizer = CountVectorizer()
            bag_of_words = vectorizer.fit_transform(text_data).toarray().tolist()
            for i, item in enumerate(dataset):
                item[column] = bag_of_words[i]
        
        elif embedding == 'TF-IDF':
            text_data = [item[column] for item in dataset]
            if isinstance(text_data[0], list):
                text_data = [' '.join(item) for item in text_data]
            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform(text_data).toarray().tolist()
            for i, item in enumerate(dataset):
                item[column] = tfidf_matrix[i]
        
        print("before")
        update_dataset(dataset_id, dataset)
        print("after")
        return {'message': 'Word embedding performed successfully', 'dataset': dataset[:50]}
    
    except Exception as e:
        return {'message': str(e)}