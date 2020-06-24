import os


DIVISIONS = 16
[os.mkdir("train-easy-group{}".format(i)) for i in range(DIVISIONS)]

file_names = os.listdir()
if "arithmetic__add_or_sub.txt" not in file_names:
	raise BaseException(
		"Are you in the right directory?")


for f_name in file_names:
	with open(f_name, "r") as f:
		file = f.readlines()
		slice_index = len(file)//16
		print("added" + f_name)

slice_sizes = [len(f)//16 for f in files]


for n in renage(DIVISIONS):
	if n != DIVISIONS-1:
