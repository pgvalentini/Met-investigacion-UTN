import numpy as np
import pandas as pd



url = 'Reordered Linescan_nro 31 label JORDAN_234_P1_201901271901_MGA94_55.csv'
dfdos = pd.read_csv(url)

url = 'Reordered Linescan_nro 38 label WALHALLA_295_P1_201902011156_MGA94_55.csv'
dftres = pd.read_csv(url)


url = 'Reordered Linescan_nro 39 label JORDAN_310_P1_201902012046_MGA94_55.csv'
dfcuatro= pd.read_csv(url)

url = 'Reordered Linescan_nro 41 label WALHALLA_339_P1_201902030520_MGA94_55.csv'
dfcinco= pd.read_csv(url)

dfdos=dfdos.append(dfcuatro).append(dftres).append(dfcinco)

df = df.loc[~((df['linescan'] == 0))]

df_infer = pd.read_csv('test_refactorizado.csv')
df_infer.head()

from sklearn import  datasets, preprocessing
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


from sklearn.linear_model import SGDClassifier


df=df.drop('label', axis=1)
#df=df.drop('dateTimeLocal', axis=1)
#df=df.drop('x', axis=1)
#df=df.drop('y', axis=1)
df.head()


import datetime as dt
df['dateTimeLocal'] = pd.to_datetime(df['dateTimeLocal'], format='%d/%m/%Y %H:%M')
df['dateTimeLocal'] = df['dateTimeLocal'].map(dt.datetime.toordinal)


X, y = df.drop('target', axis=1),df['target'] 


X_train, X_test, y_train, y_test = train_test_split(X,y, random_state=33)

scaler =preprocessing.StandardScaler().fit((X_train))


X_train=scaler.transform(X_train)

X_test = scaler.transform(X_test)

# instantiate the model (using the default parameters)
clf =  SGDClassifier(loss='modified_huber', max_iter=1000) 

clf.fit(X_train , y_train)
y_pred=clf.predict(X_test)


y_pred


y_pred.mean()



y_test


accuracy_score(y_test, y_pred)


X_infer= df_infer.drop('target', axis=1) ##cargo el dataset objetivo


#X_infer
#X_infer=X_infer.drop('label', axis=1)
#X_infer=X_infer.drop('dateTimeLocal', axis=1)
#X_infer=X_infer.drop('x', axis=1)
#X_infer=X_infer.drop('y', axis=1)

X_infer=scaler.transform(X_infer)

y_pred=clf.predict(X_infer)

y_pred.mean()  #0.2262

sol = np.array(y_pred)

df = pd.DataFrame(sol, columns = ['target'])


df.to_csv("Submission.csv")












