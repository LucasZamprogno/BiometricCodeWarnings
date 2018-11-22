from sklearn.ensemble import RandomForestClassifier
from feature_extractor import FeatureExtractor
from collections import defaultdict
import pandas as pd
import numpy as np

def read_ratings(ratingsfile):
    df = pd.read_csv(ratingsfile, names=['file', 'start', 'end'])
    ratings = defaultdict(dict)
    for _, row in df.iterrows():
        file = row['file']
        start = row['start']
        end = row['end']
        for line in range(start, end+1):
            ratings[file][line] = 1
    return ratings

def create_targets(info, ratingsfile):
    ratings = read_ratings(ratingsfile)
    viewed = defaultdict(dict)
    lines = info
    for _, row in lines.iterrows():
        file = row['file']
        line = row['line']
        viewed[file][line] = 0
    for file in ratings:
        for line in ratings[file]:
            if(line in viewed[file]):
                viewed[file][line] = 1
    
    arr = []
    for file in viewed:
        for line in viewed[file]:
            arr.append([file, line, viewed[file][line]])
    df = pd.DataFrame(arr, columns=['file', 'line', 'difficulty'])
    return pd.merge(lines, df, on=['file', 'line'], how='left')['difficulty']



class LineDifficultyClassifier:

    #datafile: string, ratings: dataframe
    def __init__(self, n_estimators=100):
        self.model = RandomForestClassifier(n_estimators=n_estimators, class_weight='balanced')

    def set_data(self, datafile, ratingsfile):
        fe = FeatureExtractor(datafile)
        self.features = fe.extract_features()
        self.info = fe.extract_info()
        self.make_lookup_table()
        self.targets = create_targets(self.info, ratingsfile)

    def make_lookup_table(self):
        self.lookup_table = {}
        for index, row in self.info.iterrows():
            self.lookup_table[(row['file'] , row['line'])] = index
        
    def lookup(self, file, line):
        return self.lookup_table[(file, line)]
    
    def predict(self, file, line):
        X = self.features.drop(self.lookup(file, line))
        y = self.targets.drop(self.lookup(file, line))
        self.model.fit(X,y)
        X_test = self.features.iloc[self.lookup(file, line)]
        y_true = self.targets.iloc[self.lookup(file, line)]
        return (int(self.model.predict(np.array(X_test).reshape(1,-1))), y_true)
