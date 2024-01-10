import numpy as np
import pandas as pd
import json
from flask import request, jsonify
from controllers.dataset_controller import get_dataset,update_dataset

#--------------------------------------------------------------------------PLAN---------------------------------------------------------------------

# replace zero or null by :
#    moyenne                 
#    mediane                 
#    valeur donner           
#    suppression des rows    
#    min , max colonne       
#    Rows log Transformation      
# dropDuplicates
# parseToInt
# RoundingAndPrecision

#---------------------------------------------------------------------------------------------------------------------------------------------------
import warnings
warnings.filterwarnings('ignore')

#-----------------------------------------------Droping missing value rows-------------------------------------------------------------------------
def dropNull():
    try:
        data = request.get_json()
        dataset_id = data['dataset_id']
        dataset = get_dataset(dataset_id)
        dataset = pd.DataFrame(dataset)
        dataset = dataset.dropna(subset=["age"])
        dataset = dataset.to_dict('records')
        update_dataset(dataset_id, dataset)
        return jsonify({'message': 'Null values dropped successfully', 'dataset': dataset[:50]})
    except Exception as e:
        return jsonify({'error': str(e)})
      
#print(dropNull(data,'cabin'))
#-------------------------------------------------Moyenne------------------------------------------------------------------------------------------
def replaceByMean():
    try:
        data = request.get_json()
        col=data['column']
        dataset_id=data['dataset_id']
        data2 = pd.json_normalize(get_dataset(dataset_id))
        data2[col]=data2[col].fillna(data2[col].mean())
        update_dataset(dataset_id, data2) 
        return jsonify({'data':json.loads(data2.to_json(orient='records'))})
        
    except Exception as e:
        return jsonify({'message': str(e)})  
#print(replaceMean(data,'age'))
#--------------------------------------------------------------Medianne---------------------------------------------------------------------------------
def replaceByMedian():
    try:
        data = request.get_json()
        col=data['column']
        dataset_id=data['dataset_id']
        data2 = pd.json_normalize(get_dataset(dataset_id))
        data2[col] = data2[col].fillna(data2[col].median())
        update_dataset(dataset_id, data2) 
        return jsonify({'data':json.loads(data2.to_json(orient='records'))})
       
    except Exception as e:
        return jsonify({'message': str(e)})
      
#print(replaceMedian(data,'cabin'))
#--------------------------------------------------------------Remplacer par une valeur--------------------------------------------------
def replaceByVal():
    try:
        data = request.get_json()
        valeur=data['valeur']
        col=data['column']
        dataset_id=data['dataset_id']
        data2 = pd.json_normalize(get_dataset(dataset_id))
        data2[col]=data2[col].fillna(valeur)
        update_dataset(dataset_id, data2) 
        return jsonify({'data':json.loads(data2.to_json(orient='records'))})
            
          
    except Exception as e:
        return jsonify({'message': str(e)})
     

#print(replaceByVal(data,'age',66))
#-----------------------------------------------------------Min,Max d'une colonne----------------------------------------------------------------
def LimiteValCol():
    try:
        data=request.get_json()
        col=data['column']
        valeur1=data['valeur1']
        valeur2=data['valeur2']
        dataset_id=data['dataset_id']
        data2 = pd.json_normalize(get_dataset(dataset_id))
        
        data2[col] = pd.to_numeric(data2[col], errors='coerce')
        #data2[col] = data2[col].fillna(0)
        data2[col] = data2[col].clip(lower=valeur1, upper=valeur2)
        update_dataset(dataset_id, data2) 
        return jsonify({'data':json.loads(data2.to_json(orient='records'))})
           
        
        
    except Exception as e:
        return jsonify({'exception': str(e)})
     

#print(min_max_col(data,'age',18,40))
#----------------------------------log transformation-------------------------------------------------------------
def replaceByLog_Transformation():
    try:
        data = request.get_json()
        col=data['column']
        dataset_id=data['dataset_id']
        data2 = pd.json_normalize(get_dataset(dataset_id))
        data2[col] = np.log1p(data2[col])
        update_dataset(dataset_id, data2) 
        return jsonify({'data':json.loads(data2.to_json(orient='records'))})
    except Exception as e:
        return jsonify({'data':json.loads(data2.to_json(orient='records'))})
          
#print(log_Transformation(data,'age'))

def dropDuplicates():
    try:
        data = request.get_json()
        col=data['column']
        dataset_id=data['dataset_id']
        data2 = get_dataset(dataset_id)
        #data2 = data2.dropna(subset=[col])
        data2 = pd.json_normalize(get_dataset(dataset_id))
        data2.drop_duplicates(subset=col,inplace=True)
        update_dataset(dataset_id, data2) 
        return jsonify({'data':json.loads(data2.to_json(orient='records'))})
    except Exception as e:
        return jsonify({'message': str(e)})
   
#print(log_Transformation(data,'age'))


def RoundingAndPrecision():
    try:
        data = request.get_json()
        col=data['column']
        dataset_id=data['dataset_id']
        decimale=data['decimale']
        data2 = pd.json_normalize(get_dataset(dataset_id))
        data2[col]=data2[col].round(decimals=decimale)
        update_dataset(dataset_id, data2) 
        return jsonify({'data':json.loads(data2.to_json(orient='records'))})
    except Exception as e:
        return jsonify({'message': str(e)})
    


def parseToInt():
    try:
        data = request.get_json()
        col=data['column']
        dataset_id=data['dataset_id']
        data2 = pd.json_normalize(get_dataset(dataset_id))
        data2=data2.dropna(subset=[col])
        data2[col]=data2[col].astype(int)
        update_dataset(dataset_id, data2) 
        return jsonify({'data':json.loads(data2.to_json(orient='records'))})
    except Exception as e:
        return jsonify({'message': str(e)})