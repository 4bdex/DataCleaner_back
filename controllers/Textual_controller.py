import re
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem import SnowballStemmer
from spellchecker import SpellChecker
from langdetect import detect
from flask import request, jsonify
from imblearn.over_sampling import SMOTE
from bs4 import BeautifulSoup
from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from controllers.dataset_controller import get_dataset, update_dataset




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
    
    
# Removing HTML Tags and Special Characters(dataset, column)
def removeHTML():
    try:
        data = request.get_json()
        dataset = data['dataset']
        column = data['column']
        
        for item in dataset:
            item[column] = re.sub(r'<.*?>', '', item[column])
        
        return jsonify({'message': 'HTML Tags and Special Characters removed successfully', 'dataset': dataset})
    except Exception as e:
        return jsonify({'message': str(e)})
    
    
#removing special characters (dataset, column)
def removeSpecialCharacters():
    try:
        data = request.get_json()
        dataset = data['dataset']
        column = data['column']
        
        for item in dataset:
            item[column] = re.sub(r'[^a-zA-Z0-9\s]', '', item[column])
        
        return jsonify({'message': 'Special Characters removed successfully', 'dataset': dataset})
    except Exception as e:
        return jsonify({'message': str(e)})



# tokenize column data (dataset, column)
def tokenize():
    try:
        data = request.get_json()
        dataset = data['dataset']
        column = data['column']
        
        for item in dataset:
            item[column] = word_tokenize(item[column])
        
        return jsonify({'message': 'Column data tokenized successfully', 'dataset': dataset})
    except Exception as e:
        return jsonify({'message': str(e)})

# Lowercase column data (dataset, column)
def lowercase():
    try:
        data = request.get_json()
        dataset = data['dataset']
        column = data['column']
        
        for item in dataset:
            item[column] = item[column].lower()
        
        return jsonify({'message': 'Column data converted to lowercase successfully', 'dataset': dataset})
    except Exception as e:
        return jsonify({'message': str(e)})
    
# remove stopwords (dataset, column, language) #language: english, french, german, spanish, arabic, russian
def removeStopwords():
    try:
        data = request.get_json()
        dataset = data['dataset']
        column = data['column']
        language = data['language']
        
        stop_words = set(stopwords.words(language))
        
        for item in dataset:
            item[column] = ' '.join([word for word in item[column].split() if word.lower() not in stop_words])
        
        return jsonify({'message': 'Stopwords removed successfully', 'dataset': dataset})
    except Exception as e:
        return jsonify({'message': str(e)})

#stemming column data (dataset, column, language)
def stemming():
    try:
        data = request.get_json()
        dataset = data['dataset']
        column = data['column']
        language = data['language']
        
        stemmer = SnowballStemmer(language)
        
        for item in dataset:
            stemmed_words = [stemmer.stem(word) for word in item[column].split()]
            item[column] = ' '.join(stemmed_words)
        
        return jsonify({'message': 'Column data stemmed successfully', 'dataset': dataset})
    except Exception as e:
        return jsonify({'message': str(e)})

# lemmatization column data (dataset, column)
def lemmatization():
    try:
        data = request.get_json()
        dataset = data['dataset']
        column = data['column']
        
        lemmatizer = WordNetLemmatizer()
        
        for item in dataset:
            tokenized_words = word_tokenize(item[column])
            lemmatized_words = [lemmatizer.lemmatize(word) for word in tokenized_words]
            item[column] = ' '.join(lemmatized_words)
        
        return jsonify({'message': 'Column data lemmatized successfully', 'dataset': dataset})
    except Exception as e:
        return jsonify({'message': str(e)})


# remove duplicate text (dataset, column) ## isnt working
def removeDuplicates():
    try:
        data = request.get_json()
        dataset = data['dataset']
        column = data['column']
        for row in dataset:
            row[column] = list(set(row[column]))
        return jsonify({'message': 'Duplicate text removed successfully', 'dataset': dataset})
    except Exception as e:
        return jsonify({'message': str(e)})


# Dealing with Noisy Text
# column Language Identification(dataset, column) 
def languageIdentification(dataset, column):
    pass
    
# spell checking(dataset, column, language) language: auto, en, fr, de, es , de, ru, ar. this doesn't work
def spellChecking():
    pass



# clean with custom patterns (dataset, column, pattern)
def cleanWithCustomPatterns():
    try:
        data = request.get_json()
        dataset = data['dataset']
        column = data['column']
        pattern = data['pattern']
        
        for item in dataset:
            item[column] = re.sub(pattern, '', item[column])
        
        return jsonify({'message': 'Column data cleaned with custom patterns successfully', 'dataset': dataset})
    
    except Exception as e:
        return jsonify({'message': str(e)})

    
    
# handle encoding issues (dataset, column, encoding,errors) #encoding: utf-8, ascii, latin-1,utf_16,utf_32 #errors: strict, ignore, replace,backslashreplace
def handleEncodingIssues():
    try:
        data = request.get_json()
        dataset = data['dataset']
        column = data['column']
        encoding = data['encoding']
        errors = data['errors']
        for item in dataset:
            item[column] = item[column].encode(encoding, errors=errors).decode(encoding)
        
        return jsonify({'message': 'Encoding issues handled successfully', 'dataset': dataset})
    
    except Exception as e:
        return jsonify({'message': str(e)})

    
    
# remove whitespaces (dataset, column)
def removeWhitespaces():
    try:
        data = request.get_json()
        dataset = data['dataset']
        column = data['column']
        for row in dataset:
            # Remove leading and trailing whitespaces
            row[column] = row[column].strip()
            # Replace multiple spaces with a single space
            row[column] = re.sub(r'\s+', ' ', row[column])
        return jsonify({'message': 'Whitespaces removed successfully', 'dataset': dataset})
    except Exception as e:
        return jsonify({'message': str(e)})
    
# get text from html with beatifulsoup (dataset, column) 
def getTextFromHTML():
    try:
        data = request.get_json()
        dataset = data['dataset']
        column = data['column']
        
        for row in dataset:
            row[column] = BeautifulSoup(row[column], 'html.parser').get_text()
        return jsonify({'message': 'Text extracted from HTML successfully', 'dataset': dataset})
    except Exception as e:
        return jsonify({'message': str(e)})



# TF-IDF 
def tfidf():
    try:
        data = request.get_json()
        dataset = data['dataset']
        column = data['column']
        vectorizer = TfidfVectorizer()
        for row in dataset:
            text = row[column]
            tfidf = vectorizer.fit_transform(text)
            row[column] = tfidf
        return jsonify({'message': 'TF-IDF performed successfully', 'dataset': dataset})
    except Exception as e:
        return jsonify({'message': str(e)})
    
    
# word embedding (dataset, column, embedding) #embedding: word2vec, tfidf, bag of words
def wordEmbedding():
    try:
        data = request.get_json()
        dataset = data['dataset']
        column = data['column']
        embedding = data['embedding']
        
        # if embedding == 'word2vec':
        #     model = Word2Vec.load('models/word2vec.bin')  # Load Word2Vec model
        #     for row in dataset:
        #         text = row[column]
        #         word_embeddings = []
        #         for word in text.split():
        #             if word in model:
        #                 word_embeddings.append(model[word])
        #             else:
        #                 word_embeddings.append([0.0] * 100)  # Replace with the embedding dimension of your Word2Vec model
        #         row[column] = word_embeddings
        
        if embedding == 'bag of words':
            text_data = [item[column] for item in dataset]
            vectorizer = CountVectorizer()
            bag_of_words = vectorizer.fit_transform(text_data).toarray().tolist()
            for i, item in enumerate(dataset):
                item[column] = bag_of_words[i]  # Compute bag-of-words embeddings
        
        elif embedding == 'tfidf':
            text_data = [item[column] for item in dataset]
            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform(text_data).toarray().tolist()
            for i, item in enumerate(dataset):
                item[column] = tfidf_matrix[i]  # Compute TF-IDF embeddings
        
        return {'message': 'Word embedding performed successfully', 'dataset': dataset}
    
    except Exception as e:
        return {'message': str(e)}



    




# balace text data with smote


# #multiprocessing
# # from multiprocessing import Pool

# # def parallel_process_text(data, cleaning_function, num_workers):
# #     with Pool(num_workers) as pool:
# #         cleaned_data = pool.map(cleaning_function, data)
# #     return cleaned_data


    


