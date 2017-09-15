import glob
import shutil
import os
import xml.etree.ElementTree as ET

arr = ['aeroplane', 'bicycle', 'car', 'cat', 'dog']

src_dir1 = "../datasets/test/JPEGImages/"
src_dir2 = "../datasets/test/Annotations/"
dst_dir1 = "../datasets/test/final/JPEGImages/"
dst_dir2 = "../datasets/test/final/Annotations/"
for anno_filename in os.listdir(src_dir2):
	tree = 	ET.parse(src_dir2+anno_filename)
	tmp = anno_filename.split('.')
	img_filename = tmp[0] + '.jpg'
	root = tree.getroot()
	# print root
	for i,object in enumerate(root.findall('object')):
		class1 = str(object.find('name').text)
		if class1 in arr:
			shutil.copy(src_dir1+img_filename, dst_dir1)
			shutil.copy(src_dir2+anno_filename, dst_dir2)
			break