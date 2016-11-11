import cv2
import numpy as np
import param as pr

def findPlate(src, color_src = None): # color_src for Debug only
	result = []
	contours, _ = cv2.findContours(src, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	#con = np.zeros((pr.IMAGE_WIDTH_SIZE, pr.IMAGE_HEIGHT_SIZE), np.uint8);
	for i in xrange(0, len(contours)):
		for j in xrange(0, len(contours[i])):
			if j == 0:
				xmax = xmin = contours[i][j][0][0]
				ymax = ymin = contours[i][j][0][1]
			else:
				if xmax < contours[i][j][0][0]:
					xmax =  contours[i][j][0][0]
				if xmin > contours[i][j][0][0]:
					xmin =  contours[i][j][0][0]
				if ymax < contours[i][j][0][1]:
					ymax = contours[i][j][0][1]
				if ymin > contours[i][j][0][1]:
					ymin = contours[i][j][0][1]
		rh, rw = src.shape
		if (xmin + pr.LEFT_OFFSET) > 0:
			xmin = xmin + pr.LEFT_OFFSET
		else: 
			xmin = 0

		if (xmax + pr.RIGHT_OFFSET) < rh:
			xmax = xmax + pr.RIGHT_OFFSET
		else: 
			xmax = rh

		if (ymin + pr.TOP_OFFSET) > 0:
			ymin = ymin + pr.TOP_OFFSET
		else: 
			ymin = 0

		if (ymax + pr.BOTTOM_OFFSET) > 0:
			ymax = ymax + pr.BOTTOM_OFFSET
		else: 
			ymax = 0
		#print "%d %d %d %d" % (xmax, xmin, ymax, ymin)
		w = xmax - xmin
		h = ymax - ymin

		if w * h == 0:
			acreageRatio = 1000
		else:
			acreageRatio = 1.0 * rh * rw / (w * h)
		whRatio = 1.0 * w / h
		if acreageRatio > pr.MIN_ACREAGE_RATIO and acreageRatio < pr.MAX_ACREAGE_RATIO:
			if whRatio > pr.MIN_WIDTH_HEIGHT_RATIO and whRatio < pr.MAX_WIDTH_HEIGHT_RATIO:
				if w > pr.MIN_WIDTH and w < pr.MAX_WIDTH and h > pr.MIN_HEIGHT and h < pr.MAX_HEIGHT:
					result.append((xmin, ymin, xmax, ymax))
					if pr.DEBUG:
						cropImg = color_src[ymin: ymax, xmin: xmax]
						cv2.imshow("plate", cropImg)
						cv2.rectangle(color_src, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
				else:
					if pr.DEBUG:
						cv2.rectangle(color_src, (xmin, ymin), (xmax, ymax), (0, 0, 255), 2)
			else:
				if pr.DEBUG:
					cv2.rectangle(color_src, (xmin, ymin), (xmax, ymax), (0, 0, 255), 2)
		else:
			if pr.DEBUG:
				cv2.rectangle(color_src, (xmin, ymin), (xmax, ymax), (0, 0, 255), 2)
	if pr.DEBUG:
		cv2.imshow("color_src", color_src)
		cv2.waitKey(0)
	return result
