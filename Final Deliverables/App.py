import numpy as np
import os
from flask import Flask, request, render_template, url_for
from werkzeug.utils import secure_filename, redirect
from flask import send_from_directory
from joblib import Parallel,delayed
import joblib
import pandas as pd
from scipy.sparse import issparse
from sklearn.preprocessing import MaxAbsScaler




app = Flask(__name__)

scaler=MaxAbsScaler()

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

        gender=int(gender) 
        married=int(married)
        dependency=int(dependency)
        education=int(education)
        self_employed=int(self_employed)
        applicant_income=int(applicant_income)
        coapplicant_income=float(coapplicant_income)
        loan_amount=float(loan_amount)
        loan_amount_term=float(loan_amount_term)
        credit_history=int(credit_history)
        property_area=int(property_area)

        d=[[gender,married,dependency,education,self_employed,applicant_income,coapplicant_income,loan_amount,loan_amount_term,credit_history,property_area]]
        gh=joblib.load('model.pkl')
        df=scaler.fit_transform(d)
        num=gh.predict(df)
        a=''
        if(num==0):
            a='Sorry {},Your are not elligible for getting loan'.format(name)
        else:
            a='Congratulations {},Your Loan application will be succesfull.'.format(name)
        
        return render_template('submit.html', num=a)       


if __name__ == '__main__':
    app.run(debug=True, threaded=False)