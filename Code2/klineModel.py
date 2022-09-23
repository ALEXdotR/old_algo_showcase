def xgBoostModel(X_train, y_train, X_test, y_test):
    from xgboost import XGBClassifier
    from sklearn.metrics import classification_report
    from sklearn.metrics import confusion_matrix
    from xgboost import plot_importance
    from matplotlib import plt
    xgb = XGBClassifier()
    model = xgb.fit(X_train, y_train)
    y_pre = xgb.predict(X_test)
    
    print(classification_report(y_test, y_pre))
    print("Confusion_matrix :")
    print(confusion_matrix(y_test, y_pre))
    print("Feature importances :")
    # plot feature importance
    plot_importance(model)
    plt.show()
    return model
    
def validation(model,X_train, y_train, times):
    from sklearn.model_selection import cross_val_score
    scores = cross_val_score(model,X_train, y_train,cv=times,scoring='accuracy')
    print(scores)
    print(scores.mean())