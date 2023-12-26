from flask import jsonify
from controllers.dataset_controller import upload_dataset, get_dataset,upload_dataset2
from controllers.Textual_controller import replaceString,removeHTML,removeSpecialCharacters,tokenize,lowercase,removeStopwords,stemming,lemmatization,removeDuplicates, spellChecking,cleanWithCustomPatterns,handleEncodingIssues,removeWhitespaces,getTextFromHTML,wordEmbedding

def init_app_routes(app):
    app.add_url_rule('/upload', 'upload_dataset', upload_dataset, methods=['POST'])
    app.add_url_rule('/upload2', 'upload_dataset2', upload_dataset2, methods=['POST'])
    app.add_url_rule('/get_dataset/<string:dataset_id>', 'get_dataset', get_dataset, methods=['GET'])
    app.add_url_rule('/replaceString', 'replaceString', replaceString, methods=['POST'])
    app.add_url_rule('/removeHTML', 'removeHTML', removeHTML, methods=['POST'])
    app.add_url_rule('/removeSpecialCharacters', 'removeSpecialCharacters', removeSpecialCharacters, methods=['POST'])
    app.add_url_rule('/tokenize', 'tokenize', tokenize, methods=['POST'])
    app.add_url_rule('/removeStopwords', 'removeStopwords', removeStopwords, methods=['POST'])
    app.add_url_rule('/stemming', 'stemming', stemming, methods=['POST'])
    app.add_url_rule('/lemmatization', 'lemmatization', lemmatization, methods=['POST'])
    app.add_url_rule('/removeDuplicates', 'removeDuplicates', removeDuplicates, methods=['POST'])
    app.add_url_rule('/spellChecking', 'spellChecking', spellChecking, methods=['POST'])
    app.add_url_rule('/cleanWithCustomPatterns', 'cleanWithCustomPatterns', cleanWithCustomPatterns, methods=['POST'])
    app.add_url_rule('/handleEncodingIssues', 'handleEncodingIssues', handleEncodingIssues, methods=['POST'])
    app.add_url_rule('/removeWhitespaces', 'removeWhitespaces', removeWhitespaces, methods=['POST'])
    app.add_url_rule('/getTextFromHTML', 'getTextFromHTML', getTextFromHTML, methods=['POST'])
    app.add_url_rule('/lowercase', 'lowercase', lowercase, methods=['POST'])
    app.add_url_rule('/wordEmbedding', 'wordEmbedding', wordEmbedding, methods=['POST'])
    #app.add_url_rule('/tfidf', 'tfidf', tfidf, methods=['POST'])
    
    
    
    
