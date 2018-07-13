#run this in any directory add -v for verbose
#pip install Image
import os
import sys
from PIL import Image

def buildDirectories(file, subdir):
	pwd = subdir
	#makes two new dirs for compressed and resized
	new_directory = pwd + '/compressed'
	new_filename = 'Compressed_' + pwd.replace('/', '_') + file

	if not os.path.exists(new_directory):
		os.mkdir(new_directory)

	path_to_compressed = new_directory + '/Compressed_' + file

	return path_to_compressed

def compressImages(file, filepath, subdir, verbose=False):
	#What percentage quality of the original image to keep. 65 to 85 is best bet here
	compress_quality = 80
	oldsize = os.stat(filepath).st_size
	picture = Image.open(filepath)

	#Build the directories
	path_compress = buildDirectories(file, subdir)

	#Save the compressed pic to its correct path
	picture.save(path_compress,optimize=True,quality=compress_quality)

	#Log information about the compression savings
	newsize = os.stat(os.path.join(os.getcwd(), path_compress)).st_size
	percent = round((oldsize-newsize)/float(oldsize)*100, 2)

	if (verbose):
		print("File compressed from %s to %s or %s%%" % (oldsize,newsize,percent))

	return percent

def main():
	verbose = False
	#checks for verbose flag
	if (len(sys.argv)>1):
		if (sys.argv[1].lower()=="-v"):
			verbose = True

	#finds present working dir
	pwd = os.getcwd()

	tot = 0
	num = 0
	for subdir, dirs, files in os.walk(pwd):
		for file in files:
			if os.path.splitext(file)[1].lower() in ('.jpg', '.jpeg', '.png'):
				filepath = os.path.join(subdir, file)
				num += 1
				tot += compressImages(file, filepath, subdir, verbose)
	print("Average Compression: %d" % (float(tot)/num))
	print("Done")

if __name__ == "__main__":
	main()
