import matplotlib.pyplot as plt
import numpy as np
import xml.etree.ElementTree as ET
import os
import pprint
pp = pprint.PrettyPrinter(indent=4)

tree = ET.parse('tmp.xml')
root = tree.getroot()

files = {} # {filename: {linenumber: {text: string, heat: number}}}
for fname in os.listdir("./srcFiles"):
	files[fname] = {}
	with open("./srcFiles/" + fname) as f:
		for num, text in enumerate(f.readlines()):
			files[fname][str(num + 1)] = {"text": text.rstrip().replace("\t", "  "), "heat": 0}


for child in root[1]:
	file = child.attrib["object_name"]
	if file in files:
		line = child.attrib["line"]
		files[file][line]["heat"] = files[file][line]["heat"] + 1
	
for filename, file in files.items():
	data = [[val["heat"]] for _, val in file.items()][::-1]
	labels = [val["text"] for _, val in file.items()][::-1]
	heatmap = plt.pcolor(data, cmap="YlOrRd")
	plt.axis('off')
	for y in range(len(labels)
	):
		plt.text(0.01, y + 0.45, labels[y], verticalalignment='center')

	plt.show()
