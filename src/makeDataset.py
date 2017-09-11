import cv2
import os
import xml.etree.ElementTree as ET
import cv2

folders = ("train","test")

train_classes = {
	'aeroplane' : [],
	'bicycle' : [],
	'bird' : [],
	'boat' : [],
	'bottle' : [],
	'bus' : [],
	'car' : [],
	'cat' : [],
	'chair' : [],
	'cow' : [],
	'diningtable' : [],
	'dog' : [],
	'horse' : [],
	'motorbike' : [],
	'person' : [],
	'pottedplant' : [],
	'sheep' : [],
	'sofa' : [],
	'train' : [],
	'tvmonitor' : []
}
test_classes = train_classes


for dir in folders:
	print dir
	raw_image = '../datasets/'+dir+'/VOC2007/JPEGImages/'
	anno_image = '../datasets/'+dir+'/VOC2007/Annotations/'
	for anno_filename in os.listdir(anno_image):
		tree = 	ET.parse(anno_image+anno_filename)
		tmp = anno_filename.split('.')
		img_filename = tmp[0] + '.jpg'
		print anno_filename, img_filename
		img = cv2.imread(raw_image+img_filename)
		root = tree.getroot()
		print root
		for object in root.findall('object'):
			class1 = str(object.find('name').text)
			bndbox = object.find('bndbox')
			print class1, bndbox[0].text, bndbox[1].text, bndbox[2].text, bndbox[3].text
			class1 = str(object[0].text)
			xmin = int(bndbox[0].text)
			ymin = int(bndbox[1].text)
			xmax = int(bndbox[2].text)
			ymax = int(bndbox[3].text)
			crop_img = img[ymin:ymax, xmin:xmax]
			if dir == 'train':
				train_classes[class1].append(crop_img)
			else:
				test_classes[class1].append(crop_img)
		# break

print train_classes, test_classes


