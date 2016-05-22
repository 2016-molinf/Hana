from __future__ import print_function

import matplotlib.pyplot as plt
import pandas
import numpy as np

from rdkit import Chem
from rdkit.Chem import Descriptors
from rdkit import DataStructs
from rdkit.Chem.Fingerprints import FingerprintMols

from sklearn import cross_validation
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.decomposition import PCA
from sklearn.svm import SVC



def gsarIC50(soubor, treshold=1000, test_size=0.3):
    # nacteni dat
    print("Loading data %s" %(soubor))
    print("...")
    #soubor = "bioactivities-16 15_40_42.tab"
    data = pandas.read_csv(soubor, sep="\t")
    data = data[~np.isnan(data.STANDARD_VALUE)]


    if data.shape[0] != len(np.where(data.STANDARD_UNITS == "nM")[0]):
        print("Inconsistent units")
    else:

        print("Create dataset")
        print("...")
        # Zobrazeni rozlozneni hodnot IC50
        print(data.STANDARD_VALUE.hist())
        plt.title("Standard values distribution")
        plt.xlabel('IC50')

        #Vytvoreni datasetu
        data["MOL"] = data.CANONICAL_SMILES.apply(Chem.MolFromSmiles)
        dataset = data[["MOL", "STANDARD_VALUE"]]

        # pridani deskriptoru
        print("Compute Descriptors")
        print("...")
        for name, f in Descriptors.descList:
            dataset[name] = dataset.MOL.apply(f)

        # odstraneni nan hodnot
        features = np.asarray(dataset.drop(["MOL", "STANDARD_VALUE"], axis=1))
        features -= features.mean(axis=0)
        features /= features.std(axis=0)
        no_variance = np.isnan(np.abs(np.std(features, axis=0)))
        for i in np.where(no_variance)[0]:
            dataset = dataset.drop([Descriptors.descList[i][0]], axis=1)
        print(dataset.columns.shape)

        # pridani tridy pro klasifikaci
        dataset["ACTIVITY_COMMENT"] = dataset.STANDARD_VALUE < treshold

        # rozdeleni na trenovaci a testovaci data 70x30
        print("Split into a training and testing set %d x %d"
            % (100-(test_size*100), (test_size*100)))
        train, test = cross_validation.train_test_split(dataset, test_size=test_size, random_state=1)
        #print(len(train), len(test))
        print("...")

        #spocitani fingerprints a prumerne vzdalenosti fingerprints
        fps = [FingerprintMols.FingerprintMol(x) for x in train["MOL"]]
        avgValue = 0

        def distij(i,j,fps=fps):
            return DataStructs.FingerprintSimilarity(fps[i],fps[j])

        for i in range(len(fps)):
            for j in range(len(fps)):
                avgValue += distij(i,j,fps)

        avgValue /= len(fps)**2
        #print("prumer",p, len(fps)**2,avgValue)


        # ulozeni trenovaci a testovaci mnoziny
        train.to_csv('train.csv',sep='\t', index=False)
        test.to_csv('test.csv',sep='\t',index=False)

        """
        # nacteni trenovaci a testovaci mnoziny
        train = pandas.read_csv("train.csv", sep="\t")
        test = pandas.read_csv("test.csv", sep="\t")
        train["ACTIVITY_COMMENT"] = train.STANDARD_VALUE < treshold
        test["ACTIVITY_COMMENT"] = test.STANDARD_VALUE < treshold
        """

        # fce pro vztvoreni vstupnich dat do jednotlivzch modelu
        def getX(dataset):
            return np.array(dataset[list(dataset.columns[2:])])
        def gety(dataset):
            return np.array(dataset.ACTIVITY_COMMENT)

        # rozdeleni na data a tridy
        X_train = getX(train)
        y_train = gety(train)


        # vypocet PCA
        n_samples, n_features = X_train.shape
        n_components = min(n_samples, n_features)

        print("Extracting the top %d eigenfaces from %d faces"
              % (n_components, X_train.shape[0]))
        pca = PCA(n_components=n_components, whiten=True).fit(X_train)
        print(pca)
        print("...")

        # transformace dat pro zvoleny pocet komponent
        X_train_pca = pca.transform(X_train)

        # trenovani SVM modelu
        print("Fitting the classifier to the training set")
        param_grid = {'C': [1e3, 5e3, 1e4, 5e4, 1e5],
                      'gamma': [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.1], }
        clf = GridSearchCV(SVC(kernel='rbf', class_weight='balanced'), param_grid)

        clf = clf.fit(X_train_pca, y_train)
        print("Best estimator found by grid search:")
        print(clf.best_estimator_)

        print("...")
        print("Predicting activity of compounds")
        # Urceni yda jsou data vhodna pro nas model, yda jsou podobna trenovacim datum
        testValue = 0
        tfps = [FingerprintMols.FingerprintMol(x) for x in test["MOL"]]
        def tdistij(i,j,fps,tfps):
            return DataStructs.FingerprintSimilarity(tfps[i],fps[j])
        for i in range(len(test["MOL"])):
            for j in range(len(fps)):
                testValue += tdistij(i,j,fps,tfps)
            testValue /= len(fps)
            if testValue < (avgValue / 4):
                test = test.drop(test.index[[i]])
        X_test = getX(test)
        y_test = gety(test)
        X_test_pca = pca.transform(X_test)
        y_pred = clf.predict(X_test_pca)

        # Evaluace modelu
        target_names = ["Not Active","Active"]
        n_classes = 2
        print(classification_report(y_test, y_pred, target_names=target_names))

        # confusion matrix
        def plot_confusion_matrix(cm, title='Confusion matrix', cmap=plt.cm.Blues):
            plt.imshow(cm, interpolation='nearest', cmap=cmap)
            plt.title(title)
            plt.colorbar()
            tick_marks = np.arange(len(target_names))
            plt.xticks(tick_marks, target_names, rotation=45)
            plt.yticks(tick_marks, target_names)
            plt.tight_layout()
            plt.ylabel('True label')
            plt.xlabel('Predicted label')

        # vypocet confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        np.set_printoptions(precision=2)
        print("...")
        print('Confusion matrix, without normalization')
        print(cm)
        #plt.figure()
        #plot_confusion_matrix(cm)

        # Normalizovana confusion matrix
        cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print('Normalized confusion matrix')
        print(cm_normalized)
        plt.figure()
        plot_confusion_matrix(cm_normalized, title='Normalized confusion matrix')
        plt.show()



gsarIC50("bioactivities-16 15_40_42.tab")
