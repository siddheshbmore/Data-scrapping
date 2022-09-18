from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import TfidfTransformer

import numpy as np
import pandas as pd
import csv

import re
import sys

# if len(sys.argv) < 2:
#    print('Format: python classify_job.py test_file.csv')
#    sys.exit(1)

# test_file = sys.argv[1]
test_file = "test_jobs.csv"

# Read the jobs.csv file
data = pd.read_csv('jobs.csv', header=None)

job_desc = list(data[0])
job_title = list(data[1])

le = preprocessing.LabelEncoder()
y = le.fit_transform(job_title)

X_train, X_test, y_train, y_test = train_test_split(job_desc, y, test_size=0.2, random_state=42)

# Build a counter based on the training dataset
counter = CountVectorizer()
counter.fit(X_train)


# count the number of times each term appears in a document and transform each doc into a count vector
counts_train = counter.transform(X_train) # transform the training data
counts_test = counter.transform(X_test) # transform the testing data

tf_transformer = TfidfTransformer(use_idf=True).fit(counts_train)
X_train_tf = tf_transformer.transform(counts_train)
X_test_tf = tf_transformer.transform(counts_test)


# SVM Classifier
svm_clf = SGDClassifier(loss='hinge', penalty='l2',
                           alpha=1e-3, random_state=42,
                           max_iter=5, tol=None)

svm_clf.fit(X_train_tf, y_train)

# Predict class on test data
pred = svm_clf.predict(X_test_tf)

# print accuracy
print ("Accuracy on Cross validation of train data = %.2f%%" % (100*accuracy_score(pred, y_test)))

# Test
# Read test file
test_data = pd.read_csv(test_file, header=None)
test_desc = list(test_data[0])

# preprocessing of text
# Remove non-alphabets including punctuations and numbers from job description
pattern = re.compile(r'[^a-zA-Z]', re.UNICODE)

def preprocess(job_desc):
    # remove non-alphabets
    job_desc = pattern.sub(' ', job_desc)
    job_desc = re.sub(r'\s+', ' ', job_desc).strip()
    # Convert to lowercase
    job_desc = job_desc.lower()
    return job_desc

X_test = [preprocess(x) for x in test_desc]

# count the number of times each term appears in a document and transform each doc into a count vector
counts_test = counter.transform(X_test) # transform the testing data
X_test_tf = tf_transformer.transform(counts_test)

# Predict class on test data
pred = svm_clf.predict(X_test_tf)

predictions = le.inverse_transform(pred)

# y_test = [1]*30 + [0]*30
# print accuracy
# print ("Accuracy on the test data = %.2f%%" % (100*accuracy_score(pred, y_test)))

# Write the predictions to a file
with open('test_predictions.csv', "w", encoding="utf-8") as pred_file:
    csv_writer = csv.writer(pred_file, delimiter=',')
    for p in predictions:
        csv_writer.writerow([p])

print('Successfully written the predicted job titles to the test_predictions.csv file')



