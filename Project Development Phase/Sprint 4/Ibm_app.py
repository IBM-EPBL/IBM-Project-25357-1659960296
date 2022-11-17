import numpy as np
import os
from flask import Flask, request, render_template, url_for
from werkzeug.utils import secure_filename, redirect
from flask import send_from_directory
from joblib import Parallel,delayed
import joblib
import pandas as pd
from scipy.sparse import issparse
import requests 


# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "W5zK1ki_mpb4VeCgGLak0aqQVfl6wY4y4ZyfHw9F3S0l"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}


app = Flask(__name__)



@app.route('/')
def index():
    return render_template('home.html')

@app.route('/predict')
def predict():
    return render_template('predict.html')

@app.route('/result', methods=['GET', 'POST'])
def upload():
    if request.method == "POST":
        name= request.form.get('name')
        gender=request.form.get('gender')
        married=request.form.get('married')
        dependency=request.form.get('dep')
        education=request.form.get('edu')
        self_employed=request.form.get('se')
        applicant_income=request.form.get('ai')
        coapplicant_income=request.form.get('cai')
        loan_amount=request.form.get('la')
        loan_amount_term=request.form.get('lat')
        credit_history=request.form.get('ch')
        property_area=request.form.get('pa')

        dependency=int(dependency)

        if(str(gender)=="Male"):
            gender=1 
        else:
            gender=0 
        
        if (str(married)=="Yes"):
            married=1 
        else:
            married=0 

        if (str(education)=="Graduate"):
            education=0 
        else:
            education=1 

        if (str(self_employed)=="Yes"):
            self_employed=1 
        else:
            self_employed=0 

        coapplicant_income=float(coapplicant_income)
        applicant_income=int(applicant_income)
        loan_amount=float(loan_amount)
        loan_amount_term=float(loan_amount_term)
        if (str(credit_history)=="Yes"):
            credit_history=1 
        else:
            credit_history=0 

        if (str(property_area)=="Rural"):
            property_area=0 
        elif (str(property_area)=="Semi Urban"):
            property_area=1 
        else:
            property_area=2 

        df =[[gender,married,dependency,education,self_employed,applicant_income,coapplicant_income,loan_amount,loan_amount_term,credit_history,property_area]]
        # NOTE: manually define and pass the array(s) of values to be scored in the next line
        payload_scoring = {"input_data": [{"fields": [['gender','married','dependency','education','self_employed','applicant_income','coapplicant_income','loan_amount','loan_amount_term','credit_history','property_area']], "values":df}]}  
        response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/8b283bb9-ad08-4e67-a29d-5df0cb69a8e8/predictions?version=2022-11-16', json=payload_scoring,
        headers={'Authorization': 'Bearer ' + mltoken})
        print("response_scoring")
        predictions=response_scoring.json()
        num=predictions['predictions'][0]['values'][0][0]
        a=''
        if(num==0):
            a='Sorry {},Your are not elligible for getting loan'.format(name)
        else:
            a='Congratulations {},Your Loan application will be succesfull.'.format(name)
        return render_template('submit.html', num=a)


if __name__ == '__main__':
    app.run(debug=True, threaded=False)