import sys
import matplotlib.pyplot as plt
import numpy as np
import os
from  matplotlib.colors import hsv_to_rgb as hsv_to_rgb
# read_as_bytestring = bool(argv[2]) if argn > 2 else None

model_names_list = [
	"transformer-base-relu-dp-00-2020-06-25",
	"transformer-base-relu-dp-01-2020-06-25",
	"transformer-base-relu-dp-02-2020-06-25",
	"transformer-base-relu-dp-03-2020-06-25",
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

dataset_split_style = ['-', '--', '-.', ':']
dataset_splits_list = [
	"inter_add_or_sub",		
	"extra_add_or_sub_big",			
	"inter_add_sub_multiple",	
	"extra_add_sub_multiple_longer",
	"inter_mul",				
	"extra_mul_big",				
	"inter_div",				
	"extra_div_big",				
	"inter_mixed",				
	"extra_mixed_longer",			
	"inter_mul_div_multiple",	
	"extra_mul_div_multiple_longer",
	# "single_inter",
	# "single_extra",
]

dataset_splits_dict = dict([(dataset_splits_list[i], i) for i in range(len(dataset_splits_list))])

dataset_splits8_list = [
	"train_easy_mul",				
	"train_medium_mul",				
	"train_hard_mul",				
	"extra_mul_big",				
	"train_easy_add_sub_multiple",	
	"train_medium_add_sub_multiple",
	"train_hard_add_sub_multiple",	
	"extra_add_sub_multiple_longer",
	"train_easy_add_or_sub",		
	"train_medium_add_or_sub",		
	"train_hard_add_or_sub",		
	"extra_add_or_sub_big",			
]
dataset_splits8_dict = dict([(dataset_splits8_list[i], i) for i in range(len(dataset_splits8_list))])

class dataHolder:
	def __init__(self, all_results_list, labels_dict, dataset_splits_dict):
		self.all_results_list = all_results_list
		self.labels_dict = labels_dict
		self.dataset_splits_dict = dataset_splits_dict

def decide_colours(items, doubleup=False):
	if not doubleup:
		unique_cols = list(set(items))
		col_gap = 1.0/len(unique_cols)
		col_map = dict([(unique_cols[i], hsv_to_rgb([i*col_gap, 1.0, .8])) for i in range(len(unique_cols))])
		return [col_map[i] for i in items]
	else:
		unique_cols = list(set([i//2 for i in items]))
		col_gap = 1.0/len(unique_cols)
		col_map = dict([(unique_cols[i]*2, hsv_to_rgb([i*col_gap, 1.0, .8])) for i in range(len(unique_cols))])
		col_map.update([(unique_cols[i]*2+1, hsv_to_rgb([i*col_gap, 1.0, .8])) for i in range(len(unique_cols))])
		return [col_map[i] for i in items]

def decide_width(items):
	unique_cols = list(set(items))
	width_gap = 1.0
	width_map = dict([(unique_cols[i], 1.0+i*width_gap) for i in range(len(unique_cols))])
	return [width_map[i]  for i in items]

def decide_split_colours(split):
	return hsv_to_rgb((float(dataset_splits_dict[split]//2)/6, 1.0, 1.0))

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


def plot_against_difficulty(holder8,
							title="???",
						ylabel="Accuracy",
						font_size=15,
						ylim=None,
						ckpt_num=-1):
	arr = np.array(holder8.all_results_list)
	ia = holder8.labels_dict["accuracy_per_sequence"]
	arr_bit = arr[:, ckpt_num, ia]
	arr1 = arr[:, -1, ia]
	arr2 = arr[:, -2, ia]
	arr3 = arr[:, -3, ia]
	arr4 = arr[:, -4, ia]
	arr5 = arr[:, -5, ia]
	arr6 = arr[:, -6, ia]
	# plt.plot(range(4), arr_bit[8:121
	plt.plot(range(4), arr1[0:4], label="mul")
	plt.plot(range(4), arr1[4:8], label="add_sub_multiple")
	plt.plot(range(4), arr1[8:12], label="add_or_sub")
	# # plt.plot(range(4), arr2[8:12], label="add_or_sub")
	# plt.plot(range(4), arr2[4:8], label="add_su2b_multiple")
	# # plt.plot(range(4), arr2[0:4], label="mul")
	# # plt.plot(range(4), arr3[8:12], label="add_o3r_sub")
	# plt.plot(range(4), arr3[4:8], label="add_sub_multiple")
	# # plt.plot(range(4), arr3[0:4], label="mul")
	# # plt.plot(range(4), arr4[8:12], label="add_o4r_sub")
	# plt.plot(range(4), arr4[4:8], label="add_sub_multiple")
	# # plt.plot(range(4), arr4[0:4], label="mul")
	# # plt.plot(range(4), arr5[8:12], label="add_o5r_sub")
	# plt.plot(range(4), arr5[4:8], label="add_sub_multiple")
	# # plt.plot(range(4), arr5[0:4], label="mul")
	# # plt.plot(range(4), arr6[8:12], label="add_o6r_sub")
	# plt.plot(range(4), arr6[4:8], label="add_sub_multiple")
	# # plt.plot(range(4), arr6[0:4], label="mul")
	difficulties = ["easy", "medium", "hard", "extrapolate"]


	plt.rcParams["font.size"] = 12
	plt.grid(which="major", axis="both")
	plt.title(title)
	plt.xlabel("Difficulty", fontsize=font_size)
	plt.ylabel(ylabel, fontsize=font_size)
	plt.xticks(range(4), difficulties, rotation=0)
	if ylim:
		plt.ylim(ylim[0], ylim[1])
		plt.ticklabel_format(style='plain', axis='y')
	plt.legend()
	plt.ion
	plt.show(block=False)


def plot_against_steps(ax, models_and_dataset_splits,
						title="asdfjdb",
					font_size=15,
					multi_model=None,
					xlim=None,
					ylim=None,
					save_name="Latest_plot.png",
					include_model_name=False,
					ylabel="Accuracy",
					flip=False,
					hold=False,
					legend=True,
					linewidth=None):
	mdis = index(models_and_dataset_splits)
	model_indicies = mdis[:, 0]
	dataset_split_indicies = mdis[:, 1]
	data_to_plot = database[:, model_indicies, dataset_split_indicies]
	if multi_model == None:
		if len(set(model_indicies)) > len(set(dataset_split_indicies)):
			multi_model = True
		else:
			multi_model = False
	if multi_model:
		linecolor_list = decide_colours(model_indicies)
		linewidth_list = decide_width(dataset_split_indicies)
	else:
		linecolor_list = decide_colours(dataset_split_indicies, doubleup=True)
		linewidth_list = decide_width(model_indicies)
	if linewidth != None:
		linewidth_list = [linewidth for _ in range(data_to_plot.shape[-1])]
	for i in range(data_to_plot.shape[-1]):
		if models_and_dataset_splits[i][1].startswith("extra"):
			linestyle = "--"
		else:
			linestyle = "-"
		linecolor = linecolor_list[i]
		linewidth = linewidth_list[i]
		if include_model_name == "only":
			label = str(models_and_dataset_splits[i][1])[0:5]+"polate, dropout 0."+str(models_and_dataset_splits[i][0]).split("-")[4][-1]
		elif include_model_name:
			label = str(" with ".join(models_and_dataset_splits[i]))
		else:
			label = str(models_and_dataset_splits[i][1])
		x, y = data_to_plot[0, i], data_to_plot[1, i]
		if flip:
			x = np.flip(x)
		ax.plot([0]+x, [0]+y,
			label=label,
			linestyle=linestyle,
			linewidth=linewidth,
			color=linecolor
			)
	plt.rcParams["font.size"] = 12
	ax.grid(which="major", axis="both")
	ax.title.set_text(title)
	ax.set_xlabel("steps", fontsize=font_size)
	ax.set_ylabel(ylabel, fontsize=font_size)
	if xlim:
		ax.set_xlim(xlim[0], xlim[1])
		# ax.ticklabel_format(style='plain', axis='x')
	if ylim:
		ax.set_ylim(ylim[0], ylim[1])
		# ax.ticklabel_format(style='plain', axis='y')
	if legend:
		# handles, labels = plt.gca().get_legend_handles_labels()
		# by_label = dict(zip(labels, handles))
		# ax.legend(by_label.values(), by_label.keys())
		ax.legend()
	if not hold:
		plt.show()
	
def get_i(x):
	if x in model_names_list:
		return model_names_dict[x]
	if x in dataset_splits_list:
		return dataset_splits_dict[x]
	raise ValueError("No match for", x)
index = np.vectorize(get_i)


def inconsistent_cols():
	raise BaseException(
						"number of columns is inconsistent with category labels"
						)


all_results_list = []
# print(results_dir, read_as_bytestring)
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



all_results_list = []
# read as text
results_dir = "transformer-data-easy-2020-06-24"
# get dataset_splits from dataset_splits8_list
for dataset_split in dataset_splits8_list:
	print("found {:^30} in {:^60}".format(dataset_split, results_dir))
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
labels8_dict = dict([(labels[i], i) for i in range(len(labels))])
holder8 = dataHolder(all_results_list[:], labels_dict, dataset_splits8_dict)



fig, axs = plt.subplots(3, 2)
fig.suptitle('Accuracy On Each Question Type on Transformer Base With Dropout Levels: 0.0, 0.1, 0.2, 0.3', fontsize=16)
for i in range(3):
	for j in range(2):
		plot_against_steps(
			axs[i, j],
			make_md([
				"transformer-base-relu-dp-00-2020-06-25",
				"transformer-base-relu-dp-01-2020-06-25",
				"transformer-base-relu-dp-02-2020-06-25",
				"transformer-base-relu-dp-03-2020-06-25",
			    ], dataset_splits_list[2*(3*j+i):2*(3*j+i+1)]),
			xlim=(-10000, 905000),
			ylim=(-0.05, 1.05),
			title=" and ".join(dataset_splits_list[2*(3*j+i):2*(3*j+i+1)]),
			# save_name="Latest_plot.png", 
			# font_size=20,
			include_model_name="only",
			multi_model=True,
			hold=True,
			legend=not(i+j),
			linewidth=1
		)
plt.show()

# axs[0,0].plot((1,2,3,4), (2,4,3,5))
# plt.show()
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
	