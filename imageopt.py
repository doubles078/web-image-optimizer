#run this in any directory add -v for verbose 
#pip install Image
import os
import sys
from PIL import Image

def buildDirectories(file):
	pwd = os.getcwd()
	#makes two new dirs for compressed and resized
	new_directories = [pwd + '/compressed', pwd + '/compressed_and_resized']

	for directory in new_directories:
		if not os.path.exists(directory):
			os.mkdir(directory)
		
	path_to_compressed = new_directories[0] + '/Compressed_' + file
	path_to_resized = new_directories[1] + '/Smaller_' + file

	return [path_to_compressed, path_to_resized]


def resizeImages(picture, path_to_resized, compress_quality):
	#Static width in pixels.  Could also change this to be a param in the CLI
	new_width = 300
	width, height = picture.size
	new_height = int(new_width * height / width)
	picture_resized = picture.resize((new_width, new_height), Image.ANTIALIAS)

	#Save the compressed and resized image to the correct path
	picture_resized.save(path_to_resized, optimize=True,quality=compress_quality)

	return picture_resized


def compressImages(file,  verbose=False):
	#What percentage quality of the original image to keep. 65 to 85 is best bet here
	compress_quality = 85

	filepath = os.path.join(os.getcwd(), file)
	oldsize = os.stat(filepath).st_size
	picture = Image.open(filepath)

	#Build the directories
	path_compress = buildDirectories(file)[0]
	path_resize = buildDirectories(file)[1]

	#Save the compressed pic to its correct path
	picture.save(path_compress,optimize=True,quality=compress_quality) 
	resizeImages(picture, path_resize, compress_quality)

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
	for file in os.listdir(pwd):
		if os.path.splitext(file)[1].lower() in ('.jpg', '.jpeg', '.png'):
			num += 1
			tot += compressImages(file, verbose)
	print("Average Compression: %d" % (float(tot)/num))
	print("Done")

if __name__ == "__main__":
	main()