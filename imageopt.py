import os
import getopt
import sys
from PIL import Image, ExifTags

def buildNewDirectoryForCompressedImages(filepath):
	path, file = os.path.split(filepath)

	#Create the names of the new directories
	new_directory = path + '/Compressed_and_Resized'

	#If the new directory does not exist, then make it
	#This doesnt work and needs fixing
	if not os.path.exists(new_directory):
		os.mkdir(new_directory)

	path_for_compressed_images = path + '/Compressed_and_Resized/Compressed_' + file

	return path_for_compressed_images


def compressImage(filepath, max_picture_width, compression_quality_percent):
	#What percentage quality of the original image to keep. 65 to 85 is best bet here
	oldsize = os.stat(filepath).st_size
	picture = Image.open(filepath)
	#Build the new directory to put the compressed images in
	path_for_compressed_images = buildNewDirectoryForCompressedImages(filepath) 	

	#Resize the images and save them
	resizeImage(picture, path_for_compressed_images, max_picture_width, compression_quality_percent)

	#Keep these numbers for console logging
	newsize = os.stat(os.path.join(os.getcwd(), path_for_compressed_images)).st_size
	percent = round((oldsize-newsize)/float(oldsize)*100, 2)

	picture.close()

	return (oldsize, newsize, percent)


def findPictureOrientation(picture):


	#PNGs dont have this attribute and need to be checked
	if hasattr(picture, '_getexif'):
		e = dict(picture._getexif().items())

	#Finds the correct Exif id number for orientaiton aka 274
	#Then sets orientation equal to it 
	for orientation in ExifTags.TAGS.keys():
		if ExifTags.TAGS[orientation]=='Orientation':
			break
	
	try:
		#If there is orientation data, set it to the orientation variable
		orientation = e[orientation]
	except:
		#If there is no orientation meta data, then default orientation to 0
		print("There was no orientation data so default to 0.")
		orientation = 0
	
	return orientation


def resizeImage(picture, path_for_compressed_images, max_picture_width, compression_quality_percent):
	#Static width in pixels.  Could also change this to be a param in the CLI
	new_width = max_picture_width
	#Return the orientation of the picture
	orientation = findPictureOrientation(picture)

	if orientation in [0,1]:
		width, height = picture.size
	else:
		#PIL seems to flip these if the orientation is not 0 or 1
		height, width = picture.size

	new_height = int(new_width * height / width)

	#If the width of the image is larger than the assigned new width, then resize them
	if width >= new_width:
		if orientation in [0,1]:
			resized_picture = picture.resize((new_width, new_height), Image.ANTIALIAS)
		else:
			resized_picture = picture.resize((new_height, new_width), Image.ANTIALIAS)
	else:
		resized_picture = picture

	picture_resized_and_rotated = rotateResizedPicture(resized_picture, orientation)

	#Save the compressed and resized image to the correct path
	picture_resized_and_rotated.save(path_for_compressed_images, optimize=True, quality=compression_quality_percent)

	return picture_resized_and_rotated


def rotateResizedPicture(resized_picture, orientation):
	if orientation == 3:
		resized_picture = resized_picture.transpose(Image.ROTATE_180)
	elif orientation == 6:
		resized_picture = resized_picture.transpose(Image.ROTATE_270)
	elif orientation == 8:
		resized_picture = resized_picture.transpose(Image.ROTATE_90)

	return resized_picture


def main():
	#Defaulting values
	verbose = False
	max_picture_width = 1200
	compression_quality_percent = 80

	for arg in sys.argv[1:]:
		if arg.lower() in ['-v', 'verbose']:
			verbose = True
		elif int(arg) > 0:
			max_picture_width = int(arg)
			print("Max width set to " + arg)
		else:
			print("No arguments provided defaulting max width to 1200px and verbose output to false. (i.e. -v or an integer for max pic width)")

	#Current Working Directory
	pwd = os.getcwd()

	#Ignore these directories
	exclude = set(['.git', 'venv'])

	for subdir, dirs, files in os.walk(pwd):
		#Walk through the current working directory and all sub directories until there are none left
		dirs[:] = [d for d in dirs if d not in exclude]
		for file in files:
			if os.path.splitext(file)[1].lower() in ('.jpg', '.jpeg', '.png'):
				filepath = os.path.join(subdir, file)
				image = compressImage(filepath, max_picture_width, compression_quality_percent)
				print(file)
				if (verbose):
					print("File compressed from %s to %s or %s%%" % (image[0],image[1],image[2]))

if __name__ == "__main__":
	main()
