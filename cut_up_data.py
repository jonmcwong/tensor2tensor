import os

root = "gs://us_bucketbucket"
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
		for i in range(DIVISIONS):
			if i != DIVISIONS-1:
				piece = file.[i*slice_index:(i+1)*slice_index]
			else:
				piece = file.[i*slice_index:]
			os.join("train-easy-group{}".format(i), f_name)
		print("added" + f_name)

