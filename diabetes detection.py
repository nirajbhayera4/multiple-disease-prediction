 
import numpy as np
import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import accuracy_score

diabetes_dataset = pd.read_csv("/Users/hp/Downloads/diabetes.csv")

diabetes_dataset.head()

diabetes_dataset.shape

diabetes_dataset.describe()

diabetes_dataset['Outcome'].value_counts()

# label 0 represents non diabetics and 1 represents diabetics

diabetes_dataset.groupby('Outcome').mean()

# seperating the dataset

X = diabetes_dataset.drop(columns='Outcome', axis=1)
Y = diabetes_dataset['Outcome']
print(Y)

# Data standardization

scaler = StandardScaler()
scaler.fit(X)
standardized_data = scaler.transform(X)
print(standardized_data)

X = standardized_data
Y = diabetes_dataset['Outcome']
print(X)
print(Y)

# Train Test split

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, stratify=Y, random_state=2)
print(X.shape, X_train.shape, X_test.shape)

# Training the model

classifier = svm.SVC(kernel='linear')

# Training the svm classifier

classifier.fit(X_train, Y_train)

# Model Evaluation trying to predict the accuracy score

X_train_prediction = classifier.predict(X_train)
training_data_accuracy = accuracy_score(X_train_prediction, Y_train)
print('accuracy score of the training data : ', training_data_accuracy)

# trying to predict the accuracy score of test data

X_test_prediction = classifier.predict(X_test)
test_data_accuracy = accuracy_score(X_test_prediction, Y_test)
print('accuracy score of the test data : ', test_data_accuracy)

filename = 'diabetes_model.sav'
pickle.dump(classifier, open(filename, 'wb'))

loaded_model = pickle.load(open('diabetes_model.sav', 'rb'))
# Making a predictive system

input_data = (

    str(input("Name: ")),
    float(input("Pregnancies: ")),
    float(input("Glucose: ")),
    float(input("BloodPressure: ")),
    float(input("SkinThickness: ")),
    float(input("Insulin: ")),
    float(input("BMI: ")),
    float(input("DiabetesPedigreeFunction: ")),
    float(input("Age: "))
)

input_data_as_numpy_array = np.asarray(input_data)

input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)

std_data = scaler.transform(input_data_reshaped)
print(std_data)

prediction = classifier.predict(std_data)
print(prediction)

if (prediction[0] == 0):
    print('The person is not diabetic')
else:
    print('The person is diabetic')



















