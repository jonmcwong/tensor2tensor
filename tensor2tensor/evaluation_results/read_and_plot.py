import sys
import matplotlib.pyplot as plt
import numpy as np
import os
from  matplotlib.colors import hsv_to_rgb as hsv_to_rgb
# read_as_bytestring = bool(argv[2]) if argn > 2 else None

model_names_list = [
	# "transformer-base_test-2020-06-19", # Dont delete, code will crash
	"transformer-base_test-dropout01-2020-06-24",
	"transformer-base_test-dropout03-2020-06-20",
	"transformer-base_test-no-dropout-2020-06-19",
	"transformer-base_test_dropout02-2020-06-19",
	"transformer-noam-dropout0-2020-06-20",
	"transformer-noam-dropout01-2020-06-20",
	"transformer-noam-dropout02-2020-06-20",
	"transformer-noam-dropout03-2020-06-20",
	"transformer-quick-base-dropout01-2020-06-21",
	"transformer-quick-noam-dropout01-2020-06-21",
	"universal_transformer-base_test-loss-0001-2020-06-21",
	"universal_transformer-base_test-loss-001-2020-06-21",
	"universal_transformer-base_test_loss_0005-2020-06-21",
	"universal_transformer-global-lowerlr0-02-2020-06-23",
	"universal_transformer-lowerlr0-02-2020-06-23",
	"universal_transformer-ut-lowerlr0-002-2020-06-23",
	"combined_transformer-base-dropout01",
	"combined_transformer-noam-dropout01",

]
model_names_dict = dict([(model_names_list[i], i) for i in range(len(model_names_list))])

dataset_splits_list = [
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
dataset_splits_dict = dict([(dataset_splits_list[i], i) for i in range(len(dataset_splits_list))])

all_results_list = []
# print(results_dir, read_as_bytestring)

class dataHolder:
	def __init__(self, all_results_list, labels_dict, dataset_splits_dict):
		self.all_results_list = all_results_list
		self.labels_dict = labels_dict
		self.dataset_splits_dict = dataset_splits_dict

def decide_model_colours(models):
	unique_cols = list(set(models))
	col_gap = 1/len(unique_cols)
	col_map = dict([(unique_cols[i], hsv_to_rgb([i*col_gap, 1.0, 1.0])) for i in range(len(unique_cols))])
	return col_map

def decide_split_colours(split):
	return hsv_to_rgb(((dataset_splits_dict[split]%6)/6, 1.0, 1.0))

def make_md(models, dataset_splits):
	if models == "all" or models[0] == "all":
		if dataset_splits == "all" or dataset_splits[0] == "all":
			raise ValueError("maximum one of the arguments can be 'all'")
		else:
			D_list = dataset_splits
			M_list = model_names_list
	else:
		if dataset_splits == "all" or dataset_splits[0] == "all":
			D_list = dataset_splits_list
			M_list = models
		else:
			D_list = dataset_splits
			M_list = models
	return [(j, i) for i in D_list for j in M_list]

def plot_against_steps(models_and_dataset_splits,
						title="asdfjdb",
					font_size=12,
					xlim=None,
					save_name="Latest_plot.png",
					col_model=False,
					col_split=False,
					include_model_name=False,
					xlabel="Accuracy"):
	mdis = index(models_and_dataset_splits)
	model_indicies = mdis[:, 0]
	dataset_split_indicies = mdis[:, 1]
	col_dict = decide_model_colours(model_indicies)
	data_to_plot = database[:, model_indicies, dataset_split_indicies]
	for i in range(data_to_plot.shape[-1]):
		print(models_and_dataset_splits[i][1].startswith("extra"))
		if models_and_dataset_splits[i][1].startswith("extra"):
			linestyle = "--"
		else:
			linestyle = "-"
		if col_model:
			linecolor = col_dict[model_indicies[i]]
		else col_split:
			linecolor = decide_split_colours(models_and_dataset_splits[i][1])
		label = " with ".join(models_and_dataset_splits[i]) if include_model_name else models_and_dataset_splits[i][1]
		plt.plot(data_to_plot[0, i], data_to_plot[1, i],
			label=label,
			linestyle=linestyle,)
	plt.rcParams["font.size"] = 12
	plt.grid(which="major", axis="both")
	plt.title(title)
	plt.xlabel("steps")
	plt.ylabel(xlabel)
	if xlim:
		plt.xlim(xlim[0], xlim[1])
		plt.ticklabel_format(style='plain', axis='x')
	plt.legend()
	plt.show()
	plt.savefig(save_name)
	
def get_i(x):
	if x in model_names_list:
		return model_names_dict[x]
	if x in dataset_splits_list:
		return dataset_splits_dict[x]

index = np.vectorize(get_i)

def inconsistent_cols():
	raise BaseException(
						"number of columns is inconsistent with category labels"
						)

holders = []

for results_dir in model_names_list:
	if "combined" in results_dir:
		continue
	elif os.path.isdir(results_dir):
		all_results_list = []
		# read as text
		# get dataset_splits from dataset_splits_list
		for dataset_split in dataset_splits_list:
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
		labels_dict = dict([(labels[i], i) for i in range(len(labels))])
		dataset_splits_dict = dict([(dataset_splits_list[i], i) for i in range(len(dataset_splits_list))])
		holders.append(dataHolder(all_results_list[:], labels_dict, dataset_splits_dict))
	else:
		raise BaseException(
			"Could not find {} folder".format(results_dir)
			)

database = np.empty((2, len(model_names_list), len(dataset_splits_list)), dtype=np.object)
for i_qu, question in enumerate(holders):
	question_data = []
	for i_sp, split in enumerate(question.all_results_list):
		gs_index = question.labels_dict["global_step"]
		aps_index = question.labels_dict["accuracy_per_sequence"]
		split_gs = []
		split_aps = []
		for i_st, step in enumerate(split):
			split_gs.append(step[gs_index])
			split_aps.append(step[aps_index])
		database[0, i_qu, i_sp] = split_gs
		database[1, i_qu, i_sp] = split_aps

for k in range(database.shape[2]):
	head_noam_gs, tail_noam_gs = database[0,
		index(["transformer-quick-noam-dropout01-2020-06-21",
			"transformer-noam-dropout01-2020-06-20"]), k]
	head_base_gs, tail_base_gs = database[0,
		index(["transformer-quick-base-dropout01-2020-06-21",
			"transformer-base_test-dropout01-2020-06-24"]), k]
	head_noam_aps, tail_noam_aps = database[1,
		index(["transformer-quick-noam-dropout01-2020-06-21",
			"transformer-noam-dropout01-2020-06-20"]), k]
	head_base_aps, tail_base_aps = database[1,
		index(["transformer-quick-base-dropout01-2020-06-21",
			"transformer-base_test-dropout01-2020-06-24"]), k]

	full_base_gs = np.array(head_base_gs[:] + tail_base_gs[1:])
	full_base_aps = np.array(head_base_aps[:] + tail_base_aps[1:])
	argsort_base = full_base_gs.argsort()
	full_base_gs = full_base_gs[argsort_base]
	full_base_aps = full_base_aps[argsort_base]

	full_noam_gs = np.array(head_noam_gs[:] + tail_noam_gs[1:])
	full_noam_aps = np.array(head_noam_aps[:] + tail_noam_aps[1:])
	argsort_noam = full_noam_gs.argsort()
	full_noam_gs = full_noam_gs[argsort_noam]
	full_noam_aps = full_noam_aps[argsort_noam]
	database[0, index("combined_transformer-noam-dropout01"), k] = full_noam_gs
	database[1, index("combined_transformer-noam-dropout01"), k] = full_noam_aps
	database[0, index("combined_transformer-base-dropout01"), k] = full_base_gs
	database[1, index("combined_transformer-base-dropout01"), k] = full_base_aps








# def decide_model_colours(models, dataset_splits):
# 	if len(unique_cols) != 1:
# 		tmp_m = list(set(models))
# 		unique_cols = dict([(tmp[i], i), for i in list(set(models))])
# 		col_map = [hsv_to_rgb([unique_cols[i]*len(unique_cols), 1.0, 1.0]) for i in models]
# 		return col_map
# 	else:
# 		# tmp_d = list(set(dataset_splits))
# 		six_map = [hsv_to_rgb([i/6, 1.0, 1.0]) for i in range(6)]
# 		return six_map + six_map

# def make_md(models, dataset_splits):
# 	if models == "all" or models[0] == "all":
# 		if dataset_splits == "all" or dataset_splits[0] == "all":
# 			raise ValueError("maximum one of the arguments can be 'all'")
# 		else:
# 			D_list = dataset_splits
# 			M_list = model_names_list
# 	else:
# 		if dataset_splits == "all" or dataset_splits[0] == "all":
# 			D_list = dataset_splits_list
# 			M_list = models
# 		else:
# 			D_list = dataset_splits
# 			M_list = models
# 	return [(j, i) for i in D_list for j in M_list]

# def plot_against_steps(models_and_dataset_splits,
# 						title="asdfjdb",
# 					font_size=12,
# 					xlim=None,
# 					save_name="Latest_plot.png",
# 					col_match=False,
# 					include_model_name=False):
# 	mdis = index(models_and_dataset_splits)
# 	model_indicies = mdis[:, 0]
# 	dataset_split_indicies = mdis[:, 1]
# 	col_dict = decide_model_colours(model_indicies, dataset_split_indicies)
# 	data_to_plot = database[:, model_indicies, dataset_split_indicies]
# 	for i in range(data_to_plot.shape[-1]):
# 		print(models_and_dataset_splits[i][1].startswith("extra"))
# 		if models_and_dataset_splits[i][1].startswith("extra"):
# 			linestyle = "--"
# 		else:
# 			linestyle = "-"
# 		if col_match:
# 			linecolor = col_dict[i]
# 		label = " with ".join(models_and_dataset_splits[i]) if include_model_name else models_and_dataset_splits[i][1]
# 		plt.plot(data_to_plot[0, i], data_to_plot[1, i],
# 			label=label,
# 			linestyle=linestyle,)
# 	plt.rcParams["font.size"] = 12
# 	plt.grid(which="major", axis="both")
# 	plt.title(title)
# 	plt.xlabel("number of steps")
# 	plt.ylabel("accuracy_per_sequence")
# 	if xlim:
# 		plt.xlim(xlim[0], xlim[1])
# 		plt.ticklabel_format(style='plain', axis='x')
# 	plt.legend()
# 	plt.show()
# 	plt.savefig(save_name)
	