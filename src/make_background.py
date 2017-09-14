from __future__ import division
import cv2
import os
import xml.etree.ElementTree as ET
import cv2
from random import randint
from PIL import Image
from collections import namedtuple

Rectangle = namedtuple('Rectangle', 'xmin ymin xmax ymax')

def random_bbox(bbox):
	left = 0
	right = 0
	upper = 0
	lower = 0
	while right-left < 50 or lower-upper < 50:
		x1 = randint(bbox[0], bbox[2])
		x2 = randint(bbox[0], bbox[2])
		while x2 == x1:
			x2 = randint(bbox[0], bbox[2])
		y1 = randint(bbox[1], bbox[3])
		y2 = randint(bbox[1], bbox[3])
		while y2 == y1:
			y2 = randint(bbox[1], bbox[3])
		left = min(x1, x2)
		right = max(x1, x2)
		upper = min(y1, y2)
		lower = max(y1, y2)
	return [left, upper, right, lower]

def area_intersection(a, b):  # returns None if rectangles don't intersect
    dx = min(a.xmax, b.xmax) - max(a.xmin, b.xmin)
    dy = min(a.ymax, b.ymax) - max(a.ymin, b.ymin)
    if (dx>=0) and (dy>=0):
        return dx*dy

def area(a):
	dx = a.xmax - a.xmin
	dy = a.ymax - a.ymin
	return dx*dy

folders = ('train','test')
background = []

for dir in folders:
	raw_image = '../datasets/'+dir+'/JPEGImages/'
	anno_image = '../datasets/'+dir+'/Annotations/'
	train_dataset = '../datasets/train/final/'
	for i, anno_filename in enumerate(os.listdir(anno_image)):
		tree = 	ET.parse(anno_image+anno_filename)
		tmp = anno_filename.split('.')
		img_filename = tmp[0] + '.jpg'
		im = Image.open(raw_image+img_filename)
		bbox = im.getbbox()
		box = random_bbox(bbox)
		random_tile = im.crop(box)
		rect_random = Rectangle(box[0], box[1], box[2], box[3])
		root = tree.getroot()
		tmp_arr = []
		for i,object in enumerate(root.findall('object')):
			bndbox = object.find('bndbox')
			class1 = str(object[0].text)
			xmin = int(bndbox[0].text)
			ymin = int(bndbox[1].text)
			xmax = int(bndbox[2].text)
			ymax = int(bndbox[3].text)
			rect_class = Rectangle(xmin, ymin, xmax, ymax)
			intersect_area = area_intersection(rect_random, rect_class)
			if intersect_area == None:
				intersect_area = 0
			total_area = area(rect_random) + area(rect_class) - intersect_area
			tmp_arr.append(intersect_area/total_area)
		background.append((random_tile, max(tmp_arr)))
	break

background.sort(key=lambda tup: tup[1])
for i in range(800):
	background[i][0].save(train_dataset+'__background__/'+str(i)+'.jpg',"JPEG")


