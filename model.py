from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

def modelTraining(df, last_row):
    
    x = df.drop(columns=["Target", "Next_Day", "Up_Band", "Lo_Band"])
    y = df["Target"]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size= 0.2, random_state= 42, shuffle= False)

    model = RandomForestClassifier(n_estimators= 500, min_samples_leaf=5, max_features="sqrt",  class_weight="balanced", max_depth=15, random_state= 42)
    
    model.fit(x_train, y_train)

    prob = model.predict_proba(x_test)[:, 1]
    y_predict = (prob>0.54).astype(int)

    accuracy = accuracy_score(y_test, y_predict)
    print(f"Accuracy: {accuracy:.2%}")

    cm = confusion_matrix(y_test, y_predict)

    cr = classification_report(y_test, y_predict)

    ut_values =  y_test.unique()
    up_values = set(y_predict)

    prediction = model.predict(last_row)

    return prediction, model, cm, cr, accuracy

