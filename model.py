from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import TimeSeriesSplit
from sklearn.model_selection import RandomizedSearchCV


def modelTraining(df, last_row):
    
    x = df.drop(columns=["Target", "Next_Day", "Up_Band", "Lo_Band"])
    y = df["Target"]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size= 0.2, random_state= 42, shuffle= False)

    tscv = TimeSeriesSplit(n_splits=5)

    params = {
        "n_estimators": [200, 300, 700, 800],
        "max_depth": [5,8,10,12,15],
        "min_samples_leaf": [ 3,4,2,5],
        "min_samples_split": [2,5,10],
        "max_features": ["log2", "sqrt"]
        
    }
    search = RandomizedSearchCV(
        estimator = RandomForestClassifier(random_state=42),
        param_distributions = params,
        n_iter = 20,
        cv = tscv,
        scoring = "accuracy",
        random_state = 42,
        n_jobs = -1
    )

    #model = RandomForestClassifier(n_estimators= 500, min_samples_leaf=5, max_features="sqrt",  class_weight="balanced", max_depth=15, random_state= 42)
    
    search.fit(x_train, y_train)
    # bParams = search.best_params_
    # bScore = search.best_score_
    bModel = search.best_estimator_
    y_predict = bModel.predict(x_test)

    accuracy = accuracy_score(y_test, y_predict)
    #print(f"Accuracy: {accuracy:.2%}")

    cm = confusion_matrix(y_test, y_predict)

    #cr = classification_report(y_test, y_predict)

    prediction = bModel.predict(last_row)

    return prediction, cm, accuracy 

