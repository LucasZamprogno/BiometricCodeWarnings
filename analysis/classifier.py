from sklearn.ensemble import RandomForestClassifier
from feature_extractor import FeatureExtractor
import pandas as pd
import numpy as np

class LineDifficultyClassifier:

    #datafile: string, ratings: dataframe
    def __init__(self, datafile, ratings, n_estimators=100):
        self.model = RandomForestClassifier(n_estimators=n_estimators)
        fe = FeatureExtractor(datafile)
        self.features = fe.extract_features()
        self.info = fe.extract_targets()
        self.make_lookup_table()
        self.ratings = ratings

    def make_lookup_table(self):
        self.lookup_table = {}
        for index, row in self.info.iterrows():
            self.lookup_table[(row['file'] , row['line'])] = index
        
    def lookup(self, file, line):
        return self.lookup_table[(file, line)]
    
    def predict(self, file, line):
        X = self.features.drop(self.lookup(file, line))
        y = self.ratings.drop(self.lookup(file, line))
        self.model.fit(X,y)
        X_test = self.features.iloc[self.lookup(file, line)]
        return self.model.predict(np.array(X_test).reshape(1,-1))

if __name__ == '__main__':
    ldc = LineDifficultyClassifier('rawdata.csv', None)
    print(ldc.predict('PaintWindow.java', 186))