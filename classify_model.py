'''
Author: Derry
Date: 2022-12-05 21:30:18
LastEditors: Derry
Email: drlv@mail.ustc.edu.cn
LastEditTime: 2022-12-06 17:15:26
Description: None
'''
import joblib
import matplotlib.pyplot as plt
import numpy as np
from catboost import CatBoostClassifier
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.manifold import TSNE
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from xgboost import XGBClassifier

from NLP import NLPEmbedding


def bow(X):
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(X)
    return X


def plot_embedding(X, y, title=None):
    """
    Plot an embedding with the target classes using t-SNE.

    Parameters
    ----------
    X : array-like of shape (n_samples, n_features)
        The input samples.
    y : array-like of shape (n_samples,)
        The target values.
    title : str, optional
        The title of the plot. The default is None.

    Returns
    -------
    None.
    """
    plt.figure(figsize=(6, 5))
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.get_cmap("jet", 2))
    plt.legend(handles=plt.scatter([], [], c='k', cmap=plt.cm.get_cmap("jet", 2)).legend_elements()[0],
               labels=["negative", "positive"])
    plt.xticks(())
    plt.yticks(())
    if title is not None:
        plt.title(title)
    plt.legend()
    plt.show()


class TextClassifier(NLPEmbedding):
    def __init__(self):
        super().__init__()
        self.focus_words = ['cancer', 'tumor', 'tumour']

    def predict(self, X, model_path="model/LogisticRegression.model"):
        X = self.model.encode(X)
        clf = joblib.load(model_path)
        y_pred = clf.predict(X)
        return y_pred


if __name__ == "__main__":
    with open("data/train/pos.txt", 'r', encoding='utf-8') as f:
        pos = []
        for line in f:
            pos.append(line.strip())

    with open("data/train/neg.txt", 'r', encoding='utf-8') as f:
        neg = []
        for line in f:
            neg.append(line.strip())

    X_org = pos + neg
    nlp = NLPEmbedding()
    X = nlp.model.encode(X_org)
    # X = bow(X_org)
    y = np.array([1]*len(pos)+[0]*len(neg))

    clf = LogisticRegression()
    clf.fit(X, y)
    joblib.dump(clf, "model/LogisticRegression.model")

    # # 10折交叉验证
    # from sklearn.model_selection import KFold
    # from sklearn.metrics import accuracy_score
    # from sklearn.neighbors import KNeighborsClassifier

    # kf = KFold(n_splits=10, shuffle=True, random_state=0)
    # for model in [LogisticRegression(), SVC(kernel='poly'), RandomForestClassifier(n_estimators=100), XGBClassifier(),KNeighborsClassifier()]:
    #     acc = []
    #     for train_index, test_index in kf.split(X):
    #         X_train, X_test = X[train_index], X[test_index]
    #         y_train, y_test = y[train_index], y[test_index]
    #         clf = LogisticRegression()
    #         clf.fit(X_train, y_train)
    #         y_pred = clf.predict(X_test)
    #         acc.append(accuracy_score(y_test, y_pred))
    #     print(sum(acc)/len(acc))

    # Plot data
    # X_tsne = TSNE(n_components=2, init="pca", random_state=0).fit_transform(X)
    # X_pca = PCA(n_components=2).fit_transform(X)
    # plot_embedding(X_tsne, y, title="t-SNE embedding of the data")
    # plot_embedding(X_pca, y, title="PCA embedding of the data")
