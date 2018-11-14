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
	with open("./srcFiles/" + fname) as f:
		allLines = f.readlines()
		files[fname] = [{} for _ in allLines]
		for num, text in enumerate(allLines):
			files[fname][num]["text"] = text.rstrip().replace("\t", "  ")
			files[fname][num]["heat"] =  0

		# pp.pprint(allLines)
for child in root[1]:
	file = child.attrib["object_name"]
	if file in files:
		line = int(child.attrib["line"]) - 1
		files[file][line]["heat"] = files[file][line]["heat"] + 1
	
for filename, file in files.items():
	data = [[val["heat"]] for val in file][::-1]
	labels = [val["text"] for val in file][::-1]
	# pp.pprint(labels)
	heatmap = plt.pcolor(data, cmap="YlOrRd")
	plt.axis('off')
	for y in range(len(labels)):
		plt.text(0.01, y + 0.45, labels[y], verticalalignment='center')

	plt.show()
