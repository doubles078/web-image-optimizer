# WebImageOptimizer
Looks in a directory for .jpg, .jpeg, and .png files.  Then compresses and resizes them based on your specs.

## Steps to Run
1. Make sure you have Python 3 installed
2. Clone the repo into a directory full of images or full of more directories with images inside of them
3. In your Terminal/CMD Prompt, run pip install Image
4. Now run python imageopt.py
5. Add -v for stats on compression or an integer to set the max picture width
6. i.e. python imageopt.py -v 1000


Thanks to [Shantanu Joshi](https://shantanujoshi.github.io/python-image-compression/) for the starter script.  I added orientation checks, png support and directory creation.