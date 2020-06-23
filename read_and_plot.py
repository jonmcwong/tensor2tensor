#!/usr/bin/env python

import sys
import matplotlib.pyplot as plt
import numpy as np
import os

argv = sys.argv
print(argv)
argn = len(argv)

if argn < 2 or argn > 3:
	raise ValueError(
"""
function signature:
./read_and_plot.py <model_name> <read_as_bytestring>
""")

read_as_bytestring = bool(argv[2]) if argn > 2 else None
model_name = argv[1]

results_dir = "eval-results-" + model_name
all_results_array = []
print(results_dir, read_as_bytestring)

class dataHolder:
	def __init__(self, all_results_array, labels_dict, dataset_splits_dict):
		self.all_results_array = all_results_array
		self.labels_dict = labels_dict
		self.dataset_splits_dict = dataset_splits_dict

def plot_against_steps(collated_results, datset_splits, models):
	if datset_splits == "all":
		dataset_split_indicies = np.arange(12)
	collated_results[dataset_splits, :, metrics]
	plt.plot()
	

def inconsistent_cols():
	raise BaseException(
						"number of columns is inconsistent with category labels"
						)

if os.path.isdir(results_dir):
	# read as text
	# get dataset_splits from checklist
	with open(os.path.join(results_dir, "checklist"), "r") as checklist_file:
		checklist = checklist_file.read().split("\n")
		checklist = [i for i in checklist if i != ""]
	for dataset_split in checklist:
		print("found " + dataset_split)
		# read results
		with open(os.path.join(
			results_dir,
			"eval_"+dataset_split+"_results.txt"), "r") as data_file:
			# split by line as remove empty lines
			data = data_file.read().split("\n")
			data = [i for i in data if i != ""]
			# split lines by data item
			data = [row.split("\t") for row in data]
			# pick out the first row (category labels)
			labels = np.array(data.pop(0))
			reorder = labels.argsort()
			labels = np.sort(labels)
			num_categories = len(labels)
			# raise error if inconsistent columns per row
			[inconsistent_cols() for i in data if len(i) != num_categories ]
			array = np.array(data, dtype = np.float64)
			# reorder the columns
			array = array[:, reorder]
		all_results_array.append(array)
	all_results_array = np.array(all_results_array)
	labels_dict = dict([(labels[i], i) for i in range(len(labels))])
	dataset_splits_dict = dict([(labels[i], i) for i in range(len(checklist))])
	collated_results = dataHolder(all_results_array, labels_dict, dataset_splits_dict)
else:
	raise BaseException(
		"Could not find {} folder".format(results_dir)
		)



# extra_add_or_sub_big
# extra_add_sub_multiple_longer
# extra_div_big
# extra_mixed_longer
# extra_mul_big
# extra_mul_div_multiple_longer
# inter_add_or_sub
# inter_add_sub_multiple
# inter_div
# inter_mixed
# inter_mul
# inter_mul_div_multiple
