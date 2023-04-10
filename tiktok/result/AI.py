

# # import
import sys

import numpy as np 
import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import gender_guesser.detector as gender
import matplotlib.pyplot as plt 
from datetime import datetime
from sklearn import metrics
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import get_inpute_data 
import csv
import joblib
import os
# # load data
def run():
    data = pd.read_csv('./cleandata.csv')
    # x=data.loc[:,['statuses' , 'date_joined' , 'most_recent_post' , 'following' , 'followers' , 'likes', 'retweet' , 'retweeted_count'  ,'avg_tweets_by_hour_of_day', 'avg_tweets_by_day_of_week']]
    x=data.iloc[:, :-1]
    y = data.account_type.values.tolist()
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42,stratify=y)
    clf=RandomForestClassifier()
    clf.fit(x_train,y_train)
    y_pred_train = clf.predict(x_train)
    y_pred_test = clf.predict(x_test)
    joblib.dump(clf, "clf.pkl")
    return {"message":"done","Training Accuracy score":metrics.accuracy_score(y_train, y_pred_train),"Testing Accuracy score":metrics.accuracy_score(y_test, y_pred_test)}

def rerun():  
    try:
        accounts=pd.read_csv('./accounts.csv')
    except :
        return {"message":"there is nothing to add"}
    data = pd.read_csv('./datavf.csv')
    accounts['screen_name'] = accounts['screen_name'].astype(str).str.lower()
    data['screen_name'] = data['screen_name'].astype(str).str.lower()
    ac=accounts[~accounts['screen_name'].isin(data['screen_name'])]
    ac=ac.drop(['predict_proba'],axis=1)
    ac.to_csv('./datavf.csv', mode='a', header=False, index=False)
    os.remove('./accounts.csv')
    return run()

def predicte(name,access_key,access_secret):
    
    # data = pd.read_csv('./featuresfloatvf.csv')
    # column_names = data.columns.tolist()
    try:
        accounts=pd.read_csv('./accounts.csv')
        accounts['screen_name'] = accounts['screen_name'].astype(str).str.lower()
        dp = accounts[accounts['screen_name']==str.lower(name)]
        x=0
        # print(dp.shape[0])
        if dp.shape[0] == 0:
            x=1
        else :
            # print("accounts exist")
            ac = dp.iloc[0]
            r={"result":"bot" if str(ac['account_type']) == "0" else "human","proba":str(ac['predict_proba']),"score":str(ac['predict_proba']*5)}
            return r            
    except Exception as e:
         # print("Exception file dosen't exist")
         x=-1
    account=get_inpute_data.get_details(name,access_key,access_secret)
    # print(account)
    if 'message' in account:
        return account
    dp=pd.DataFrame(account, index=[0])
    dp1=dp.drop('screen_name',axis=1)
    try:
        clf=joblib.load("clf.pkl")
    except:
        run()
    predicted=clf.predict(dp1)
    predict_proba=clf.predict_proba(dp1)[:,1]
    dp1['account_type']=predicted
    dp1['predict_proba']=predict_proba
    dp1['screen_name']=dp['screen_name']
    if x ==1:
        dp1.to_csv('./accounts.csv', mode='a', header=False, index=False)
    elif x == -1:
         dp1.to_csv('./accounts.csv', index=False)
    return {"result":"bot" if str(predicted[0]) == "0" else "human","score":str(predict_proba[0]*5),"proba":str(predict_proba[0])}



def changepredicte(name,type):
    # data = pd.read_csv('./featuresfloatvf.csv')
    # column_names = data.columns.tolist()
    try:
        accounts=pd.read_csv('./accounts.csv')
        
        accounts['screen_name'] = accounts['screen_name'].astype(str).str.lower()
        dp = accounts[accounts['screen_name']==str.lower(name)]
        
        if dp.shape[0] == 0:
            return {"message": "accounts with that name does not exist"}
        else :
            #  dp[0]['account_type']=type
             accounts.loc[accounts['screen_name']==str.lower(name), 'account_type'] = type
            
             accounts.to_csv('./accounts.csv', index=False)
             return {"message":"done please rerun"}            
    except Exception as e:
        return {"message": "accounts empty","error":str(e)}
