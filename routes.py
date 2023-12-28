from flask import jsonify
from controllers.dataset_controller import upload_dataset, get_dataset,get_user_datasets
from controllers.Textual_controller import replaceString,removeHTML,removeSpecialCharacters,tokenize,lowercase,removeStopwords,stemming,lemmatization,removeDuplicates, spellChecking,cleanWithCustomPatterns,handleEncodingIssues,removeWhitespaces,getTextFromHTML,wordEmbedding
from controllers.Number_Controller import dropNull,LimiteValCol,replaceByLog_Transformation,replaceByMean,replaceByMedian,replaceByVal
from controllers.utils import token_required
from controllers.user_controller import signup, login


def init_app_routes(app):
    app.add_url_rule('/signup', 'signup', signup, methods=['POST'])
    app.add_url_rule('/login', 'login', login, methods=['POST'])
    app.add_url_rule('/upload', 'upload_dataset', upload_dataset, methods=['POST'])
    app.add_url_rule('/get_user_datasets', 'get_user_datasets', get_user_datasets, methods=['POST'])
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
    
    #routes Of numbers cleanning
    app.add_url_rule('/dropNull', 'dropNull', dropNull, methods=['POST'])  # Attributs : column,dataset_id
    app.add_url_rule('/replaceByMean', 'replaceByMean', replaceByMean, methods=['POST'])  # Attributs : column,dataset_id
    app.add_url_rule('/replaceByMedian', 'replaceByMedian', replaceByMedian, methods=['POST'])  # Attributs : column,dataset_id
    app.add_url_rule('/replaceByVal', 'replaceByVal', replaceByVal, methods=['POST'])  # Attributs : column,dataset_id,valeur
    app.add_url_rule('/LimiteValCol', 'LimiteValCol', LimiteValCol, methods=['POST'])  # Attributs : column,dataset_id,valeur1,valeur2 
    app.add_url_rule('/replaceByLog_Transformation','replaceByLog_Transformation', replaceByLog_Transformation, methods=['POST'])
    # Attributs : column,dataset_id
    
    
    
    
