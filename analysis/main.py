from classifier import LineDifficultyClassifier
import os
import pandas as pd
from collections import defaultdict
import make_rawdata
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import cohen_kappa_score

def getlines():
    raw = pd.read_csv("/Users/csatterfield/repos/507/507/analysis/rawdata.csv")
    lines = raw[['file', 'line']].drop_duplicates()
    return list([tuple(x) for x in lines.values])

def predictlines():
    ldc = LineDifficultyClassifier()
    ldc.set_data("/Users/csatterfield/repos/507/507/analysis/rawdata.csv", "/Users/csatterfield/repos/507/507/analysis/highlighted.csv")
    lines = getlines()
    for (file, line) in lines:
        pred, true = ldc.predict(file, line)
        print(file + "," + str(line) +"," + str(pred))

def main():
    folders = ["./Userdata/" + x for x in os.listdir("./Userdata") if x.startswith("P")]
    ldc = LineDifficultyClassifier()
    difficulty_maps = dict()
    scores = defaultdict(dict)
    for folder in folders:
        make_rawdata.main(folder)
        ldc.set_data(folder + "/rawdata.csv", folder + "/highlighted.csv")
        raw = pd.read_csv(folder + "/rawdata.csv")
        lines = raw[['file', 'line']].drop_duplicates()
        m = defaultdict(dict)
        pred = []
        true = []
        for _, row in lines.iterrows():
            line = row['line']
            file = row['file']
            m[file][line] = ldc.predict(file, line)
            pred.append(m[file][line][0])
            true.append(m[file][line][1])
        difficulty_maps[folder] = m
        scores[folder]['pred'] = pred
        scores[folder]['true'] = true

        print(folder)
        print("Recall:",recall_score(true, pred))
        print("Precision:",precision_score(true, pred))
        print("Accuracy:", accuracy_score(true, pred))
        print("CK:", cohen_kappa_score(true, pred))

    #print(difficulty_maps)

def all_users_main():
    folders = ["./Userdata/" + x for x in os.listdir("./Userdata") if x.startswith("P")]
    ldc = LineDifficultyClassifier()
    difficulty_maps = dict()
    scores = defaultdict(dict)
    raw = pd.DataFrame()
    highlighted = pd.DataFrame()
    for folder in folders:
        make_rawdata.main(folder)
        raw = raw.append(pd.read_csv(folder + "/rawdata.csv"))
        h = pd.read_csv(folder + "/highlighted.csv", names=['file', 'start', 'end'])
        highlighted = highlighted.append(h)

    raw.to_csv("rawdata.csv", index=False)
    highlighted.to_csv("highlighted.csv", header=False, index=False)
    ldc.set_data("./rawdata.csv", "./highlighted.csv")
    raw = pd.read_csv("./rawdata.csv")
    lines = raw[['file', 'line']].drop_duplicates()
    m = defaultdict(dict)
    pred = []
    true = []
    for _, row in lines.iterrows():
        line = row['line']
        file = row['file']
        m[file][line] = ldc.predict(file, line)
        pred.append(m[file][line][0])
        true.append(m[file][line][1])
    difficulty_maps[folder] = m
    scores[folder]['pred'] = pred
    scores[folder]['true'] = true

    print("Recall:",recall_score(true, pred))
    print("Precision:",precision_score(true, pred))
    print("Accuracy:", accuracy_score(true, pred))
    print("CK:", cohen_kappa_score(true, pred))

    #print(difficulty_maps)
if __name__ == '__main__':
    predictlines()