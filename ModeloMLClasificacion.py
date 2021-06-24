import numpy as np
import pandas as pd

url = 'Reordered Linescan_nro 29 label JORDAN_231_P1_201901271500_MGA94_55.csv'
df = pd.read_csv(url)
df_infer = pd.read_csv('resources/challenge1_test.csv')


url = 'Reordered Linescan_nro 31 label JORDAN_234_P1_201901271901_MGA94_55.csv'
dfdos = pd.read_csv(url)


url = 'Reordered Linescan_nro 38 label WALHALLA_295_P1_201902011156_MGA94_55.csv'
dftres = pd.read_csv(url)

url = 'Reordered Linescan_nro 39 label JORDAN_310_P1_201902012046_MGA94_55.csv'
dfcuatro= pd.read_csv(url)

dfcinco=df.append(dfcuatro).append(dftres).append(dfdos).append(df)


df['dateTimeLocal'] = pd.to_datetime(df['dateTimeLocal'], format='%d/%m/%Y %H:%M')


import datetime as dt
df['dateTimeLocal'] = df['dateTimeLocal'].map(dt.datetime.toordinal)

df.dateTimeLocal.mean()

df = df.loc[~((df['linescan'] == 0))] #eliminar todos las filas dde linescan ==0


df_infer = pd.read_csv('test_refactorizado.csv')
df_infer.head()

format='%d/%m/%Y %H:%M'
df_infer['dateTimeLocal'] = pd.to_datetime(df_infer['dateTimeLocal'], format=format)

df_infer['dateTimeLocal'] = df_infer['dateTimeLocal'].map(dt.datetime.toordinal)

from sklearn import  datasets, preprocessing
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


df=df.drop('label', axis=1)
#df=df.drop('dateTimeLocal', axis=1)
#df=df.drop('x', axis=1)
#df=df.drop('y', axis=1)
df.head()

X, y = df.drop('target', axis=1), df['target'] 


X_train, X_test, y_train, y_test = train_test_split(X,y, random_state=63)

scaler = preprocessing.StandardScaler().fit((X_train))



X_train=scaler.transform(X_train)


X_test = scaler.transform(X_test)



# import the class
from sklearn.linear_model import LogisticRegression

# instantiate the model (using the default parameters)
logreg = LogisticRegression()


# fit the model with data

logreg.fit(X_train,y_train)


y_pred=logreg.predict(X_test)

y_pred

y_test

accuracy_score(y_test, y_pred)


X_infer= df_infer.drop('target', axis=1) ##cargo el dataset objetivo


#X_infer
X_infer=X_infer.drop('label', axis=1)
#X_infer=X_infer.drop('dateTimeLocal', axis=1)
#X_infer=X_infer.drop('x', axis=1)
#X_infer=X_infer.drop('y', axis=1)


X_infer=scaler.transform(X_infer)

y_pred=logreg.predict(X_infer)


import numpy as np
sol = np.array(y_pred)

df = pd.DataFrame(sol, columns = ['target'])

df.to_csv("Submission 04-06-21_5.csv")


pr("ok submission")



