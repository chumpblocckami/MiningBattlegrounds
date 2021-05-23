from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import matplotlib.pyplot as plt
import pandas as pd
#data = LabelEncoder().fit_transform(data)

X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.33, random_state=126)
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
clf = DecisionTreeClassifier(max_depth = 2, random_state=126)
# fit the model
clf.fit(X_train, y_train)
preds = clf.predict(X_test)
accuracy_score(y_test,preds)

importance = clf.feature_importances_
# summarize feature importance
for i,v in enumerate(importance):
	print('Feature: %0d, Score: %.5f' % (i,v))
# plot feature importance
plt.bar([x for x in range(len(importance))], importance)