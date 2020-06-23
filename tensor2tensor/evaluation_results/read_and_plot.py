import sys
import matplotlib.pyplot as plt
import numpy as np
import os

# read_as_bytestring = bool(argv[2]) if argn > 2 else None

model_name_list = [
	'transformer-base_test-2020-06-19',
	'transformer-base_test-dropout03-2020-06-20',
	'transformer-base_test-no-dropout-2020-06-19',
	'transformer-base_test_dropout02-2020-06-19',
	'transformer-noam-dropout0-2020-06-20',
	'transformer-noam-dropout01-2020-06-20',
	'transformer-noam-dropout02-2020-06-20',
	'transformer-noam-dropout03-2020-06-20',
	'transformer-quick-base-dropout01-2020-06-21',
	# 'transformer-quick-noam-dropout01-2020-06-21',
	'universal_transformer-base_test-loss-0001-2020-06-21',
	'universal_transformer-base_test-loss-001-2020-06-21',
	'universal_transformer-base_test_loss_0005-2020-06-21',
]

all_results_array = []
# print(results_dir, read_as_bytestring)

class dataHolder:
	def __init__(self, all_results_array, labels_dict, dataset_splits_dict):
		self.all_results_array = all_results_array
		self.labels_dict = labels_dict
		self.dataset_splits_dict = dataset_splits_dict

def plot_against_steps(collated_results, models, dataset_splits):
	if datset_splits == "all":
		dataset_split_indicies = np.arange(12)
	collated_results[dataset_splits, :, metrics]
	plt.plot()
	

def inconsistent_cols():
	raise BaseException(
						"number of columns is inconsistent with category labels"
						)

holders = []
checklist = [
	"extra_add_or_sub_big",
	"extra_add_sub_multiple_longer",
	"extra_div_big",
	"extra_mixed_longer",
	"extra_mul_big",
	"extra_mul_div_multiple_longer",
	"inter_add_or_sub",
	"inter_add_sub_multiple",
	"inter_div",
	"inter_mixed",
	"inter_mul",
	"inter_mul_div_multiple",
]

for results_dir in model_name_list:
	if os.path.isdir(results_dir):
		all_results_list = []
		# read as text
		# get dataset_splits from checklist
		for dataset_split in checklist:
			print("found {:^30}in {:^60}".format(dataset_split, results_dir))
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
			all_results_list.append(array)
		all_results_array = np.array(all_results_list)
		labels_dict = dict([(labels[i], i) for i in range(len(labels))])
		dataset_splits_dict = dict([(checklist[i], i) for i in range(len(checklist))])
		holders.append(dataHolder(all_results_array.copy(), labels_dict, dataset_splits_dict))
	else:
		raise BaseException(
			"Could not find {} folder".format(results_dir)
			)

