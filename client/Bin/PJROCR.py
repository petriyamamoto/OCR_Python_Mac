from ast import Return
import cv2
import numpy as np
import os
from paddleocr import PPStructure
from isBlueCharacter import isBlueCharacter
from ExtractInformation import get_table_data


def PJROCR(image_path):

	#----------------Geometrical Correction----------------------------
	# Read image
	image = cv2.imread(image_path)
	# Convert image to grayscale
	gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	# Use canny edge detection
	edges = cv2.Canny(gray,50,150,apertureSize=3)
	# Apply HoughLinesP method to
	# to directly obtain line end points
	lines_list =[]
	lines = cv2.HoughLinesP(
				edges, # Input edge image
				1, # Distance resolution in pixels
				np.pi/180, # Angle resolution in radians
				threshold=140, # Min number of votes for valid line
				minLineLength=100, # Min allowed length of line
				maxLineGap=10 # Max allowed gap between line for joining them
				)

	# Iterate over points
	angle = 0
	for points in lines:
		# Extracted points nested in the list
		x1,y1,x2,y2=points[0]
		# Draw the lines joing the points
		# On the original image
		if x2 - x1 > 100:
				angle = (y2 - y1)/(x2-x1)
				break  
		
	# Save the result image
	height, width = image.shape[:2]
	center = (width/2, height/2)
	rotate_matrix = cv2.getRotationMatrix2D(center=center, angle = (np.arctan(angle)/np.pi*180), scale=1)
	rotated_image = cv2.warpAffine(src=image, M=rotate_matrix, dsize=(width, height))
	# cv2.imwrite('./temp/rotated_image.jpg',rotated_image)

	#-----------------------PaddleOCR Module Start ----------------------------------
	# Chinese image
	table_engine = PPStructure(recovery=True)
	# save_folder = './output'
	# img_path = './temp/rotated_image.jpg'
	img = rotated_image

	result = table_engine(img)
	count = 0
	array_process  =  result[0]['res'].copy()
	raw_data = array_process.copy()
	# torch.save(array_process,'Data1.txt')
	for item in  result[0]['res']:
		p1,p2,p3,p4 = item['text_region']
		x_start = min(p1[0],p2[0],p3[0],p4[0]) 
		x_end = max(p1[0],p2[0],p3[0],p4[0]) 
		y_start = min(p1[1],p2[1],p3[1],p4[1]) 
		y_end = max(p1[1],p2[1],p3[1],p4[1]) 
		subimg = img[int(y_start):int(y_end),int(x_start):int(x_end),:]
		if isBlueCharacter(subimg) == False:
			array_process.remove(item)	
			# count += 1
			# cv2.imwrite('title' + str(count) + '.png',subimg)
	result[0]['res'] = array_process

	# torch.save(array_process,'Data2.txt')
	# ExtractInformation(result[0]['res'],array_process)
	# save_structure_res(result, save_folder,os.path.basename(img_path).split('.')[0])
	# font_path = './font/simfang.ttf' # font provieded in PaddleOCR
	# im_show = draw_structure_result(img, result,font_path=font_path)
	# im_show = Image.fromarray(im_show)
	# im_show.save('./temp/result.jpg')
	return get_table_data(raw_data,array_process)
