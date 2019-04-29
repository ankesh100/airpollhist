import os
import sys
from stat import *
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


if sys.version[0] == '2':
    reload(sys)
    sys.setdefaultencoding("utf-8")


df=pd.read_csv("data/Air_Quality_RSPM_2008.csv",encoding="ISO-8859-1")

feature_col_name=['Numbers of  monitoring days (n)','Annual Avg RSPM','Percentage- exceedence(24 hourly)']
predicted_classname=['Air Quality']
#lol={'Low':0,'Moderate':0,'High':1,'Critical':1}
lol={'Low':0,'Moderate':1,'High':2,'Critical':3}
df['Air Quality']=df['Air Quality'].fillna('Moderate')
df['Air Quality']=df['Air Quality'].map(lol)
x=df[feature_col_name].values
y=df[predicted_classname].values
def input(StringData):
    inputData = StringData.split(' ')
    inputData = [float(elem) for elem in inputData]
    inputData = [inputData]

    from sklearn.tree import DecisionTreeClassifier
    dt_model=DecisionTreeClassifier(random_state=0)
    dt_model.fit(x,y.ravel())
    #rf_test_predict=rf_model.predict_proba(inputData)
    dt_test_predict=dt_model.predict(inputData)
    #print("%-30s%-4.2f%-1s"%('Likelihood of Heart Disease is ',100*rf_test_predict[0][1],'%'))
    #print(dt_test_predict)
    if dt_test_predict==[0]:
    	return ('Risk Impact of Air Pollution: Low')
        #return "Low." +"Enjoy daily outdoor activity"
    elif dt_test_predict==[1]:
    	return ('Risk Impact of Air Pollution: Moderate')
        #return "\bModerate."+ "\n" +" People with Asthma & Respiratory illness should wear mask"

    elif dt_test_predict==[2]:
    	return ('Risk Impact of Air Pollution: High')
        #return "\bHigh." + "\n" + "!!!Wear mask before stepping outside!!!"

    elif dt_test_predict==[3]:
        return ('Risk Impact of Air Pollution: Critical')
        #return "\bCritical." + "\n" + "!If you step outside, you're reducing your livelihood and risking your life, Please don't step outside at any cost!!!"

#if __name__ == "__input__":
#    inputs = ' '.join(sys.argv[1:])
#    input(inputs)
