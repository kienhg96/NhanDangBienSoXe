import cv2
import numpy as np
import preprocImage as ppi
import findPlate as fp
import param as pr
import findCharacter as fc
import os

folder = "data"
def main():
	picNum = 752
	for filename in os.listdir(folder):
		root_src = cv2.imread(folder + '/' + filename);
		print filename
		src = cv2.resize(root_src, (pr.IMAGE_WIDTH_SIZE, pr.IMAGE_HEIGHT_SIZE))
		color_src = np.copy(src)
		src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
		preImg = ppi.preprocess(src)
		plateArray = fp.findPlate(preImg)	
		for i in xrange(0, len(plateArray)):
			img = np.copy(color_src[plateArray[i][1]: plateArray[i][3], \
				plateArray[i][0]: plateArray[i][2]])
			# cv2.imshow("img %d" % i, img)
			cv2.rectangle(color_src, (plateArray[i][0], plateArray[i][1]), \
				(plateArray[i][2], plateArray[i][3]), (0, 255, 0), 2)
			result = fc.findCharacter(img)
			if (len(result) >= 5):
				for j in xrange(0, len(result)):
					#cv2.imshow("%d" % j, result[j])
					cv2.imwrite("samples/sample(%d).jpg" % picNum, result[j])
					picNum = picNum + 1
	print "total character reconigze: %d" % picNum
if __name__ == "__main__":
	main()