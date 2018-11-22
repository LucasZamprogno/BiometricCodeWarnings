import xml.etree.ElementTree as ET
import pandas as pd
import os
from sklearn import preprocessing
import numpy as np



def main(folder):
	files = parseXML(folder + '/tmp.xml')
	gaze_df = pd.DataFrame(flatten_and_make_window(files))
	biometric_df = make_biometric_df(folder + '/vitals.csv')
	gaze_df = pd.merge(gaze_df, biometric_df, on='timestamp')
	gaze_df.to_csv(folder + '/rawdata.csv', index=False)

def parseXML(xmlFileName):
	tree = ET.parse(xmlFileName)
	root = tree.getroot()

	files = {} # {filename: {numlines: number , events: [{line: number, timestamp: number}]}}
	for fname in os.listdir("../heatmap/srcFiles"):
		with open("../heatmap/srcFiles/" + fname) as f:
			files[fname] = {}
			files[fname]['numlines'] = sum(1 for line in f)
			files[fname]['events'] = []
			
	for child in root[1]:
		file = child.attrib["object_name"]
		if file in files:
			line = int(child.attrib["line"])
			timestamp = int(child.attrib["event_time"])
			files[file]['events'].append({'line': line, 'timestamp': timestamp})
	
	return files


def flatten_and_make_window(fileDict, window_size=1):
	result = []
	for filename, file in fileDict.items():
		for event in file['events']:
			for i in range(window_size):
				if(event['line'] - (i+1) > 0):
					result.append({'file': filename, 'line': event['line'] - (i+1), 'timestamp_ms': event['timestamp'], 'timestamp': event['timestamp']//1000})
				if(event['line'] + (i+1) <= file['numlines']):
					result.append({'file': filename, 'line': event['line'] + (i+1), 'timestamp_ms': event['timestamp'], 'timestamp': event['timestamp']//1000})

			result.append({'file': filename, 'line': event['line'], 'timestamp_ms': event['timestamp'], 'timestamp': event['timestamp']//1000})

	return result

def make_biometric_df(filename):
	df = pd.read_csv(filename)
	df['heart_rate'] = pd.Series([x if y >= 50 else np.nan for [x,y] in np.array(df[['heart_rate', 'hr_quality']])])
	df['heart_rate_variability'] = pd.Series([x if y >= 50 else np.nan for [x,y] in np.array(df[['heart_rate_variability', 'hrv_quality']])])

	columns = ['heart_rate', 'heart_rate_variability', 'object_temperature', 'gsr_electrode']
	values = df[columns].values

	imputer = preprocessing.Imputer()
	imputed_values = imputer.fit_transform(values)

	standard_scaler = preprocessing.StandardScaler()
	scaled_values = standard_scaler.fit_transform(imputed_values)
	scaled_df = pd.DataFrame(scaled_values, columns=columns)
	scaled_df['timestamp'] = df['timestamp']

	return scaled_df