 

import numpy as np
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

heart_disease_dataset= pd.read_csv("/Users/hp/Downloads/heart.csv")

heart_disease_dataset.head()

heart_disease_dataset.tail()

# number of rows and columns in dataset

heart_disease_dataset.shape

#checking for missing values

heart_disease_dataset.isnull().sum()

#statistical measures about the data

heart_disease_dataset.describe()

#checking the distribution of target variable

heart_disease_dataset['target'].value_counts()

# 1= heart disease
# 0= no heart disease

X= heart_disease_dataset.drop(columns='target', axis=1)
Y= heart_disease_dataset['target']
print(X)
print(Y)

#spliting the data into training data and test data

X_train, X_test, Y_train, Y_test= train_test_split(X, Y, test_size=0.2, stratify=Y, random_state=2)
print(X.shape, X_train.shape, X_test.shape)

#Model training by logistic regression model

model= LogisticRegression()

#training the logistic regression model with training data

model.fit(X_train, Y_train)

#Model evaluation

X_train_prediction= model.predict(X_train)
training_data_accuracy= accuracy_score(X_train_prediction, Y_train)
print('Accuracy on training data : ',training_data_accuracy)

#Accuracy on test data

X_test_prediction= model.predict(X_test)
test_data_accuracy= accuracy_score(X_test_prediction, Y_test)
print('Accuracy on test data : ',test_data_accuracy)


filename= 'heart_model.sav'
pickle.dump(model, open(filename,'wb'))

loaded_model= pickle.load(open('heart_model.sav','rb'))

#Building a predictive data

print("\nEnter the values for the following features:")
input_data = (
    float(input("Name: ")),
    float(input("Age: ")),
    float(input("Sex (1 = Male, 0 = Female): ")),
    float(input("Chest Pain Type (0, 1, 2, or 3): ")),
    float(input("Resting Blood Pressure: ")),
    float(input("Cholesterol: ")),
    float(input("Fasting Blood Sugar (> 120 mg/dl, 1 = True; 0 = False): ")),
    float(input("Rest ECG (0, 1, or 2): ")),
    float(input("Max Heart Rate Achieved: ")),
    float(input("Exercise Induced Angina (1 = Yes; 0 = No): ")),
    float(input("Oldpeak (ST depression induced by exercise): ")),
    float(input("Slope (0, 1, or 2): ")),
    float(input("Number of Major Vessels (0-3): ")),
    float(input("Thal (1, 2, or 3): "))
)


input_data_as_numpy_array= np.asarray(input_data)

#reshaping the numpy array as we are predicting for only 1 instance

input_data_reshaped= input_data_as_numpy_array.reshape(1,-1)

prediction= model.predict(input_data_reshaped)
print(prediction)

if(prediction[0]==0):
    print('The person does not have heart disease')
else:
    print('The person has heart disease')












