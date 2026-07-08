from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

def modelTraining(df, last_row):
    
    x = df.drop(columns=["Target", "Next_Day", "Dividends", "Stock Splits"])
    y = df["Target"]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size= 0.2, random_state= 42, shuffle= False)

    model = RandomForestClassifier(n_estimators= 700, min_samples_leaf=5, max_depth=10, random_state= 42)
    
    model.fit(x_train, y_train)

    y_predict = model.predict(x_test)

    accuracy = accuracy_score(y_test, y_predict)
    print(f"Accuracy: {accuracy:.2%}")

    prediction = model.predict(last_row)
    print(f"Prediction for tomorrow: {bool(prediction)}")

    # print(x_train.shape)

    # print(x_test.shape)

    # print(df["Target"].value_counts())
    # print(df["Target"].value_counts(normalize=True))
    # print(classification_report(y_test, y_predict))
    # print(confusion_matrix(y_test, y_predict))

    # importance = model.feature_importances_
    # for feature, score in zip(x.columns, importance):
    #     print(feature, score)
