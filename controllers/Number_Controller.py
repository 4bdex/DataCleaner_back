import numpy as np
import pandas as pd
import json
from flask import request, jsonify
from controllers.dataset_controller import get_dataset

#--------------------------------------------------------------------------PLAN---------------------------------------------------------------------

#replace zero or null by :
#    moyenne                 V
#    mediane                 V
#    valeur donner           V
#    suppression des rows    V
#    min , max colonne       V
#    log Transformation      V

#---------------------------------------------------------------------------------------------------------------------------------------------------
import warnings
warnings.filterwarnings('ignore')

#-----------------------------------------------Droping missing value rows-------------------------------------------------------------------------
def dropNull():
    try:
        data = request.get_json()
        col=data['column']
        dataset_id=data['dataset_id']
        data2 = pd.json_normalize(get_dataset(dataset_id))
        data2 = data2.dropna(subset=[col])
        return jsonify({'data':json.loads(data2.to_json(orient='records'))})
    except Exception as e:
        return jsonify({'message': str(e)})
      
#print(dropNull(data,'cabin'))
#-------------------------------------------------Moyenne------------------------------------------------------------------------------------------
def replaceByMean():
    try:
        data = request.get_json()
        col=data['column']
        dataset_id=data['dataset_id']
        data2 = pd.json_normalize(get_dataset(dataset_id))
        data2[col] = pd.to_numeric(data[col], errors='coerce')
        data2[col] = data2[col].fillna(data2[col].mean())
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
        data2[col] = pd.to_numeric(data[col], errors='coerce')
        data2[col] = data2[col].fillna(data2[col].median())
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
        data2[col] = pd.to_numeric(data[col], errors='coerce')
        data2[col] = data[col].fillna(valeur)
                
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
        #data2[col] = data2[col].astype(int)
        data2[col] = data2[col].clip(lower=valeur1, upper=valeur2)
                
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
        data2[col] = pd.to_numeric(data[col], errors='coerce')
        data2[col] = np.log1p(data2[col])
        return data2
    except Exception as e:
        return jsonify({'data':json.loads(data2.to_json(orient='records'))})
        
#print(log_Transformation(data,'age'))