import os
import mmap
import string
from collections import Counter


def mapcount(filename):
	lines = 0
	f = open(filename, "r+")
	buf = mmap.mmap(f.fileno(), 0)
	readline = buf.readline
	while readline():
		lines += 1
	return lines

def prepare(dir_path):
	remove_digits = str.maketrans('', '', string.digits)
	remove_punctuations = str.maketrans('', '', string.punctuation)
	# prepare empty counter for accumulating words from all abstracts
	global_dict = Counter()
	# get all abstract files from the directory
	filenames = os.listdir(dir_path)
	# prepare each file
	for ifile, filename in enumerate(filenames, 1):
		curr_line = 0
		local_dict = Counter()
		print(f"preparing file {ifile} of {len(filenames)}")
		total_lines = mapcount(f"{dir_path}/{filename}")
		print(f"preparing {total_lines} lines")
		# use file iterator to save RAM space and increase speed
		with open(f"{dir_path}/{filename}") as file_iterator:
			for line in file_iterator:
				# I have seen empty lines (line only with \n) so ignore these lines
				if len(line) > 2:
					# remove all \t\n\r, convert to lowercase, remove non-letters an punctuations
					words = line.rstrip().lower().translate(remove_digits).translate(remove_punctuations).split()
					# append these words to the global word counter and local
					global_dict.update(words)
					local_dict.update(words)
				# increment the number of prepared line
				curr_line += 1
				# show the progress
				if curr_line % 100000 == 0:
					print(f"{curr_line}/{total_lines} ({curr_line / total_lines * 100:.2f}%) lines are done")
		# save local dictionary for current abstract file (for working with separated abstracts if need)
		with open(f"{dir_path}/dict_{filename}", 'w') as dict_file:
			for k, v in local_dict.most_common():
				dict_file.write(f"{k}: {v}\n")
	# save the global dict
	with open(f"{dir_path}/global_dict", 'w') as dict_file:
		for k, v in global_dict.most_common():
			dict_file.write(f"{k}: {v}\n")


if __name__ == "__main__":
	prepare("/home/alex/Desktop/abs")
