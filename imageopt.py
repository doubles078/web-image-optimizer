#run this in any directory add -v for verbose
#pip install Image

import os
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

	path_for_compressed_images = path + '/Compressed_and_Resized' + '/Compressed_' + file

	return path_for_compressed_images

def compressImage(filepath):
	#What percentage quality of the original image to keep. 65 to 85 is best bet here
	compress_quality = 80
	oldsize = os.stat(filepath).st_size
	picture = Image.open(filepath)
	#Build the new directory to put the compressed images in
	path_for_compressed_images = buildNewDirectoryForCompressedImages(filepath) 	

	#Resize the images and save them
	resizeImages(picture, path_for_compressed_images, compress_quality)

	#Keep these numbers for console logging
	newsize = os.stat(os.path.join(os.getcwd(), path_for_compressed_images)).st_size
	percent = round((oldsize-newsize)/float(oldsize)*100, 2)

	return (oldsize, newsize, percent)


def resizeImages(picture, path_for_compressed_images, compress_quality):
	#Static width in pixels.  Could also change this to be a param in the CLI
	new_width = 1200

	for orientation in ExifTags.TAGS.keys():
		if ExifTags.TAGS[orientation]=='Orientation':
			break

	try:
		e = picture._getexif()    # returns None if no EXIF data
	except:
		e = None

	if e is not None:
		exif=dict(e.items())

		try:
			orientation = exif[orientation]
		except:
			print("There was no orientation # so I set it to 0")
			orientation = 0

	if orientation == 1 or orientation == 0:
		width, height = picture.size
		new_height = int(new_width * height / width)
		print("Height: " + str(height) + "Width: " + str(width) + ' New height: ')
	else:
		height, width = picture.size
		new_height = int(new_width * height / width)

	if width >= 1200:
		if width > height:
			if orientation == 1 or orientation == 0:
				picture_resized = picture.resize((new_width, new_height), Image.ANTIALIAS)
				print("Width bigger, width: " + str(width) + " height: " + str(height) + " New width: " + str(new_width) + " New height: " + str(new_height))
			else:
				picture_resized = picture.resize((new_height, new_width), Image.ANTIALIAS)
		else:
			if orientation == 6:
				picture_resized = picture.resize((new_height, new_width), Image.ANTIALIAS)
				print("ORIENTATION 6 Width bigger, width: " + str(width) + " height: " + str(height) + " New width: " + str(new_width) + " New height: " + str(new_height))
			else:
				picture_resized = picture.resize((new_width, new_height), Image.ANTIALIAS)
				print("Height bigger, width: " + str(width) + " height: " + str(height))
	else:
		picture_resized = picture

	print("Orientation: " + str(orientation))

	if orientation == 3:
		picture_resized = picture_resized.transpose(Image.ROTATE_180)
	elif orientation == 6:
		picture_resized = picture_resized.transpose(Image.ROTATE_270)
		print("I reoriented")
	elif orientation == 8:
		picture_resized = picture_resized.transpose(Image.ROTATE_90)



	#Save the compressed and resized image to the correct path
	picture_resized.save(path_for_compressed_images, optimize=True, quality=compress_quality)

	return picture_resized



def main():
	verbose = False

	#Checks the arguments passed in when running the python script from a console
	if (len(sys.argv)>1):
		if (sys.argv[1].lower()=="-v"):
			verbose = True

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
				image = compressImage(filepath)
				print(file)
				if (verbose):
					print("File compressed from %s to %s or %s%%" % (image[0],image[1],image[2]))

if __name__ == "__main__":
	main()
