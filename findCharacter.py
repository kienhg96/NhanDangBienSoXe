import cv2
import numpy as np
import param as pr

def findCharacter(src):
	result = []
	tmp = []
	resizeImg = cv2.resize(src, (pr.CHAR_HEIGHT_RESIZE, pr.CHAR_WIDTH_RESIZE))
	resizeImg = cv2.cvtColor(resizeImg, cv2.COLOR_BGR2GRAY)
	binaryImg = cv2.adaptiveThreshold(resizeImg, 255, cv2.ADAPTIVE_THRESH_MEAN_C, \
		cv2.THRESH_BINARY, 13, 2)
	copy_binaryImg = np.copy(binaryImg)
	cv2.imshow("binaryImg", binaryImg)
	contours, _ = cv2.findContours(binaryImg, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	# print "len contours: %d" % len(contours)
	i = 0
	for j in xrange(0, len(contours)):
		for k in xrange(0, len(contours[j])):
			if k == 0: 
				xmax = xmin = contours[j][k][0][0]
				ymax = ymin = contours[j][k][0][1]
			else:
				if xmax < contours[j][k][0][0]:
					xmax =  contours[j][k][0][0]
				if xmin > contours[j][k][0][0]:
					xmin =  contours[j][k][0][0]
				if ymax < contours[j][k][0][1]:
					ymax = contours[j][k][0][1]
				if ymin > contours[j][k][0][1]:
					ymin = contours[j][k][0][1]
		w = xmax - xmin
		h = ymax - ymin
		charImg = copy_binaryImg[ymin: ymax, xmin: xmax]
		if h != 0 and w != 0:
			ratio = 1.0 * w / h
			ratioWhite = 1.0 * cv2.countNonZero(charImg) / (w * h)
		else:
			ratio = 1000
			ratioWhite = 1000
		# ratioWhite = 1.0 * cv2.countNonZero(charImg) / w * h
		if w > pr.CHAR_MIN_WIDTH and w < pr.CHAR_MAX_WIDTH \
		and h > pr.CHAR_MIN_HEIGHT and h < pr.CHAR_MAX_HEIGHT \
		and w * h > pr.MIN_WH and ratio > pr.CHAR_MIN_WH_RATIO \
		and ratio < pr.CHAR_MAX_WH_RATIO and ratioWhite > pr.CHAR_MIN_RATIO_WHITE \
		and ratioWhite < pr.CHAR_MAX_RATIO_WHITE:
			cv2.rectangle(resizeImg, (xmin, ymin), (xmax, ymax), 0, 1)
			# result.append(copy_binaryImg[ymin: ymax, xmin: xmax])
			tmp.append({"x": xmin, "elem": charImg})
			# cv2.imshow("%d" % i, copy_binaryImg[ymin: ymax, xmin: xmax])
			# i = i + 1
			# print xmin
	# cv2.imshow("binary", binaryImg)
	# cv2.imshow("resizeImg", resizeImg)
	while len(tmp) != 0:
		i = 0
		for j in xrange(0, len(tmp)):
			if tmp[i]["x"] > tmp[j]["x"]:
				i = j
		result.append(tmp[i]["elem"])
		del tmp[i]
	return result