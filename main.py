import cv2
import numpy as np
import param as pr
import preprocImage as ppi
import findPlate as fp
import findCharacter as fc

def main():
	root_src = cv2.imread("bien so xe/Car_ (9).jpg")
	src = cv2.resize(root_src, (pr.IMAGE_WIDTH_SIZE, pr.IMAGE_HEIGHT_SIZE))
	color_src = np.copy(src)
	src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

	cv2.imshow("src", src);

	preImg = ppi.preprocess(src)
	if pr.DEBUG:
		cv2.imshow("PreImg", preImg)
	plateArray = fp.findPlate(preImg, color_src)
	for i in xrange(0, len(plateArray)):
		img = np.copy(color_src[plateArray[i][1]: plateArray[i][3], \
			plateArray[i][0]: plateArray[i][2]])
		# cv2.imshow("img %d" % i, img)
		cv2.rectangle(color_src, (plateArray[i][0], plateArray[i][1]), \
			(plateArray[i][2], plateArray[i][3]), (0, 255, 0), 2)
		result = fc.findCharacter(img)
		if (pr.DEBUG):
			print("Len: %d" % len(result))
		if len(result) >= 5:
			for j in xrange(0, len(result)):
				cv2.imshow("%d" % j, result[j])
			if pr.DEBUG:
				cv2.waitKey(0)

	cv2.imshow("src", color_src)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

if __name__ == "__main__":
	main()